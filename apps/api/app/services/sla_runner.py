import asyncio
import logging
import os
from typing import Optional

from sqlalchemy import text

from database import get_session
from app.routers.claim_router import sync_sla_escalation_state


logger = logging.getLogger("jkn_sentinel.sla_runner")

JOB_NAME = "SLA_ESCALATION"
ADVISORY_LOCK_ID = 42020

_scheduler_task: Optional[asyncio.Task] = None


def _interval_seconds() -> int:
    raw = os.getenv(
        "JKN_SLA_RUNNER_INTERVAL_SECONDS",
        "60"
    )

    try:
        value = int(raw)
    except (TypeError, ValueError):
        value = 60

    # Hindari loop terlalu agresif jika env salah.
    return max(value, 30)


def _record_failed_run(error_message: str):
    session = get_session()

    try:
        session.execute(
            text(
                """
                INSERT INTO system_job_state
                (
                    job_name,
                    last_started_at,
                    last_finished_at,
                    last_status,
                    last_transition_count,
                    last_error,
                    run_count,
                    updated_at
                )
                VALUES
                (
                    :job_name,
                    clock_timestamp(),
                    clock_timestamp(),
                    'FAILED',
                    0,
                    :last_error,
                    1,
                    clock_timestamp()
                )
                ON CONFLICT (job_name)
                DO UPDATE SET
                    last_finished_at = clock_timestamp(),
                    last_status = 'FAILED',
                    last_transition_count = 0,
                    last_error = EXCLUDED.last_error,
                    run_count = system_job_state.run_count + 1,
                    updated_at = clock_timestamp()
                """
            ),
            {
                "job_name": JOB_NAME,
                "last_error": error_message[:4000]
            }
        )

        session.commit()

    except Exception:
        session.rollback()
        logger.exception(
            "Gagal mencatat kegagalan SLA runner."
        )

    finally:
        session.close()


def run_sla_scheduler_once():
    """
    Menjalankan satu siklus SLA escalation secara sinkron.

    pg_try_advisory_xact_lock memastikan hanya satu worker/proses
    yang menjalankan siklus yang sama pada satu waktu. Lock otomatis
    dilepas saat transaction commit/rollback.
    """

    session = get_session()

    try:
        acquired = session.execute(
            text(
                """
                SELECT pg_try_advisory_xact_lock(
                    :lock_id
                )
                """
            ),
            {
                "lock_id": ADVISORY_LOCK_ID
            }
        ).scalar_one()

        if not acquired:
            session.rollback()

            return {
                "status": "SKIPPED_LOCKED",
                "transition_count": 0
            }

        session.execute(
            text(
                """
                INSERT INTO system_job_state
                (
                    job_name,
                    last_started_at,
                    last_finished_at,
                    last_status,
                    last_transition_count,
                    last_error,
                    run_count,
                    updated_at
                )
                VALUES
                (
                    :job_name,
                    clock_timestamp(),
                    NULL,
                    'RUNNING',
                    0,
                    NULL,
                    0,
                    clock_timestamp()
                )
                ON CONFLICT (job_name)
                DO UPDATE SET
                    last_started_at = clock_timestamp(),
                    last_finished_at = NULL,
                    last_status = 'RUNNING',
                    last_transition_count = 0,
                    last_error = NULL,
                    updated_at = clock_timestamp()
                """
            ),
            {
                "job_name": JOB_NAME
            }
        )

        transitions = sync_sla_escalation_state(
            session,
            claim_id=None
        )

        transition_count = len(transitions)

        session.execute(
            text(
                """
                UPDATE system_job_state
                SET
                    last_finished_at = clock_timestamp(),
                    last_status = 'SUCCESS',
                    last_transition_count = :transition_count,
                    last_error = NULL,
                    run_count = run_count + 1,
                    updated_at = clock_timestamp()
                WHERE job_name = :job_name
                """
            ),
            {
                "job_name": JOB_NAME,
                "transition_count": transition_count
            }
        )

        session.commit()

        return {
            "status": "SUCCESS",
            "transition_count": transition_count
        }

    except Exception as exc:
        session.rollback()

        error_message = (
            f"{exc.__class__.__name__}: {exc}"
        )

        logger.exception(
            "SLA automatic runner gagal."
        )

        _record_failed_run(
            error_message
        )

        return {
            "status": "FAILED",
            "transition_count": 0,
            "error": error_message
        }

    finally:
        session.close()


async def _scheduler_loop():
    interval = _interval_seconds()

    logger.info(
        "SLA automatic runner aktif. Interval=%s detik",
        interval
    )

    # Beri waktu aplikasi menyelesaikan startup.
    await asyncio.sleep(2)

    while True:
        try:
            result = await asyncio.to_thread(
                run_sla_scheduler_once
            )

            logger.info(
                "SLA runner result: %s",
                result
            )

            await asyncio.sleep(
                interval
            )

        except asyncio.CancelledError:
            logger.info(
                "SLA automatic runner dihentikan."
            )
            raise

        except Exception:
            logger.exception(
                "Unexpected SLA scheduler loop error."
            )

            await asyncio.sleep(
                interval
            )


async def start_sla_scheduler():
    global _scheduler_task

    if (
        _scheduler_task is None
        or _scheduler_task.done()
    ):
        _scheduler_task = asyncio.create_task(
            _scheduler_loop(),
            name="jkn-sentinel-sla-runner"
        )


async def stop_sla_scheduler():
    global _scheduler_task

    if _scheduler_task is None:
        return

    if not _scheduler_task.done():
        _scheduler_task.cancel()

        try:
            await _scheduler_task
        except asyncio.CancelledError:
            pass

    _scheduler_task = None
