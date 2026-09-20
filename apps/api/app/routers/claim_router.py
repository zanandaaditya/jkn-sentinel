from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import text
from pydantic import BaseModel
from typing import Optional

from database import get_session


router = APIRouter(
    prefix="/claims",
    tags=["Claims"]
)

# =====================================
# INVESTIGATION CASE REQUEST MODELS
# =====================================

class CreateFraudCaseRequest(BaseModel):
    assigned_to: Optional[str] = None
    investigation_note: Optional[str] = None


class UpdateFraudCaseRequest(BaseModel):
    case_status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    investigation_note: Optional[str] = None
    investigation_result: Optional[str] = None
    estimated_loss: Optional[float] = None
    confirmed_loss: Optional[float] = None
    recovered_amount: Optional[float] = None
    conclusion: Optional[str] = None


class AssignFraudCaseRequest(BaseModel):
    investigator_id: Optional[str] = None

    # sementara dipertahankan untuk kompatibilitas lama
    assigned_to: Optional[str] = None

class BulkAssignFraudCasesRequest(BaseModel):
    claim_ids: list[str]
    investigator_id: Optional[str] = None

    # sementara dipertahankan untuk kompatibilitas lama
    assigned_to: Optional[str] = None

class AutoAssignFraudCasesRequest(BaseModel):
    claim_ids: list[str]


def get_investigator_capacity_state(
    session,
    investigator_id: str
):

    investigator = session.execute(
        text(
            """
            SELECT
                iu.id,
                iu.full_name,
                iu.status,
                iu.role,
                iu.max_active_cases,

                COUNT(fc.id) FILTER (
                    WHERE fc.closed_at IS NULL
                ) AS active_cases

            FROM investigator_users iu

            LEFT JOIN fraud_cases fc
                ON fc.assigned_investigator_id = iu.id

            WHERE iu.id = :investigator_id

            GROUP BY
                iu.id,
                iu.full_name,
                iu.status,
                iu.role,
                iu.max_active_cases
            """
        ),
        {
            "investigator_id":
                investigator_id
        }
    ).mappings().first()

    if not investigator:

        raise HTTPException(
            status_code=404,
            detail="Investigator tidak ditemukan."
        )

    active_cases = int(
        investigator["active_cases"] or 0
    )

    max_active_cases = int(
        investigator["max_active_cases"] or 0
    )

    return {
        **investigator,
        "active_cases":
            active_cases,
        "max_active_cases":
            max_active_cases,
        "available_capacity":
            max(
                max_active_cases - active_cases,
                0
            )
    }


def ensure_investigator_capacity(
    session,
    investigator_id: str
):

    capacity = get_investigator_capacity_state(
        session,
        investigator_id
    )

    if capacity["status"] != "ACTIVE":

        raise HTTPException(
            status_code=400,
            detail="Investigator tidak aktif."
        )

    if capacity["role"] != "INVESTIGATOR":

        raise HTTPException(
            status_code=400,
            detail=(
                "Hanya user dengan role INVESTIGATOR "
                "yang dapat menerima kasus."
            )
        )

    if capacity["max_active_cases"] <= 0:

        raise HTTPException(
            status_code=409,
            detail=(
                f"{capacity['full_name']} tidak memiliki "
                "kapasitas kasus aktif."
            )
        )

    if (
        capacity["active_cases"]
        >=
        capacity["max_active_cases"]
    ):

        raise HTTPException(
            status_code=409,
            detail=(
                f"Kapasitas aktif {capacity['full_name']} "
                f"telah penuh "
                f"({capacity['active_cases']}/"
                f"{capacity['max_active_cases']})."
            )
        )

    return capacity


def select_lowest_load_investigator(
    session
):

    return session.execute(
        text(
            """
            SELECT
                iu.id,
                iu.full_name,
                iu.max_active_cases,

                COUNT(fc.id) FILTER (
                    WHERE fc.closed_at IS NULL
                ) AS active_cases,

                ROUND(
                    (
                        COUNT(fc.id) FILTER (
                            WHERE fc.closed_at IS NULL
                        )::numeric
                        /
                        NULLIF(
                            iu.max_active_cases,
                            0
                        )::numeric
                    ),
                    6
                ) AS load_ratio

            FROM investigator_users iu

            LEFT JOIN fraud_cases fc
                ON fc.assigned_investigator_id = iu.id

            WHERE
                iu.status = 'ACTIVE'
                AND
                iu.role = 'INVESTIGATOR'
                AND
                iu.max_active_cases > 0

            GROUP BY
                iu.id,
                iu.full_name,
                iu.max_active_cases

            HAVING
                COUNT(fc.id) FILTER (
                    WHERE fc.closed_at IS NULL
                )
                <
                iu.max_active_cases

            ORDER BY
                load_ratio ASC,
                active_cases ASC,
                iu.full_name ASC

            LIMIT 1
            """
        )
    ).mappings().first()

# =====================================
# HELPER — INVESTIGATOR ASSIGNMENT
# =====================================

def resolve_investigator_assignment(
    session,
    investigator_id: Optional[str],
    assigned_to: Optional[str]
):

    if (
        investigator_id
        and investigator_id.strip()
    ):

        investigator = session.execute(
            text(
                """
                SELECT
                    id,
                    full_name,
                    status
                FROM investigator_users
                WHERE id = :id
                LIMIT 1
                """
            ),
            {
                "id":
                    investigator_id.strip()
            }
        ).mappings().first()


        if not investigator:

            raise HTTPException(
                status_code=404,
                detail="Investigator tidak ditemukan."
            )


        if investigator["status"] != "ACTIVE":

            raise HTTPException(
                status_code=400,
                detail="Investigator tidak aktif."
            )


        return (
            investigator["id"],
            investigator["full_name"]
        )


    if (
        assigned_to
        and assigned_to.strip()
    ):

        investigator = session.execute(
            text(
                """
                SELECT
                    id,
                    full_name,
                    status
                FROM investigator_users
                WHERE
                    LOWER(TRIM(full_name))
                    =
                    LOWER(TRIM(:full_name))
                LIMIT 1
                """
            ),
            {
                "full_name":
                    assigned_to.strip()
            }
        ).mappings().first()


        if not investigator:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Investigator belum terdaftar "
                    "di Investigator Registry."
                )
            )


        if investigator["status"] != "ACTIVE":

            raise HTTPException(
                status_code=400,
                detail="Investigator tidak aktif."
            )


        return (
            investigator["id"],
            investigator["full_name"]
        )


    return (
        None,
        None
    )
# =====================================
# FRAUD CASE QUEUE
# SERVER SIDE FILTER + PAGINATION
# =====================================

@router.get("/cases/queue")
def get_fraud_case_queue(

    case_status: Optional[str] = Query(
        default=None
    ),

    priority: Optional[str] = Query(
        default=None
    ),

    assigned_to: Optional[str] = Query(
        default=None
    ),

    search: Optional[str] = Query(
        default=None
    ),

    page: int = Query(
        default=1,
        ge=1
    ),

    page_size: int = Query(
        default=10,
        ge=5,
        le=100
    )

):

    session = get_session()


    # =====================================
    # NORMALIZE FILTER
    # =====================================

    normalized_status = (
        case_status.strip().upper()
        if case_status
        else None
    )


    normalized_priority = (
        priority.strip().upper()
        if priority
        else None
    )


    search_value = (
        f"%{search.strip()}%"
        if search and search.strip()
        else None
    )


    assigned_value = (
        f"%{assigned_to.strip()}%"
        if assigned_to and assigned_to.strip()
        else None
    )



    # =====================================
    # VALIDATE STATUS
    # =====================================

    allowed_status = [
        "NEW",
        "REVIEWING",
        "CONFIRMED",
        "CLEARED"
    ]


    if (
        normalized_status
        and
        normalized_status not in allowed_status
    ):

        session.close()

        raise HTTPException(
            status_code=400,
            detail="Filter status tidak valid"
        )



    # =====================================
    # VALIDATE PRIORITY
    # =====================================

    allowed_priority = [
        "LOW",
        "NORMAL",
        "MEDIUM",
        "HIGH",
        "URGENT"
    ]


    if (
        normalized_priority
        and
        normalized_priority not in allowed_priority
    ):

        session.close()

        raise HTTPException(
            status_code=400,
            detail="Filter priority tidak valid"
        )



    # =====================================
    # PAGINATION
    # =====================================

    offset = (
        page - 1
    ) * page_size



    params = {

        "case_status":
            normalized_status,

        "priority":
            normalized_priority,

        "assigned_to":
            assigned_value,

        "search":
            search_value,

        "limit":
            page_size,

        "offset":
            offset

    }



    # =====================================
    # TOTAL FILTERED DATA
    # =====================================

    total = session.execute(
        text(
            """
            SELECT
                COUNT(*)

            FROM fraud_cases fc


            INNER JOIN claims c
                ON fc.claim_id = c.id


            LEFT JOIN facilities f
                ON c.facility_id = f.id


            LEFT JOIN diagnosis d
                ON c.diagnosis_id = d.id


            WHERE

                (
                    :case_status IS NULL
                    OR fc.case_status = :case_status
                )

                AND

                (
                    :priority IS NULL
                    OR fc.priority = :priority
                )

                AND

                (
                    :assigned_to IS NULL
                    OR fc.assigned_to ILIKE :assigned_to
                )

                AND

                (
                    :search IS NULL

                    OR c.claim_code ILIKE :search

                    OR f.facility_name ILIKE :search

                    OR d.name ILIKE :search

                    OR fc.assigned_to ILIKE :search
                )
            """
        ),
        params

    ).scalar_one()



    # =====================================
    # QUEUE DATA
    # =====================================

    items = session.execute(
        text(
            """
            SELECT

                fc.id AS case_id,

                fc.claim_id,

                fc.case_status,

                fc.priority,

                fc.assigned_investigator_id,

                fc.assigned_to,

                fc.investigation_result,

                fc.created_at,

                fc.closed_at,

                c.claim_code,

                c.claim_amount,

                c.fraud_score,

                c.risk_level,

                c.service_date,

                f.facility_name AS facility,

                d.name AS diagnosis

            FROM fraud_cases fc

            INNER JOIN claims c
                ON fc.claim_id = c.id

            LEFT JOIN facilities f
                ON c.facility_id = f.id

            LEFT JOIN diagnosis d
                ON c.diagnosis_id = d.id

            WHERE

                (
                    :case_status IS NULL
                    OR fc.case_status = :case_status
                )

                AND

                (
                    :priority IS NULL
                    OR fc.priority = :priority
                )

                AND

                (
                    :assigned_to IS NULL
                    OR fc.assigned_to ILIKE :assigned_to
                )

                AND

                (
                    :search IS NULL

                    OR c.claim_code ILIKE :search

                    OR f.facility_name ILIKE :search

                    OR d.name ILIKE :search

                    OR fc.assigned_to ILIKE :search
                )

            ORDER BY

                CASE fc.priority
                    WHEN 'URGENT' THEN 1
                    WHEN 'HIGH' THEN 2
                    WHEN 'MEDIUM' THEN 3
                    WHEN 'NORMAL' THEN 4
                    WHEN 'LOW' THEN 5
                    ELSE 6
                END,

                c.fraud_score DESC,

                fc.created_at ASC

            LIMIT :limit

            OFFSET :offset
            """
        ),
        params
    ).mappings().all()



    # =====================================
    # GLOBAL QUEUE SUMMARY
    # =====================================

    summary = session.execute(
        text(
            """
            SELECT

                COUNT(*) AS total_cases,


                COUNT(*) FILTER (
                    WHERE case_status = 'NEW'
                ) AS new_cases,


                COUNT(*) FILTER (
                    WHERE case_status = 'REVIEWING'
                ) AS reviewing_cases,


                COUNT(*) FILTER (
                    WHERE case_status = 'CONFIRMED'
                ) AS confirmed_cases,


                COUNT(*) FILTER (
                    WHERE case_status = 'CLEARED'
                ) AS cleared_cases,


                COUNT(*) FILTER (
                    WHERE priority = 'URGENT'
                ) AS urgent_cases,


                COUNT(*) FILTER (
                    WHERE priority = 'HIGH'
                ) AS high_priority_cases


            FROM fraud_cases
            """
        )

    ).mappings().first()



    # =====================================
    # CALCULATE TOTAL PAGES
    # =====================================

    total_pages = (
        total + page_size - 1
    ) // page_size



    session.close()



    # =====================================
    # RESPONSE
    # =====================================

    return {

        "items":
            items,

        "pagination": {

            "page":
                page,

            "page_size":
                page_size,

            "total":
                total,

            "total_pages":
                total_pages,

            "has_previous":
                page > 1,

            "has_next":
                page < total_pages

        },

        "summary":
            summary

    }

# =====================================
# FRAUD INVESTIGATION ANALYTICS
# IMPORTANT:
# Place this endpoint BEFORE @router.get("/{claim_id}")
# =====================================

@router.get("/cases/analytics")
def get_fraud_case_analytics():

    session = get_session()


    # =====================================
    # CASE SUMMARY
    # =====================================

    summary = session.execute(
        text(
            """
            SELECT

                COUNT(*) AS total_cases,

                COUNT(*) FILTER (
                    WHERE case_status = 'NEW'
                ) AS new_cases,

                COUNT(*) FILTER (
                    WHERE case_status = 'REVIEWING'
                ) AS reviewing_cases,

                COUNT(*) FILTER (
                    WHERE case_status = 'CONFIRMED'
                ) AS confirmed_cases,

                COUNT(*) FILTER (
                    WHERE case_status = 'CLEARED'
                ) AS cleared_cases,

                COUNT(*) FILTER (
                    WHERE closed_at IS NULL
                ) AS active_cases,

                COUNT(*) FILTER (
                    WHERE closed_at IS NOT NULL
                ) AS closed_cases

            FROM fraud_cases
            """
        )
    ).mappings().first()



    # =====================================
    # FINANCIAL SUMMARY
    # =====================================

    financial = session.execute(
        text(
            """
            SELECT

                COALESCE(
                    SUM(estimated_loss),
                    0
                ) AS total_estimated_loss,

                COALESCE(
                    SUM(confirmed_loss),
                    0
                ) AS total_confirmed_loss,

                COALESCE(
                    SUM(recovered_amount),
                    0
                ) AS total_recovered_amount,

                GREATEST(
                    COALESCE(
                        SUM(confirmed_loss),
                        0
                    )
                    -
                    COALESCE(
                        SUM(recovered_amount),
                        0
                    ),
                    0
                ) AS outstanding_loss,

                CASE

                    WHEN
                        COALESCE(
                            SUM(confirmed_loss),
                            0
                        ) > 0

                    THEN
                        ROUND(
                            (
                                COALESCE(
                                    SUM(recovered_amount),
                                    0
                                )
                                /
                                COALESCE(
                                    SUM(confirmed_loss),
                                    0
                                )
                            )
                            *
                            100,
                            2
                        )

                    ELSE 0

                END AS recovery_rate

            FROM fraud_cases
            """
        )
    ).mappings().first()



    # =====================================
    # STATUS DISTRIBUTION
    # =====================================

    status_distribution = session.execute(
        text(
            """
            SELECT

                case_status,

                COUNT(*) AS total

            FROM fraud_cases

            GROUP BY case_status

            ORDER BY
                CASE case_status
                    WHEN 'NEW' THEN 1
                    WHEN 'REVIEWING' THEN 2
                    WHEN 'CONFIRMED' THEN 3
                    WHEN 'CLEARED' THEN 4
                    ELSE 5
                END
            """
        )
    ).mappings().all()



    # =====================================
    # PRIORITY DISTRIBUTION
    # =====================================

    priority_distribution = session.execute(
        text(
            """
            SELECT

                priority,

                COUNT(*) AS total

            FROM fraud_cases

            GROUP BY priority

            ORDER BY
                CASE priority
                    WHEN 'URGENT' THEN 1
                    WHEN 'HIGH' THEN 2
                    WHEN 'MEDIUM' THEN 3
                    WHEN 'NORMAL' THEN 4
                    WHEN 'LOW' THEN 5
                    ELSE 6
                END
            """
        )
    ).mappings().all()



    # =====================================
    # RISK DISTRIBUTION
    # =====================================

    risk_distribution = session.execute(
        text(
            """
            SELECT

                c.risk_level,

                COUNT(*) AS total

            FROM fraud_cases fc

            INNER JOIN claims c
                ON c.id = fc.claim_id

            GROUP BY c.risk_level

            ORDER BY
                CASE c.risk_level
                    WHEN 'HIGH' THEN 1
                    WHEN 'MEDIUM' THEN 2
                    WHEN 'LOW' THEN 3
                    ELSE 4
                END
            """
        )
    ).mappings().all()



    session.close()


    return {

        "summary":
            summary,

        "financial_summary":
            financial,

        "status_distribution":
            status_distribution,

        "priority_distribution":
            priority_distribution,

        "risk_distribution":
            risk_distribution

    }

# =====================================
# SLA POLICY ENGINE
# FASE 4.20
# =====================================

@router.get("/cases/sla-policies")
def get_sla_policies():

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                priority,
                sla_hours,
                warning_hours_before,
                critical_hours_after_breach,
                description,
                is_active,
                created_at,
                updated_at
            FROM fraud_sla_policy
            ORDER BY
                CASE priority
                    WHEN 'URGENT' THEN 1
                    WHEN 'HIGH' THEN 2
                    WHEN 'MEDIUM' THEN 3
                    WHEN 'NORMAL' THEN 4
                    WHEN 'LOW' THEN 5
                    ELSE 6
                END
            """
        )
    ).mappings().all()

    session.close()

    return result


@router.get("/cases/sla-summary")
def get_sla_summary():

    session = get_session()

    result = session.execute(
        text(
            """
            WITH case_sla AS (
                SELECT
                    fc.id,
                    fc.closed_at,
                    sp.priority AS policy_priority,
                    fc.created_at
                        + (sp.sla_hours * INTERVAL '1 hour')
                        AS sla_due_at,
                    fc.created_at
                        + (
                            (
                                sp.sla_hours
                                - sp.warning_hours_before
                            ) * INTERVAL '1 hour'
                        ) AS sla_warning_at,
                    fc.created_at
                        + (
                            (
                                sp.sla_hours
                                + sp.critical_hours_after_breach
                            ) * INTERVAL '1 hour'
                        ) AS sla_critical_at
                FROM fraud_cases fc
                LEFT JOIN fraud_sla_policy sp
                    ON sp.priority = fc.priority
                    AND sp.is_active = TRUE
            ),
            classified AS (
                SELECT
                    *,
                    CASE
                        WHEN policy_priority IS NULL
                        THEN 'NO_POLICY'

                        WHEN closed_at IS NOT NULL
                             AND closed_at <= sla_due_at
                        THEN 'CLOSED_WITHIN_SLA'

                        WHEN closed_at IS NOT NULL
                             AND closed_at > sla_due_at
                        THEN 'CLOSED_BREACHED'

                        WHEN CURRENT_TIMESTAMP >= sla_critical_at
                        THEN 'CRITICAL'

                        WHEN CURRENT_TIMESTAMP > sla_due_at
                        THEN 'BREACHED'

                        WHEN CURRENT_TIMESTAMP >= sla_warning_at
                        THEN 'WARNING'

                        ELSE 'ON_TRACK'
                    END AS sla_status
                FROM case_sla
            )
            SELECT
                COUNT(*) AS total_cases,

                COUNT(*) FILTER (
                    WHERE closed_at IS NULL
                ) AS active_cases,

                COUNT(*) FILTER (
                    WHERE sla_status = 'ON_TRACK'
                ) AS on_track_cases,

                COUNT(*) FILTER (
                    WHERE sla_status = 'WARNING'
                ) AS warning_cases,

                COUNT(*) FILTER (
                    WHERE sla_status = 'BREACHED'
                ) AS breached_cases,

                COUNT(*) FILTER (
                    WHERE sla_status = 'CRITICAL'
                ) AS critical_cases,

                COUNT(*) FILTER (
                    WHERE sla_status = 'CLOSED_WITHIN_SLA'
                ) AS closed_within_sla_cases,

                COUNT(*) FILTER (
                    WHERE sla_status = 'CLOSED_BREACHED'
                ) AS closed_breached_cases,

                COUNT(*) FILTER (
                    WHERE sla_status = 'NO_POLICY'
                ) AS no_policy_cases

            FROM classified
            """
        )
    ).mappings().first()

    session.close()

    return {
        "mode": "PRIORITY_POLICY",
        "summary": result
    }


# =====================================
# SLA ESCALATION ENGINE + AUDIT TRAIL
# FASE 4.20C
# =====================================

def sync_sla_escalation_state(
    session,
    claim_id: Optional[str] = None
):

    transitions = session.execute(
        text(
            """
            WITH computed AS (
                SELECT
                    fc.id AS case_id,
                    fc.claim_id,
                    fc.case_status,
                    fc.priority,
                    fc.assigned_to,
                    fc.closed_at,
                    fc.sla_last_status AS old_sla_status,

                    fc.created_at
                        + (sp.sla_hours * INTERVAL '1 hour')
                        AS sla_due_at,

                    fc.created_at
                        + (
                            (
                                sp.sla_hours
                                - sp.warning_hours_before
                            ) * INTERVAL '1 hour'
                        ) AS sla_warning_at,

                    fc.created_at
                        + (
                            (
                                sp.sla_hours
                                + sp.critical_hours_after_breach
                            ) * INTERVAL '1 hour'
                        ) AS sla_critical_at,

                    CASE
                        WHEN sp.priority IS NULL
                        THEN 'NO_POLICY'

                        WHEN fc.closed_at IS NOT NULL
                             AND fc.closed_at <=
                                fc.created_at
                                + (sp.sla_hours * INTERVAL '1 hour')
                        THEN 'CLOSED_WITHIN_SLA'

                        WHEN fc.closed_at IS NOT NULL
                             AND fc.closed_at >
                                fc.created_at
                                + (sp.sla_hours * INTERVAL '1 hour')
                        THEN 'CLOSED_BREACHED'

                        WHEN CURRENT_TIMESTAMP >=
                            fc.created_at
                            + (
                                (
                                    sp.sla_hours
                                    + sp.critical_hours_after_breach
                                ) * INTERVAL '1 hour'
                            )
                        THEN 'CRITICAL'

                        WHEN CURRENT_TIMESTAMP >
                            fc.created_at
                            + (sp.sla_hours * INTERVAL '1 hour')
                        THEN 'BREACHED'

                        WHEN CURRENT_TIMESTAMP >=
                            fc.created_at
                            + (
                                (
                                    sp.sla_hours
                                    - sp.warning_hours_before
                                ) * INTERVAL '1 hour'
                            )
                        THEN 'WARNING'

                        ELSE 'ON_TRACK'
                    END AS new_sla_status

                FROM fraud_cases fc

                LEFT JOIN fraud_sla_policy sp
                    ON sp.priority = fc.priority
                    AND sp.is_active = TRUE

                WHERE
                    CAST(:claim_id AS uuid) IS NULL
                    OR fc.claim_id = CAST(:claim_id AS uuid)
            ),

            changed AS (
                UPDATE fraud_cases fc

                SET
                    sla_last_status =
                        c.new_sla_status,

                    sla_status_updated_at =
                        CURRENT_TIMESTAMP,

                    sla_last_escalated_at =
                        CASE
                            WHEN c.new_sla_status IN (
                                'WARNING',
                                'BREACHED',
                                'CRITICAL'
                            )
                            THEN CURRENT_TIMESTAMP
                            ELSE fc.sla_last_escalated_at
                        END

                FROM computed c

                WHERE
                    fc.id = c.case_id
                    AND fc.sla_last_status
                        IS DISTINCT FROM
                        c.new_sla_status

                RETURNING
                    fc.id AS case_id,
                    fc.claim_id,
                    c.case_status,
                    c.priority,
                    c.assigned_to,
                    c.old_sla_status,
                    c.new_sla_status,
                    c.sla_due_at,
                    c.sla_warning_at,
                    c.sla_critical_at,
                    fc.sla_status_updated_at,
                    fc.sla_last_escalated_at
            )

            SELECT *
            FROM changed
            ORDER BY case_id
            """
        ),
        {
            "claim_id": claim_id
        }
    ).mappings().all()


    event_map = {
        "ON_TRACK":
            "SLA_RETURNED_ON_TRACK",

        "WARNING":
            "SLA_WARNING",

        "BREACHED":
            "SLA_BREACHED",

        "CRITICAL":
            "SLA_CRITICAL",

        "CLOSED_WITHIN_SLA":
            "SLA_CLOSED_WITHIN_SLA",

        "CLOSED_BREACHED":
            "SLA_CLOSED_BREACHED",

        "NO_POLICY":
            "SLA_NO_POLICY"
    }


    for transition in transitions:

        old_sla_status = (
            transition["old_sla_status"]
        )

        new_sla_status = (
            transition["new_sla_status"]
        )


        if old_sla_status is None:

            event_type = (
                "SLA_MONITORING_STARTED"
            )

        else:

            event_type = event_map.get(
                new_sla_status,
                "SLA_STATUS_CHANGED"
            )


        note_parts = [
            (
                "Status SLA: "
                f"{old_sla_status or 'BELUM_DICATAT'}"
                " -> "
                f"{new_sla_status}"
            )
        ]


        if transition["sla_due_at"] is not None:

            note_parts.append(
                "Batas SLA: "
                f"{transition['sla_due_at']}"
            )


        if transition["assigned_to"]:

            note_parts.append(
                "Investigator: "
                f"{transition['assigned_to']}"
            )


        session.execute(
            text(
                """
                INSERT INTO fraud_case_history
                (
                    fraud_case_id,
                    claim_id,
                    event_type,
                    old_status,
                    new_status,
                    old_priority,
                    new_priority,
                    old_assigned_to,
                    new_assigned_to,
                    note,
                    actor
                )
                VALUES
                (
                    :fraud_case_id,
                    :claim_id,
                    :event_type,
                    :old_status,
                    :new_status,
                    :old_priority,
                    :new_priority,
                    :old_assigned_to,
                    :new_assigned_to,
                    :note,
                    'SLA_ENGINE'
                )
                """
            ),
            {
                "fraud_case_id":
                    transition["case_id"],

                "claim_id":
                    transition["claim_id"],

                "event_type":
                    event_type,

                "old_status":
                    transition["case_status"],

                "new_status":
                    transition["case_status"],

                "old_priority":
                    transition["priority"],

                "new_priority":
                    transition["priority"],

                "old_assigned_to":
                    transition["assigned_to"],

                "new_assigned_to":
                    transition["assigned_to"],

                "note":
                    " | ".join(note_parts)
            }
        )


    return transitions


# =====================================
# SLA AUTOMATIC RUNNER STATUS
# FASE 4.20E
# =====================================

@router.get("/cases/sla-runner/status")
def get_sla_runner_status():

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                job_name,
                last_started_at,
                last_finished_at,
                last_status,
                last_transition_count,
                last_error,
                run_count,
                updated_at
            FROM system_job_state
            WHERE job_name = 'SLA_ESCALATION'
            LIMIT 1
            """
        )
    ).mappings().first()

    session.close()

    if not result:
        return {
            "job_name": "SLA_ESCALATION",
            "last_status": "NOT_STARTED",
            "last_started_at": None,
            "last_finished_at": None,
            "last_transition_count": 0,
            "last_error": None,
            "run_count": 0,
            "updated_at": None
        }

    return result


@router.post("/cases/sla-escalation/run")
def run_sla_escalation_engine(
    claim_id: Optional[str] = Query(
        default=None
    )
):

    session = get_session()

    try:

        transitions = (
            sync_sla_escalation_state(
                session,
                claim_id=claim_id
            )
        )

        session.commit()

    except Exception:

        session.rollback()
        session.close()
        raise


    counts = {
        "ON_TRACK": 0,
        "WARNING": 0,
        "BREACHED": 0,
        "CRITICAL": 0,
        "CLOSED_WITHIN_SLA": 0,
        "CLOSED_BREACHED": 0,
        "NO_POLICY": 0
    }


    for transition in transitions:

        status = transition[
            "new_sla_status"
        ]

        if status in counts:
            counts[status] += 1


    response = {
        "mode":
            "PRIORITY_POLICY",

        "scope":
            "SINGLE_CASE"
            if claim_id
            else "ALL_CASES",

        "claim_id":
            claim_id,

        "transition_count":
            len(transitions),

        "transition_summary":
            counts,

        "transitions":
            transitions
    }


    session.close()

    return response


# =====================================
# INVESTIGATOR PERFORMANCE + CASE AGING + SLA
# IMPORTANT:
# Place this endpoint BEFORE @router.get("/{claim_id}")
# =====================================

@router.get("/cases/investigator-analytics")
def get_investigator_analytics(
    sla_days: Optional[int] = Query(
        default=None,
        ge=1,
        le=365,
        description="Legacy parameter; SLA sekarang mengikuti fraud_sla_policy."
    )
):

    session = get_session()

    # =====================================
    # SUMMARY — POLICY DRIVEN SLA
    # =====================================

    summary = session.execute(
        text(
            """
            WITH case_metrics AS (
                SELECT
                    fc.*,
                    sp.priority AS policy_priority,
                    sp.sla_hours,
                    sp.warning_hours_before,
                    sp.critical_hours_after_breach,

                    (
                        EXTRACT(
                            EPOCH FROM (
                                COALESCE(
                                    fc.closed_at,
                                    CURRENT_TIMESTAMP
                                )
                                - fc.created_at
                            )
                        ) / 86400.0
                    ) AS age_days,

                    fc.created_at
                        + (sp.sla_hours * INTERVAL '1 hour')
                        AS sla_due_at,

                    fc.created_at
                        + (
                            (
                                sp.sla_hours
                                - sp.warning_hours_before
                            ) * INTERVAL '1 hour'
                        ) AS sla_warning_at,

                    fc.created_at
                        + (
                            (
                                sp.sla_hours
                                + sp.critical_hours_after_breach
                            ) * INTERVAL '1 hour'
                        ) AS sla_critical_at

                FROM fraud_cases fc

                LEFT JOIN fraud_sla_policy sp
                    ON sp.priority = fc.priority
                    AND sp.is_active = TRUE
            ),
            classified AS (
                SELECT
                    *,
                    CASE
                        WHEN policy_priority IS NULL
                        THEN 'NO_POLICY'

                        WHEN closed_at IS NOT NULL
                             AND closed_at <= sla_due_at
                        THEN 'CLOSED_WITHIN_SLA'

                        WHEN closed_at IS NOT NULL
                             AND closed_at > sla_due_at
                        THEN 'CLOSED_BREACHED'

                        WHEN CURRENT_TIMESTAMP >= sla_critical_at
                        THEN 'CRITICAL'

                        WHEN CURRENT_TIMESTAMP > sla_due_at
                        THEN 'BREACHED'

                        WHEN CURRENT_TIMESTAMP >= sla_warning_at
                        THEN 'WARNING'

                        ELSE 'ON_TRACK'
                    END AS sla_status
                FROM case_metrics
            )
            SELECT
                COUNT(*) AS total_cases,

                COUNT(*) FILTER (
                    WHERE closed_at IS NULL
                ) AS active_cases,

                COUNT(*) FILTER (
                    WHERE closed_at IS NOT NULL
                ) AS closed_cases,

                COUNT(*) FILTER (
                    WHERE
                        closed_at IS NULL
                        AND sla_status IN ('BREACHED', 'CRITICAL')
                ) AS overdue_active_cases,

                COUNT(*) FILTER (
                    WHERE
                        closed_at IS NULL
                        AND sla_status = 'WARNING'
                ) AS warning_active_cases,

                COUNT(*) FILTER (
                    WHERE
                        closed_at IS NULL
                        AND sla_status = 'CRITICAL'
                ) AS critical_active_cases,

                COUNT(*) FILTER (
                    WHERE sla_status = 'NO_POLICY'
                ) AS no_policy_cases,

                ROUND(
                    COALESCE(
                        AVG(age_days) FILTER (
                            WHERE closed_at IS NULL
                        ),
                        0
                    )::numeric,
                    2
                ) AS avg_active_case_age_days,

                ROUND(
                    COALESCE(
                        AVG(age_days) FILTER (
                            WHERE closed_at IS NOT NULL
                        ),
                        0
                    )::numeric,
                    2
                ) AS avg_resolution_days,

                ROUND(
                    CASE
                        WHEN COUNT(*) FILTER (
                            WHERE
                                closed_at IS NOT NULL
                                AND policy_priority IS NOT NULL
                        ) > 0
                        THEN
                            (
                                COUNT(*) FILTER (
                                    WHERE
                                        closed_at IS NOT NULL
                                        AND sla_status = 'CLOSED_WITHIN_SLA'
                                )::numeric
                                /
                                COUNT(*) FILTER (
                                    WHERE
                                        closed_at IS NOT NULL
                                        AND policy_priority IS NOT NULL
                                )
                            ) * 100
                        ELSE 0
                    END,
                    2
                ) AS sla_compliance_rate

            FROM classified
            """
        )
    ).mappings().first()


    # =====================================
    # INVESTIGATOR PERFORMANCE
    # =====================================

    investigator_performance = session.execute(
        text(
            """
            WITH case_metrics AS (
                SELECT
                    fc.*,
                    sp.priority AS policy_priority,

                    (
                        EXTRACT(
                            EPOCH FROM (
                                COALESCE(
                                    fc.closed_at,
                                    CURRENT_TIMESTAMP
                                )
                                - fc.created_at
                            )
                        ) / 86400.0
                    ) AS age_days,

                    fc.created_at
                        + (sp.sla_hours * INTERVAL '1 hour')
                        AS sla_due_at,

                    fc.created_at
                        + (
                            (
                                sp.sla_hours
                                - sp.warning_hours_before
                            ) * INTERVAL '1 hour'
                        ) AS sla_warning_at,

                    fc.created_at
                        + (
                            (
                                sp.sla_hours
                                + sp.critical_hours_after_breach
                            ) * INTERVAL '1 hour'
                        ) AS sla_critical_at

                FROM fraud_cases fc

                LEFT JOIN fraud_sla_policy sp
                    ON sp.priority = fc.priority
                    AND sp.is_active = TRUE
            ),
            classified AS (
                SELECT
                    *,
                    CASE
                        WHEN policy_priority IS NULL
                        THEN 'NO_POLICY'

                        WHEN closed_at IS NOT NULL
                             AND closed_at <= sla_due_at
                        THEN 'CLOSED_WITHIN_SLA'

                        WHEN closed_at IS NOT NULL
                             AND closed_at > sla_due_at
                        THEN 'CLOSED_BREACHED'

                        WHEN CURRENT_TIMESTAMP >= sla_critical_at
                        THEN 'CRITICAL'

                        WHEN CURRENT_TIMESTAMP > sla_due_at
                        THEN 'BREACHED'

                        WHEN CURRENT_TIMESTAMP >= sla_warning_at
                        THEN 'WARNING'

                        ELSE 'ON_TRACK'
                    END AS sla_status
                FROM case_metrics
            )
            SELECT
                COALESCE(
                    NULLIF(
                        TRIM(assigned_to),
                        ''
                    ),
                    'Belum Ditugaskan'
                ) AS investigator,

                COUNT(*) AS total_cases,

                COUNT(*) FILTER (
                    WHERE closed_at IS NULL
                ) AS active_cases,

                COUNT(*) FILTER (
                    WHERE closed_at IS NOT NULL
                ) AS closed_cases,

                COUNT(*) FILTER (
                    WHERE
                        closed_at IS NULL
                        AND sla_status IN ('BREACHED', 'CRITICAL')
                ) AS overdue_cases,

                COUNT(*) FILTER (
                    WHERE
                        closed_at IS NULL
                        AND sla_status = 'WARNING'
                ) AS warning_cases,

                COUNT(*) FILTER (
                    WHERE
                        closed_at IS NULL
                        AND sla_status = 'CRITICAL'
                ) AS critical_cases,

                ROUND(
                    COALESCE(
                        AVG(age_days),
                        0
                    )::numeric,
                    2
                ) AS avg_case_age_days,

                COALESCE(
                    SUM(confirmed_loss),
                    0
                ) AS confirmed_loss,

                COALESCE(
                    SUM(recovered_amount),
                    0
                ) AS recovered_amount

            FROM classified

            GROUP BY
                COALESCE(
                    NULLIF(
                        TRIM(assigned_to),
                        ''
                    ),
                    'Belum Ditugaskan'
                )

            ORDER BY
                critical_cases DESC,
                overdue_cases DESC,
                active_cases DESC,
                total_cases DESC,
                investigator ASC
            """
        )
    ).mappings().all()


    # =====================================
    # ACTIVE CASE AGING DISTRIBUTION
    # =====================================

    aging_distribution = session.execute(
        text(
            """
            WITH active_case_age AS (
                SELECT
                    (
                        EXTRACT(
                            EPOCH FROM (
                                CURRENT_TIMESTAMP
                                - created_at
                            )
                        ) / 86400.0
                    ) AS age_days
                FROM fraud_cases
                WHERE closed_at IS NULL
            ),
            bucketed AS (
                SELECT
                    CASE
                        WHEN age_days <= 3
                        THEN '0-3_DAYS'
                        WHEN age_days <= 7
                        THEN '4-7_DAYS'
                        WHEN age_days <= 14
                        THEN '8-14_DAYS'
                        ELSE 'OVER_14_DAYS'
                    END AS bucket
                FROM active_case_age
            )
            SELECT
                bucket,
                COUNT(*) AS total
            FROM bucketed
            GROUP BY bucket
            ORDER BY
                CASE bucket
                    WHEN '0-3_DAYS' THEN 1
                    WHEN '4-7_DAYS' THEN 2
                    WHEN '8-14_DAYS' THEN 3
                    WHEN 'OVER_14_DAYS' THEN 4
                    ELSE 5
                END
            """
        )
    ).mappings().all()


    # =====================================
    # OLDEST / MOST URGENT ACTIVE CASES
    # =====================================

    oldest_active_cases = session.execute(
        text(
            """
            SELECT
                fc.id AS case_id,
                fc.claim_id,
                c.claim_code,
                c.fraud_score,
                c.risk_level,
                fc.priority,
                fc.assigned_investigator_id,
                fc.assigned_to,
                fc.case_status,
                fc.created_at,

                ROUND(
                    (
                        EXTRACT(
                            EPOCH FROM (
                                CURRENT_TIMESTAMP
                                - fc.created_at
                            )
                        ) / 86400.0
                    )::numeric,
                    2
                ) AS age_days,

                sp.sla_hours,
                sp.warning_hours_before,
                sp.critical_hours_after_breach,

                fc.created_at
                    + (sp.sla_hours * INTERVAL '1 hour')
                    AS sla_due_at,

                CASE
                    WHEN sp.priority IS NULL
                    THEN 'NO_POLICY'

                    WHEN CURRENT_TIMESTAMP >=
                        fc.created_at
                        + (
                            (
                                sp.sla_hours
                                + sp.critical_hours_after_breach
                            ) * INTERVAL '1 hour'
                        )
                    THEN 'CRITICAL'

                    WHEN CURRENT_TIMESTAMP >
                        fc.created_at
                        + (sp.sla_hours * INTERVAL '1 hour')
                    THEN 'BREACHED'

                    WHEN CURRENT_TIMESTAMP >=
                        fc.created_at
                        + (
                            (
                                sp.sla_hours
                                - sp.warning_hours_before
                            ) * INTERVAL '1 hour'
                        )
                    THEN 'WARNING'

                    ELSE 'ON_TRACK'
                END AS sla_status,

                CASE
                    WHEN sp.priority IS NULL
                    THEN FALSE
                    WHEN CURRENT_TIMESTAMP >
                        fc.created_at
                        + (sp.sla_hours * INTERVAL '1 hour')
                    THEN TRUE
                    ELSE FALSE
                END AS sla_breached,

                ROUND(
                    (
                        EXTRACT(
                            EPOCH FROM (
                                (
                                    fc.created_at
                                    + (sp.sla_hours * INTERVAL '1 hour')
                                )
                                - CURRENT_TIMESTAMP
                            )
                        ) / 3600.0
                    )::numeric,
                    2
                ) AS sla_remaining_hours,

                f.facility_name AS facility,
                d.name AS diagnosis

            FROM fraud_cases fc

            INNER JOIN claims c
                ON c.id = fc.claim_id

            LEFT JOIN facilities f
                ON f.id = c.facility_id

            LEFT JOIN diagnosis d
                ON d.id = c.diagnosis_id

            LEFT JOIN fraud_sla_policy sp
                ON sp.priority = fc.priority
                AND sp.is_active = TRUE

            WHERE fc.closed_at IS NULL

            ORDER BY
                CASE
                    WHEN sp.priority IS NULL THEN 5
                    WHEN CURRENT_TIMESTAMP >=
                        fc.created_at
                        + (
                            (
                                sp.sla_hours
                                + sp.critical_hours_after_breach
                            ) * INTERVAL '1 hour'
                        ) THEN 1
                    WHEN CURRENT_TIMESTAMP >
                        fc.created_at
                        + (sp.sla_hours * INTERVAL '1 hour') THEN 2
                    WHEN CURRENT_TIMESTAMP >=
                        fc.created_at
                        + (
                            (
                                sp.sla_hours
                                - sp.warning_hours_before
                            ) * INTERVAL '1 hour'
                        ) THEN 3
                    ELSE 4
                END,
                fc.created_at ASC,
                c.fraud_score DESC

            LIMIT 10
            """
        )
    ).mappings().all()


    session.close()

    return {
        "sla_mode": "PRIORITY_POLICY",
        "legacy_sla_days": sla_days,
        "summary": summary,
        "investigator_performance": investigator_performance,
        "aging_distribution": aging_distribution,
        "oldest_active_cases": oldest_active_cases
    }


# =====================================
# INVESTIGATOR DIRECTORY
# =====================================

@router.get("/cases/investigators")
def get_investigator_directory(
    sla_days: Optional[int] = Query(
        default=None,
        ge=1,
        le=365,
        description="Legacy parameter; SLA sekarang mengikuti fraud_sla_policy."
    )
):

    session = get_session()

    result = session.execute(
        text(
            """
            WITH case_metrics AS (
                SELECT
                    fc.*,
                    sp.priority AS policy_priority,
                    fc.created_at
                        + (sp.sla_hours * INTERVAL '1 hour')
                        AS sla_due_at,
                    fc.created_at
                        + (
                            (
                                sp.sla_hours
                                - sp.warning_hours_before
                            ) * INTERVAL '1 hour'
                        ) AS sla_warning_at,
                    fc.created_at
                        + (
                            (
                                sp.sla_hours
                                + sp.critical_hours_after_breach
                            ) * INTERVAL '1 hour'
                        ) AS sla_critical_at
                FROM fraud_cases fc
                LEFT JOIN fraud_sla_policy sp
                    ON sp.priority = fc.priority
                    AND sp.is_active = TRUE
            ),
            classified AS (
                SELECT
                    *,
                    CASE
                        WHEN policy_priority IS NULL
                        THEN 'NO_POLICY'
                        WHEN closed_at IS NOT NULL
                             AND closed_at <= sla_due_at
                        THEN 'CLOSED_WITHIN_SLA'
                        WHEN closed_at IS NOT NULL
                             AND closed_at > sla_due_at
                        THEN 'CLOSED_BREACHED'
                        WHEN CURRENT_TIMESTAMP >= sla_critical_at
                        THEN 'CRITICAL'
                        WHEN CURRENT_TIMESTAMP > sla_due_at
                        THEN 'BREACHED'
                        WHEN CURRENT_TIMESTAMP >= sla_warning_at
                        THEN 'WARNING'
                        ELSE 'ON_TRACK'
                    END AS sla_status
                FROM case_metrics
            )
            SELECT
                COALESCE(
                    NULLIF(TRIM(assigned_to), ''),
                    'Belum Ditugaskan'
                ) AS investigator,

                COUNT(*) AS total_cases,

                COUNT(*) FILTER (
                    WHERE closed_at IS NULL
                ) AS active_cases,

                COUNT(*) FILTER (
                    WHERE closed_at IS NOT NULL
                ) AS closed_cases,

                COUNT(*) FILTER (
                    WHERE
                        closed_at IS NULL
                        AND sla_status IN ('BREACHED', 'CRITICAL')
                ) AS overdue_cases,

                COUNT(*) FILTER (
                    WHERE
                        closed_at IS NULL
                        AND sla_status = 'WARNING'
                ) AS warning_cases,

                COUNT(*) FILTER (
                    WHERE
                        closed_at IS NULL
                        AND sla_status = 'CRITICAL'
                ) AS critical_cases

            FROM classified

            GROUP BY
                COALESCE(
                    NULLIF(TRIM(assigned_to), ''),
                    'Belum Ditugaskan'
                )

            ORDER BY
                CASE
                    WHEN COALESCE(
                        NULLIF(TRIM(assigned_to), ''),
                        'Belum Ditugaskan'
                    ) = 'Belum Ditugaskan'
                    THEN 0
                    ELSE 1
                END,
                critical_cases DESC,
                overdue_cases DESC,
                active_cases DESC,
                investigator ASC
            """
        )
    ).mappings().all()

    session.close()

    return result


# =====================================
# INVESTIGATOR WORKBENCH
# =====================================

@router.get("/cases/workbench")
def get_investigator_workbench(

    assigned_to: Optional[str] = Query(
        default=None
    ),

    unassigned: bool = Query(
        default=False
    ),

    case_status: Optional[str] = Query(
        default=None
    ),

    priority: Optional[str] = Query(
        default=None
    ),

    search: Optional[str] = Query(
        default=None
    ),

    sla_days: Optional[int] = Query(
        default=None,
        ge=1,
        le=365,
        description="Legacy parameter; SLA sekarang mengikuti fraud_sla_policy."
    ),

    page: int = Query(
        default=1,
        ge=1
    ),

    page_size: int = Query(
        default=10,
        ge=5,
        le=100
    )

):

    session = get_session()

    normalized_status = (
        case_status.strip().upper()
        if case_status
        else None
    )

    normalized_priority = (
        priority.strip().upper()
        if priority
        else None
    )

    normalized_assigned_to = (
        assigned_to.strip()
        if assigned_to
        and assigned_to.strip()
        else None
    )

    search_value = (
        f"%{search.strip()}%"
        if search
        and search.strip()
        else None
    )

    allowed_status = [
        "NEW",
        "REVIEWING",
        "CONFIRMED",
        "CLEARED"
    ]

    allowed_priority = [
        "LOW",
        "NORMAL",
        "MEDIUM",
        "HIGH",
        "URGENT"
    ]

    if (
        normalized_status is not None
        and normalized_status not in allowed_status
    ):
        session.close()
        raise HTTPException(
            status_code=400,
            detail="Status kasus tidak valid"
        )

    if (
        normalized_priority is not None
        and normalized_priority not in allowed_priority
    ):
        session.close()
        raise HTTPException(
            status_code=400,
            detail="Prioritas tidak valid"
        )

    offset = (
        page - 1
    ) * page_size

    params = {
        "assigned_to": normalized_assigned_to,
        "unassigned": unassigned,
        "case_status": normalized_status,
        "priority": normalized_priority,
        "search": search_value,
        "limit": page_size,
        "offset": offset
    }

    where_clause = """
        WHERE
            (
                :unassigned = FALSE
                OR fc.assigned_investigator_id IS NULL
            )
            AND
            (
                :assigned_to IS NULL
                OR LOWER(TRIM(fc.assigned_to))
                   = LOWER(TRIM(:assigned_to))
            )
            AND
            (
                :case_status IS NULL
                OR fc.case_status = :case_status
            )
            AND
            (
                :priority IS NULL
                OR fc.priority = :priority
            )
            AND
            (
                :search IS NULL
                OR c.claim_code ILIKE :search
                OR f.facility_name ILIKE :search
                OR d.name ILIKE :search
                OR fc.assigned_to ILIKE :search
            )
    """

    total = session.execute(
        text(
            f"""
            SELECT COUNT(*)
            FROM fraud_cases fc
            INNER JOIN claims c
                ON c.id = fc.claim_id
            LEFT JOIN facilities f
                ON f.id = c.facility_id
            LEFT JOIN diagnosis d
                ON d.id = c.diagnosis_id
            {where_clause}
            """
        ),
        params
    ).scalar_one()

    summary = session.execute(
        text(
            f"""
            WITH filtered_cases AS (
                SELECT
                    fc.*,
                    sp.priority AS policy_priority,
                    fc.created_at
                        + (sp.sla_hours * INTERVAL '1 hour')
                        AS sla_due_at,
                    fc.created_at
                        + (
                            (
                                sp.sla_hours
                                - sp.warning_hours_before
                            ) * INTERVAL '1 hour'
                        ) AS sla_warning_at,
                    fc.created_at
                        + (
                            (
                                sp.sla_hours
                                + sp.critical_hours_after_breach
                            ) * INTERVAL '1 hour'
                        ) AS sla_critical_at
                FROM fraud_cases fc
                INNER JOIN claims c
                    ON c.id = fc.claim_id
                LEFT JOIN facilities f
                    ON f.id = c.facility_id
                LEFT JOIN diagnosis d
                    ON d.id = c.diagnosis_id
                LEFT JOIN fraud_sla_policy sp
                    ON sp.priority = fc.priority
                    AND sp.is_active = TRUE
                {where_clause}
            ),
            classified AS (
                SELECT
                    *,
                    CASE
                        WHEN policy_priority IS NULL
                        THEN 'NO_POLICY'
                        WHEN closed_at IS NOT NULL
                             AND closed_at <= sla_due_at
                        THEN 'CLOSED_WITHIN_SLA'
                        WHEN closed_at IS NOT NULL
                             AND closed_at > sla_due_at
                        THEN 'CLOSED_BREACHED'
                        WHEN CURRENT_TIMESTAMP >= sla_critical_at
                        THEN 'CRITICAL'
                        WHEN CURRENT_TIMESTAMP > sla_due_at
                        THEN 'BREACHED'
                        WHEN CURRENT_TIMESTAMP >= sla_warning_at
                        THEN 'WARNING'
                        ELSE 'ON_TRACK'
                    END AS sla_status
                FROM filtered_cases
            )
            SELECT
                COUNT(*) AS total_cases,

                COUNT(*) FILTER (
                    WHERE closed_at IS NULL
                ) AS active_cases,

                COUNT(*) FILTER (
                    WHERE closed_at IS NOT NULL
                ) AS closed_cases,

                COUNT(*) FILTER (
                    WHERE
                        closed_at IS NULL
                        AND sla_status IN ('BREACHED', 'CRITICAL')
                ) AS overdue_cases,

                COUNT(*) FILTER (
                    WHERE
                        closed_at IS NULL
                        AND sla_status = 'WARNING'
                ) AS warning_cases,

                COUNT(*) FILTER (
                    WHERE
                        closed_at IS NULL
                        AND sla_status = 'CRITICAL'
                ) AS critical_cases,

                COUNT(*) FILTER (
                    WHERE assigned_investigator_id IS NULL
                ) AS unassigned_cases,

                COUNT(*) FILTER (
                    WHERE sla_status = 'NO_POLICY'
                ) AS no_policy_cases

            FROM classified
            """
        ),
        params
    ).mappings().first()

    items = session.execute(
        text(
            f"""
            SELECT
                fc.id AS case_id,
                fc.claim_id,
                fc.case_status,
                fc.priority,
                fc.assigned_investigator_id,
                fc.assigned_to,
                fc.investigation_result,
                fc.created_at,
                fc.closed_at,
                fc.sla_last_status,
                fc.sla_status_updated_at,
                fc.sla_last_escalated_at,
                c.claim_code,
                c.claim_amount,
                c.fraud_score,
                c.risk_level,
                c.service_date,
                f.facility_name AS facility,
                d.name AS diagnosis,

                ROUND(
                    (
                        EXTRACT(
                            EPOCH FROM (
                                COALESCE(
                                    fc.closed_at,
                                    CURRENT_TIMESTAMP
                                )
                                - fc.created_at
                            )
                        ) / 86400.0
                    )::numeric,
                    2
                ) AS age_days,

                sp.sla_hours,
                sp.warning_hours_before,
                sp.critical_hours_after_breach,

                fc.created_at
                    + (sp.sla_hours * INTERVAL '1 hour')
                    AS sla_due_at,

                fc.created_at
                    + (
                        (
                            sp.sla_hours
                            - sp.warning_hours_before
                        ) * INTERVAL '1 hour'
                    ) AS sla_warning_at,

                fc.created_at
                    + (
                        (
                            sp.sla_hours
                            + sp.critical_hours_after_breach
                        ) * INTERVAL '1 hour'
                    ) AS sla_critical_at,

                CASE
                    WHEN sp.priority IS NULL
                    THEN 'NO_POLICY'

                    WHEN fc.closed_at IS NOT NULL
                         AND fc.closed_at <=
                             fc.created_at
                             + (sp.sla_hours * INTERVAL '1 hour')
                    THEN 'CLOSED_WITHIN_SLA'

                    WHEN fc.closed_at IS NOT NULL
                         AND fc.closed_at >
                             fc.created_at
                             + (sp.sla_hours * INTERVAL '1 hour')
                    THEN 'CLOSED_BREACHED'

                    WHEN CURRENT_TIMESTAMP >=
                        fc.created_at
                        + (
                            (
                                sp.sla_hours
                                + sp.critical_hours_after_breach
                            ) * INTERVAL '1 hour'
                        )
                    THEN 'CRITICAL'

                    WHEN CURRENT_TIMESTAMP >
                        fc.created_at
                        + (sp.sla_hours * INTERVAL '1 hour')
                    THEN 'BREACHED'

                    WHEN CURRENT_TIMESTAMP >=
                        fc.created_at
                        + (
                            (
                                sp.sla_hours
                                - sp.warning_hours_before
                            ) * INTERVAL '1 hour'
                        )
                    THEN 'WARNING'

                    ELSE 'ON_TRACK'
                END AS sla_status,

                CASE
                    WHEN sp.priority IS NULL
                    THEN FALSE
                    WHEN COALESCE(
                        fc.closed_at,
                        CURRENT_TIMESTAMP
                    ) >
                        fc.created_at
                        + (sp.sla_hours * INTERVAL '1 hour')
                    THEN TRUE
                    ELSE FALSE
                END AS sla_breached,

                CASE
                    WHEN
                        fc.closed_at IS NULL
                        AND sp.priority IS NOT NULL
                    THEN ROUND(
                        (
                            EXTRACT(
                                EPOCH FROM (
                                    (
                                        fc.created_at
                                        + (sp.sla_hours * INTERVAL '1 hour')
                                    )
                                    - CURRENT_TIMESTAMP
                                )
                            ) / 3600.0
                        )::numeric,
                        2
                    )
                    ELSE NULL
                END AS sla_remaining_hours

            FROM fraud_cases fc

            INNER JOIN claims c
                ON c.id = fc.claim_id

            LEFT JOIN facilities f
                ON f.id = c.facility_id

            LEFT JOIN diagnosis d
                ON d.id = c.diagnosis_id

            LEFT JOIN fraud_sla_policy sp
                ON sp.priority = fc.priority
                AND sp.is_active = TRUE

            {where_clause}

            ORDER BY
                CASE
                    WHEN fc.closed_at IS NOT NULL THEN 6
                    WHEN sp.priority IS NULL THEN 5
                    WHEN CURRENT_TIMESTAMP >=
                        fc.created_at
                        + (
                            (
                                sp.sla_hours
                                + sp.critical_hours_after_breach
                            ) * INTERVAL '1 hour'
                        ) THEN 1
                    WHEN CURRENT_TIMESTAMP >
                        fc.created_at
                        + (sp.sla_hours * INTERVAL '1 hour') THEN 2
                    WHEN CURRENT_TIMESTAMP >=
                        fc.created_at
                        + (
                            (
                                sp.sla_hours
                                - sp.warning_hours_before
                            ) * INTERVAL '1 hour'
                        ) THEN 3
                    ELSE 4
                END,
                CASE fc.priority
                    WHEN 'URGENT' THEN 1
                    WHEN 'HIGH' THEN 2
                    WHEN 'MEDIUM' THEN 3
                    WHEN 'NORMAL' THEN 4
                    WHEN 'LOW' THEN 5
                    ELSE 6
                END,
                c.fraud_score DESC,
                fc.created_at ASC

            LIMIT :limit
            OFFSET :offset
            """
        ),
        params
    ).mappings().all()

    total_pages = (
        total + page_size - 1
    ) // page_size

    session.close()

    return {
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
            "has_previous": page > 1,
            "has_next": page < total_pages
        },
        "summary": summary,
        "sla_mode": "PRIORITY_POLICY",
        "legacy_sla_days": sla_days
    }


# =====================================
# ASSIGN / REASSIGN / UNASSIGN CASE
# =====================================

@router.patch("/{claim_id}/case/assign")
def assign_fraud_case(
    claim_id: str,
    payload: AssignFraudCaseRequest
):

    session = get_session()


    existing_case = session.execute(
        text(
            """
            SELECT

                id,

                claim_id,

                case_status,

                priority,

                assigned_investigator_id,

                assigned_to,

                investigation_note,

                closed_at,

                created_at

            FROM fraud_cases

            WHERE claim_id = :claim_id

            ORDER BY created_at DESC

            LIMIT 1
            """
        ),
        {
            "claim_id":
                claim_id
        }
    ).mappings().first()


    if not existing_case:

        session.close()

        raise HTTPException(
            status_code=404,
            detail="Fraud case belum dibuat"
        )


    try:

        new_investigator_id, new_assigned_to = (
            resolve_investigator_assignment(
                session,
                payload.investigator_id,
                payload.assigned_to
            )
        )


        old_investigator_id = (
            existing_case[
                "assigned_investigator_id"
            ]
        )


        old_assigned_to = (
            existing_case["assigned_to"]
            if existing_case["assigned_to"]
            else None
        )


        # =====================================
        # NO CHANGE
        # =====================================

        if (
            old_investigator_id
            ==
            new_investigator_id
        ):

            session.close()

            return {
                **existing_case,
                "message":
                    "Tidak ada perubahan investigator."
            }


        # =====================================
        # FASE 4.19 — CAPACITY GUARD
        # Closed cases do not consume active capacity.
        # =====================================

        if (
            new_investigator_id is not None
            and
            existing_case["closed_at"] is None
        ):

            ensure_investigator_capacity(
                session,
                new_investigator_id
            )


        # =====================================
        # UPDATE RELATIONAL ASSIGNMENT
        # =====================================

        result = session.execute(
            text(
                """
                UPDATE fraud_cases

                SET

                    assigned_investigator_id =
                        :assigned_investigator_id,

                    assigned_to =
                        :assigned_to

                WHERE id = :case_id

                RETURNING

                    id,

                    claim_id,

                    case_status,

                    priority,

                    assigned_investigator_id,

                    assigned_to,

                    investigation_note,

                    investigation_result,

                    estimated_loss,

                    confirmed_loss,

                    recovered_amount,

                    conclusion,

                    closed_at,

                    created_at
                """
            ),
            {
                "case_id":
                    existing_case["id"],

                "assigned_investigator_id":
                    new_investigator_id,

                "assigned_to":
                    new_assigned_to
            }
        ).mappings().first()


        # =====================================
        # DETERMINE AUDIT EVENT
        # =====================================

        if (
            old_assigned_to is None
            and
            new_assigned_to is not None
        ):

            event_type = "CASE_ASSIGNED"

            note = (
                "Kasus ditugaskan kepada "
                f"{new_assigned_to}"
            )


        elif (
            old_assigned_to is not None
            and
            new_assigned_to is None
        ):

            event_type = "CASE_UNASSIGNED"

            note = (
                "Penugasan investigator dilepas dari "
                f"{old_assigned_to}"
            )


        else:

            event_type = "CASE_REASSIGNED"

            note = (
                "Investigator diubah dari "
                f"{old_assigned_to} menjadi "
                f"{new_assigned_to}"
            )


        # =====================================
        # AUDIT TRAIL
        # =====================================

        session.execute(
            text(
                """
                INSERT INTO fraud_case_history
                (
                    fraud_case_id,

                    claim_id,

                    event_type,

                    old_status,

                    new_status,

                    old_priority,

                    new_priority,

                    old_assigned_to,

                    new_assigned_to,

                    note,

                    actor
                )
                VALUES
                (
                    :fraud_case_id,

                    :claim_id,

                    :event_type,

                    :old_status,

                    :new_status,

                    :old_priority,

                    :new_priority,

                    :old_assigned_to,

                    :new_assigned_to,

                    :note,

                    :actor
                )
                """
            ),
            {
                "fraud_case_id":
                    result["id"],

                "claim_id":
                    result["claim_id"],

                "event_type":
                    event_type,

                "old_status":
                    existing_case["case_status"],

                "new_status":
                    result["case_status"],

                "old_priority":
                    existing_case["priority"],

                "new_priority":
                    result["priority"],

                "old_assigned_to":
                    old_assigned_to,

                "new_assigned_to":
                    new_assigned_to,

                "note":
                    note,

                "actor":
                    "SYSTEM"
            }
        )


        session.commit()


    except Exception:

        session.rollback()

        session.close()

        raise


    session.close()


    return result


# =====================================
# BULK ASSIGN / REASSIGN / UNASSIGN
# =====================================

@router.patch("/cases/bulk-assign")
def bulk_assign_fraud_cases(
    payload: BulkAssignFraudCasesRequest
):

    session = get_session()


    # =====================================
    # NORMALIZE REQUEST
    # =====================================

    claim_ids = list(
        dict.fromkeys(
            [
                str(claim_id).strip()
                for claim_id in payload.claim_ids
                if str(claim_id).strip()
            ]
        )
    )


    if len(claim_ids) == 0:

        session.close()

        raise HTTPException(
            status_code=400,
            detail="Pilih minimal satu kasus."
        )


    if len(claim_ids) > 100:

        session.close()

        raise HTTPException(
            status_code=400,
            detail=(
                "Maksimal 100 kasus dalam "
                "satu bulk assignment."
            )
        )


    updated_items = []

    unchanged_items = []

    skipped_items = []


    try:

        # =====================================
        # RESOLVE OFFICIAL INVESTIGATOR
        # =====================================

        new_investigator_id, new_assigned_to = (
            resolve_investigator_assignment(
                session,
                payload.investigator_id,
                payload.assigned_to
            )
        )


        # =====================================
        # PROCESS EACH CLAIM
        # =====================================

        for claim_id in claim_ids:


            existing_case = session.execute(
                text(
                    """
                    SELECT

                        id,

                        claim_id,

                        case_status,

                        priority,

                        assigned_investigator_id,

                        assigned_to,

                        investigation_note,

                        closed_at,

                        created_at

                    FROM fraud_cases

                    WHERE claim_id = :claim_id

                    ORDER BY created_at DESC

                    LIMIT 1
                    """
                ),
                {
                    "claim_id":
                        claim_id
                }
            ).mappings().first()


            if not existing_case:

                skipped_items.append({
                    "claim_id":
                        claim_id,

                    "reason":
                        "Fraud case belum dibuat"
                })

                continue


            old_investigator_id = (
                existing_case[
                    "assigned_investigator_id"
                ]
            )


            old_assigned_to = (
                existing_case["assigned_to"]
                if existing_case["assigned_to"]
                else None
            )


            # =====================================
            # NO CHANGE
            # =====================================

            if (
                old_investigator_id
                ==
                new_investigator_id
            ):

                unchanged_items.append({
                    "claim_id":
                        claim_id,

                    "case_id":
                        existing_case["id"],

                    "assigned_investigator_id":
                        old_investigator_id,

                    "assigned_to":
                        old_assigned_to
                })

                continue


            # =====================================
            # FASE 4.19 — CAPACITY GUARD
            #
            # Query dijalankan untuk setiap kasus.
            # Update sebelumnya di transaction yang sama
            # langsung ikut terhitung oleh query berikutnya.
            # =====================================

            if (
                new_investigator_id is not None
                and
                existing_case["closed_at"] is None
            ):

                ensure_investigator_capacity(
                    session,
                    new_investigator_id
                )


            # =====================================
            # UPDATE RELATIONAL ASSIGNMENT
            # =====================================

            result = session.execute(
                text(
                    """
                    UPDATE fraud_cases

                    SET

                        assigned_investigator_id =
                            :assigned_investigator_id,

                        assigned_to =
                            :assigned_to

                    WHERE id = :case_id

                    RETURNING

                        id,

                        claim_id,

                        case_status,

                        priority,

                        assigned_investigator_id,

                        assigned_to,

                        investigation_result,

                        closed_at,

                        created_at
                    """
                ),
                {
                    "case_id":
                        existing_case["id"],

                    "assigned_investigator_id":
                        new_investigator_id,

                    "assigned_to":
                        new_assigned_to
                }
            ).mappings().first()


            # =====================================
            # DETERMINE EVENT
            # =====================================

            if (
                old_assigned_to is None
                and
                new_assigned_to is not None
            ):

                event_type = "CASE_ASSIGNED"

                note = (
                    "Kasus ditugaskan kepada "
                    f"{new_assigned_to}"
                )


            elif (
                old_assigned_to is not None
                and
                new_assigned_to is None
            ):

                event_type = "CASE_UNASSIGNED"

                note = (
                    "Penugasan investigator dilepas dari "
                    f"{old_assigned_to}"
                )


            else:

                event_type = "CASE_REASSIGNED"

                note = (
                    "Investigator diubah dari "
                    f"{old_assigned_to} menjadi "
                    f"{new_assigned_to}"
                )


            # =====================================
            # AUDIT TRAIL
            # =====================================

            session.execute(
                text(
                    """
                    INSERT INTO fraud_case_history
                    (
                        fraud_case_id,

                        claim_id,

                        event_type,

                        old_status,

                        new_status,

                        old_priority,

                        new_priority,

                        old_assigned_to,

                        new_assigned_to,

                        note,

                        actor
                    )
                    VALUES
                    (
                        :fraud_case_id,

                        :claim_id,

                        :event_type,

                        :old_status,

                        :new_status,

                        :old_priority,

                        :new_priority,

                        :old_assigned_to,

                        :new_assigned_to,

                        :note,

                        :actor
                    )
                    """
                ),
                {
                    "fraud_case_id":
                        result["id"],

                    "claim_id":
                        result["claim_id"],

                    "event_type":
                        event_type,

                    "old_status":
                        existing_case["case_status"],

                    "new_status":
                        result["case_status"],

                    "old_priority":
                        existing_case["priority"],

                    "new_priority":
                        result["priority"],

                    "old_assigned_to":
                        old_assigned_to,

                    "new_assigned_to":
                        new_assigned_to,

                    "note":
                        note,

                    "actor":
                        "SUPERVISOR"
                }
            )


            updated_items.append({
                "claim_id":
                    result["claim_id"],

                "case_id":
                    result["id"],

                "old_investigator_id":
                    old_investigator_id,

                "old_assigned_to":
                    old_assigned_to,

                "new_investigator_id":
                    result[
                        "assigned_investigator_id"
                    ],

                "new_assigned_to":
                    result["assigned_to"]
            })


        session.commit()


    except Exception:

        session.rollback()

        session.close()

        raise


    session.close()


    return {

        "requested":
            len(claim_ids),

        "updated":
            len(updated_items),

        "unchanged":
            len(unchanged_items),

        "skipped":
            len(skipped_items),

        "assigned_investigator_id":
            new_investigator_id,

        "assigned_to":
            new_assigned_to,

        "updated_items":
            updated_items,

        "unchanged_items":
            unchanged_items,

        "skipped_items":
            skipped_items

    }


@router.post("/cases/auto-assign")
def auto_assign_fraud_cases(
    payload: AutoAssignFraudCasesRequest
):

    session = get_session()

    claim_ids = list(
        dict.fromkeys(
            [
                str(claim_id).strip()
                for claim_id in payload.claim_ids
                if str(claim_id).strip()
            ]
        )
    )

    if len(claim_ids) == 0:

        session.close()

        raise HTTPException(
            status_code=400,
            detail="Pilih minimal satu kasus."
        )

    if len(claim_ids) > 100:

        session.close()

        raise HTTPException(
            status_code=400,
            detail=(
                "Maksimal 100 kasus dalam "
                "satu auto assignment."
            )
        )

    assigned_items = []
    skipped_items = []

    try:

        for claim_id in claim_ids:

            existing_case = session.execute(
                text(
                    """
                    SELECT
                        id,
                        claim_id,
                        case_status,
                        priority,
                        assigned_investigator_id,
                        assigned_to,
                        closed_at,
                        created_at

                    FROM fraud_cases

                    WHERE claim_id = :claim_id

                    ORDER BY created_at DESC

                    LIMIT 1
                    """
                ),
                {
                    "claim_id":
                        claim_id
                }
            ).mappings().first()

            if not existing_case:

                skipped_items.append({
                    "claim_id":
                        claim_id,
                    "reason":
                        "Fraud case belum dibuat."
                })

                continue

            if existing_case["closed_at"] is not None:

                skipped_items.append({
                    "claim_id":
                        claim_id,
                    "reason":
                        "Kasus sudah ditutup."
                })

                continue

            if (
                existing_case[
                    "assigned_investigator_id"
                ]
                is not None
            ):

                skipped_items.append({
                    "claim_id":
                        claim_id,
                    "reason":
                        (
                            "Kasus sudah memiliki investigator: "
                            f"{existing_case['assigned_to']}."
                        )
                })

                continue

            investigator = (
                select_lowest_load_investigator(
                    session
                )
            )

            if not investigator:

                skipped_items.append({
                    "claim_id":
                        claim_id,
                    "reason":
                        (
                            "Tidak ada investigator aktif "
                            "yang masih memiliki kapasitas."
                        )
                })

                continue


            # Re-check immediately before assignment.
            ensure_investigator_capacity(
                session,
                investigator["id"]
            )


            result = session.execute(
                text(
                    """
                    UPDATE fraud_cases

                    SET
                        assigned_investigator_id =
                            :investigator_id,

                        assigned_to =
                            :assigned_to

                    WHERE id = :case_id

                    RETURNING
                        id,
                        claim_id,
                        case_status,
                        priority,
                        assigned_investigator_id,
                        assigned_to,
                        created_at
                    """
                ),
                {
                    "case_id":
                        existing_case["id"],

                    "investigator_id":
                        investigator["id"],

                    "assigned_to":
                        investigator["full_name"]
                }
            ).mappings().first()

            session.execute(
                text(
                    """
                    INSERT INTO fraud_case_history
                    (
                        fraud_case_id,
                        claim_id,
                        event_type,
                        old_status,
                        new_status,
                        old_priority,
                        new_priority,
                        old_assigned_to,
                        new_assigned_to,
                        note,
                        actor
                    )
                    VALUES
                    (
                        :fraud_case_id,
                        :claim_id,
                        'CASE_AUTO_ASSIGNED',
                        :old_status,
                        :new_status,
                        :old_priority,
                        :new_priority,
                        :old_assigned_to,
                        :new_assigned_to,
                        :note,
                        'SYSTEM_AUTO_ASSIGNMENT'
                    )
                    """
                ),
                {
                    "fraud_case_id":
                        result["id"],

                    "claim_id":
                        result["claim_id"],

                    "old_status":
                        existing_case["case_status"],

                    "new_status":
                        result["case_status"],

                    "old_priority":
                        existing_case["priority"],

                    "new_priority":
                        result["priority"],

                    "old_assigned_to":
                        existing_case["assigned_to"],

                    "new_assigned_to":
                        result["assigned_to"],

                    "note":
                        (
                            "Kasus dialokasikan otomatis kepada "
                            f"{result['assigned_to']} menggunakan "
                            "strategi beban relatif terendah."
                        )
                }
            )

            assigned_items.append({
                "claim_id":
                    result["claim_id"],
                "case_id":
                    result["id"],
                "investigator_id":
                    result["assigned_investigator_id"],
                "assigned_to":
                    result["assigned_to"]
            })

        session.commit()

    except Exception:

        session.rollback()
        session.close()
        raise

    session.close()

    return {
        "requested":
            len(claim_ids),
        "assigned":
            len(assigned_items),
        "skipped":
            len(skipped_items),
        "strategy":
            "LOWEST_RELATIVE_LOAD",
        "assigned_items":
            assigned_items,
        "skipped_items":
            skipped_items
    }

# =====================================
# CLAIM PROFILE DETAIL
# =====================================

@router.get("/{claim_id}")
def get_claim_detail(claim_id:str):

    session=get_session()


    result=session.execute(
        text(
            """
            SELECT

                c.id,

                c.claim_code,

                c.claim_amount,

                c.status,

                c.service_date,

                c.fraud_score,

                c.risk_level,

                c.fraud_reason,


                d.name AS diagnosis,


                f.facility_name AS facility



            FROM claims c


            LEFT JOIN diagnosis d

            ON c.diagnosis_id=d.id


            LEFT JOIN facilities f

            ON c.facility_id=f.id



            WHERE c.id=:id

            """
        ),
        {
            "id":claim_id
        }

    ).mappings().first()


    session.close()


    return result





# =====================================
# CLAIM CLINICAL DETAILS
# =====================================

@router.get("/{claim_id}/details")
def get_claim_details(claim_id:str):

    session=get_session()


    result=session.execute(
        text(
            """
            SELECT

                cd.quantity,

                cd.charged_amount,

                cd.tariff_amount,

                cd.procedure_match,

                cd.medicine_match,

                cd.detail_risk_score,

                cd.anomaly_flag,


                p.name AS procedure,


                m.name AS medicine


            FROM claim_details cd


            LEFT JOIN procedures p

            ON cd.procedure_id=p.id


            LEFT JOIN medicines m

            ON cd.medicine_id=m.id


            WHERE cd.claim_id=:id

            """
        ),
        {
            "id":claim_id
        }

    ).mappings().all()


    session.close()


    return result

# =====================================
# CLAIM RISK BREAKDOWN
# =====================================

@router.get("/{claim_id}/risk-breakdown")
def get_claim_risk_breakdown(claim_id: str):

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT

                factor,

                SUM(score) AS score,

                COUNT(*) AS findings

            FROM claim_fraud_explanation

            WHERE claim_id = :claim_id

            GROUP BY factor

            ORDER BY score DESC
            """
        ),
        {
            "claim_id": claim_id
        }

    ).mappings().all()

    session.close()

    return result



# =====================================
# CLAIM FRAUD EXPLANATION
# =====================================

@router.get("/{claim_id}/explanation")
def get_claim_explanation(claim_id: str):

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT

                id,

                factor,

                score,

                severity,

                description,

                created_at

            FROM claim_fraud_explanation

            WHERE claim_id = :claim_id

            ORDER BY score DESC, created_at ASC
            """
        ),
        {
            "claim_id": claim_id
        }

    ).mappings().all()

    session.close()

    return result

# =====================================
# GET FRAUD CASE
# =====================================

@router.get("/{claim_id}/case")
def get_fraud_case(claim_id: str):

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                fc.id,
                fc.claim_id,
                fc.case_status,
                fc.priority,
                fc.assigned_investigator_id,
                fc.assigned_to,
                fc.investigation_note,
                fc.investigation_result,
                fc.estimated_loss,
                fc.confirmed_loss,
                fc.recovered_amount,
                fc.conclusion,
                fc.closed_at,
                fc.created_at,
                fc.sla_last_status,
                fc.sla_status_updated_at,
                fc.sla_last_escalated_at,

                sp.sla_hours,
                sp.warning_hours_before,
                sp.critical_hours_after_breach,

                fc.created_at
                    + (sp.sla_hours * INTERVAL '1 hour')
                    AS sla_due_at,

                fc.created_at
                    + (
                        (
                            sp.sla_hours
                            - sp.warning_hours_before
                        ) * INTERVAL '1 hour'
                    ) AS sla_warning_at,

                fc.created_at
                    + (
                        (
                            sp.sla_hours
                            + sp.critical_hours_after_breach
                        ) * INTERVAL '1 hour'
                    ) AS sla_critical_at,

                CASE
                    WHEN sp.priority IS NULL
                    THEN 'NO_POLICY'

                    WHEN fc.closed_at IS NOT NULL
                         AND fc.closed_at <=
                             fc.created_at
                             + (sp.sla_hours * INTERVAL '1 hour')
                    THEN 'CLOSED_WITHIN_SLA'

                    WHEN fc.closed_at IS NOT NULL
                         AND fc.closed_at >
                             fc.created_at
                             + (sp.sla_hours * INTERVAL '1 hour')
                    THEN 'CLOSED_BREACHED'

                    WHEN CURRENT_TIMESTAMP >=
                        fc.created_at
                        + (
                            (
                                sp.sla_hours
                                + sp.critical_hours_after_breach
                            ) * INTERVAL '1 hour'
                        )
                    THEN 'CRITICAL'

                    WHEN CURRENT_TIMESTAMP >
                        fc.created_at
                        + (sp.sla_hours * INTERVAL '1 hour')
                    THEN 'BREACHED'

                    WHEN CURRENT_TIMESTAMP >=
                        fc.created_at
                        + (
                            (
                                sp.sla_hours
                                - sp.warning_hours_before
                            ) * INTERVAL '1 hour'
                        )
                    THEN 'WARNING'

                    ELSE 'ON_TRACK'
                END AS sla_status,

                CASE
                    WHEN sp.priority IS NULL
                    THEN FALSE
                    WHEN COALESCE(
                        fc.closed_at,
                        CURRENT_TIMESTAMP
                    ) >
                        fc.created_at
                        + (sp.sla_hours * INTERVAL '1 hour')
                    THEN TRUE
                    ELSE FALSE
                END AS sla_breached,

                CASE
                    WHEN
                        fc.closed_at IS NULL
                        AND sp.priority IS NOT NULL
                    THEN ROUND(
                        (
                            EXTRACT(
                                EPOCH FROM (
                                    (
                                        fc.created_at
                                        + (sp.sla_hours * INTERVAL '1 hour')
                                    )
                                    - CURRENT_TIMESTAMP
                                )
                            ) / 3600.0
                        )::numeric,
                        2
                    )
                    ELSE NULL
                END AS sla_remaining_hours

            FROM fraud_cases fc

            LEFT JOIN fraud_sla_policy sp
                ON sp.priority = fc.priority
                AND sp.is_active = TRUE

            WHERE fc.claim_id = :claim_id

            ORDER BY fc.created_at DESC

            LIMIT 1
            """
        ),
        {
            "claim_id": claim_id
        }
    ).mappings().first()

    session.close()

    return result


# =====================================
# CREATE FRAUD CASE
# =====================================

@router.post("/{claim_id}/case")
def create_fraud_case(
    claim_id: str,
    payload: CreateFraudCaseRequest
):

    session = get_session()


    # =====================================
    # CHECK CLAIM
    # =====================================

    claim = session.execute(
        text(
            """
            SELECT
                id,
                fraud_score,
                risk_level
            FROM claims
            WHERE id = :claim_id
            """
        ),
        {
            "claim_id": claim_id
        }
    ).mappings().first()


    if not claim:

        session.close()

        raise HTTPException(
            status_code=404,
            detail="Claim tidak ditemukan"
        )



    # =====================================
    # CHECK EXISTING CASE
    # =====================================

    existing_case = session.execute(
        text(
            """
            SELECT
                id,
                claim_id,
                case_status,
                priority,
                assigned_to,
                investigation_note,
                created_at
            FROM fraud_cases
            WHERE claim_id = :claim_id
            ORDER BY created_at DESC
            LIMIT 1
            """
        ),
        {
            "claim_id": claim_id
        }
    ).mappings().first()


    if existing_case:

        session.close()

        return existing_case



    # =====================================
    # AUTO PRIORITY
    # =====================================

    fraud_score = claim["fraud_score"] or 0


    if fraud_score >= 70:

        priority = "URGENT"

    elif fraud_score >= 50:

        priority = "HIGH"

    elif fraud_score >= 30:

        priority = "MEDIUM"

    else:

        priority = "LOW"



    # =====================================
    # CREATE CASE
    # =====================================

    result = session.execute(
        text(
            """
            INSERT INTO fraud_cases
            (
                claim_id,
                case_status,
                priority,
                assigned_to,
                investigation_note,
                investigation_result
            )
            VALUES
            (
                :claim_id,
                'NEW',
                :priority,
                :assigned_to,
                :investigation_note,
                'PENDING'
            )
            RETURNING

            id,

            claim_id,

            case_status,

            priority,

            assigned_to,

            investigation_note,

            investigation_result,

            estimated_loss,

            confirmed_loss,

            recovered_amount,

            conclusion,

            closed_at,

            created_at  
            """
        ),
        {
            "claim_id": claim_id,
            "priority": priority,
            "assigned_to": payload.assigned_to,
            "investigation_note":
                payload.investigation_note
                or "Menunggu investigasi"
        }
    ).mappings().first()


    # =====================================
    # CREATE AUDIT TRAIL
    # =====================================

    session.execute(
        text(
            """
            INSERT INTO fraud_case_history
            (
                fraud_case_id,
                claim_id,
                event_type,

                old_status,
                new_status,

                old_priority,
                new_priority,

                old_assigned_to,
                new_assigned_to,

                note,
                actor
            )
            VALUES
            (
                :fraud_case_id,
                :claim_id,
                'CASE_CREATED',

                NULL,
                :new_status,

                NULL,
                :new_priority,

                NULL,
                :new_assigned_to,

                :note,
                :actor
            )
            """
        ),
        {
            "fraud_case_id":
                result["id"],

            "claim_id":
                result["claim_id"],

            "new_status":
                result["case_status"],

            "new_priority":
                result["priority"],

            "new_assigned_to":
                result["assigned_to"],

            "note":
                result["investigation_note"],

            "actor":
                result["assigned_to"] or "SYSTEM"
        }
    )


    # Initialize persistent SLA monitoring state
    # and create SLA_MONITORING_STARTED audit event.
    sync_sla_escalation_state(
        session,
        claim_id=result["claim_id"]
    )


    session.commit()

    session.close()


    return result
# =====================================
# UPDATE FRAUD CASE
# =====================================

@router.patch("/{claim_id}/case")
def update_fraud_case(
    claim_id: str,
    payload: UpdateFraudCaseRequest
):

    session = get_session()


    # =====================================
    # GET EXISTING CASE
    # =====================================

    existing_case = session.execute(
        text(
            """
            SELECT

                id,

                claim_id,

                case_status,

                priority,

                assigned_to,

                investigation_note,

                investigation_result,

                estimated_loss,

                confirmed_loss,

                recovered_amount,

                conclusion,

                closed_at,

                created_at

            FROM fraud_cases

            WHERE claim_id = :claim_id

            ORDER BY created_at DESC

            LIMIT 1
            """
        ),
        {
            "claim_id": claim_id
        }
    ).mappings().first()


    if not existing_case:

        session.close()

        raise HTTPException(
            status_code=404,
            detail="Fraud case belum dibuat"
        )


    # =====================================
    # NORMALIZE INPUT
    # =====================================

    case_status = (
        payload.case_status.strip().upper()
        if payload.case_status
        else None
    )


    priority = (
        payload.priority.strip().upper()
        if payload.priority
        else None
    )


    investigation_result = (
        payload.investigation_result.strip().upper()
        if payload.investigation_result
        else None
    )


    # =====================================
    # VALIDATE STATUS
    # =====================================

    allowed_status = [
        "NEW",
        "REVIEWING",
        "CONFIRMED",
        "CLEARED"
    ]


    if (
        case_status is not None
        and
        case_status not in allowed_status
    ):

        session.close()

        raise HTTPException(
            status_code=400,
            detail=(
                "Case status tidak valid. "
                "Gunakan NEW, REVIEWING, "
                "CONFIRMED, atau CLEARED."
            )
        )


    # =====================================
    # VALIDATE PRIORITY
    # =====================================

    allowed_priority = [
        "LOW",
        "NORMAL",
        "MEDIUM",
        "HIGH",
        "URGENT"
    ]


    if (
        priority is not None
        and
        priority not in allowed_priority
    ):

        session.close()

        raise HTTPException(
            status_code=400,
            detail=(
                "Priority tidak valid. "
                "Gunakan LOW, NORMAL, MEDIUM, "
                "HIGH, atau URGENT."
            )
        )


    # =====================================
    # VALIDATE INVESTIGATION RESULT
    # =====================================

    allowed_results = [
        "PENDING",
        "FRAUD_CONFIRMED",
        "NOT_FRAUD",
        "INCONCLUSIVE"
    ]


    if (
        investigation_result is not None
        and
        investigation_result not in allowed_results
    ):

        session.close()

        raise HTTPException(
            status_code=400,
            detail=(
                "Hasil investigasi tidak valid. "
                "Gunakan PENDING, "
                "FRAUD_CONFIRMED, "
                "NOT_FRAUD, atau INCONCLUSIVE."
            )
        )


    # =====================================
    # VALIDATE FINANCIAL VALUES
    # =====================================

    if (
        payload.estimated_loss is not None
        and
        payload.estimated_loss < 0
    ):

        session.close()

        raise HTTPException(
            status_code=400,
            detail="Estimasi kerugian tidak boleh negatif"
        )


    if (
        payload.confirmed_loss is not None
        and
        payload.confirmed_loss < 0
    ):

        session.close()

        raise HTTPException(
            status_code=400,
            detail="Kerugian terkonfirmasi tidak boleh negatif"
        )


    if (
        payload.recovered_amount is not None
        and
        payload.recovered_amount < 0
    ):

        session.close()

        raise HTTPException(
            status_code=400,
            detail="Nilai pemulihan tidak boleh negatif"
        )


    # =====================================
    # UPDATE CASE
    # =====================================

    result = session.execute(
        text(
            """
            UPDATE fraud_cases

            SET

                case_status =

                    CASE

                        WHEN :investigation_result =
                             'FRAUD_CONFIRMED'
                        THEN 'CONFIRMED'

                        WHEN :investigation_result =
                             'NOT_FRAUD'
                        THEN 'CLEARED'

                        WHEN :investigation_result =
                             'INCONCLUSIVE'
                        THEN 'REVIEWING'

                        WHEN :investigation_result =
                             'PENDING'
                        THEN 'REVIEWING'

                        ELSE
                            COALESCE(
                                :case_status,
                                case_status
                            )

                    END,


                priority =

                    COALESCE(
                        :priority,
                        priority
                    ),


                assigned_to =

                    COALESCE(
                        :assigned_to,
                        assigned_to
                    ),


                investigation_note =

                    COALESCE(
                        :investigation_note,
                        investigation_note
                    ),


                investigation_result =

                    COALESCE(
                        :investigation_result,
                        investigation_result
                    ),


                estimated_loss =

                    COALESCE(
                        :estimated_loss,
                        estimated_loss
                    ),


                confirmed_loss =

                    COALESCE(
                        :confirmed_loss,
                        confirmed_loss
                    ),


                recovered_amount =

                    COALESCE(
                        :recovered_amount,
                        recovered_amount
                    ),


                conclusion =

                    COALESCE(
                        :conclusion,
                        conclusion
                    ),


                closed_at =

                    CASE

                        WHEN
                            COALESCE(
                                :investigation_result,
                                investigation_result
                            )
                            IN (
                                'FRAUD_CONFIRMED',
                                'NOT_FRAUD'
                            )

                        THEN
                            COALESCE(
                                closed_at,
                                CURRENT_TIMESTAMP
                            )


                        WHEN
                            :investigation_result
                            IN (
                                'PENDING',
                                'INCONCLUSIVE'
                            )

                        THEN NULL


                        ELSE closed_at

                    END


            WHERE id = :case_id


            RETURNING

                id,

                claim_id,

                case_status,

                priority,

                assigned_to,

                investigation_note,

                investigation_result,

                estimated_loss,

                confirmed_loss,

                recovered_amount,

                conclusion,

                closed_at,

                created_at
            """
        ),
        {

            "case_id":
                existing_case["id"],

            "case_status":
                case_status,

            "priority":
                priority,

            "assigned_to":
                payload.assigned_to,

            "investigation_note":
                payload.investigation_note,

            "investigation_result":
                investigation_result,

            "estimated_loss":
                payload.estimated_loss,

            "confirmed_loss":
                payload.confirmed_loss,

            "recovered_amount":
                payload.recovered_amount,

            "conclusion":
                payload.conclusion

        }
    ).mappings().first()


    # =====================================
    # DETERMINE AUDIT EVENT
    # =====================================

    outcome_changed = (

        investigation_result is not None

        or
        payload.estimated_loss is not None

        or
        payload.confirmed_loss is not None

        or
        payload.recovered_amount is not None

        or
        payload.conclusion is not None

    )


    if outcome_changed:

        event_type = (
            "INVESTIGATION_RESULT_UPDATED"
        )

    else:

        event_type = (
            "CASE_UPDATED"
        )


    # =====================================
    # BUILD AUDIT NOTE
    # =====================================

    audit_notes = []


    if investigation_result is not None:

        audit_notes.append(
            "Hasil investigasi: "
            f"{result['investigation_result']}"
        )


    if payload.estimated_loss is not None:

        audit_notes.append(
            "Estimasi kerugian: "
            f"{result['estimated_loss']}"
        )


    if payload.confirmed_loss is not None:

        audit_notes.append(
            "Kerugian terkonfirmasi: "
            f"{result['confirmed_loss']}"
        )


    if payload.recovered_amount is not None:

        audit_notes.append(
            "Nilai pemulihan: "
            f"{result['recovered_amount']}"
        )


    if payload.conclusion is not None:

        audit_notes.append(
            "Kesimpulan: "
            f"{result['conclusion']}"
        )


    if payload.investigation_note is not None:

        audit_notes.append(
            "Catatan: "
            f"{result['investigation_note']}"
        )


    audit_note = (
        " | ".join(audit_notes)
        if audit_notes
        else result["investigation_note"]
    )


    # =====================================
    # CREATE AUDIT TRAIL
    # =====================================

    session.execute(
        text(
            """
            INSERT INTO fraud_case_history
            (
                fraud_case_id,

                claim_id,

                event_type,

                old_status,

                new_status,

                old_priority,

                new_priority,

                old_assigned_to,

                new_assigned_to,

                note,

                actor
            )
            VALUES
            (
                :fraud_case_id,

                :claim_id,

                :event_type,

                :old_status,

                :new_status,

                :old_priority,

                :new_priority,

                :old_assigned_to,

                :new_assigned_to,

                :note,

                :actor
            )
            """
        ),
        {

            "fraud_case_id":
                result["id"],

            "claim_id":
                result["claim_id"],

            "event_type":
                event_type,

            "old_status":
                existing_case["case_status"],

            "new_status":
                result["case_status"],

            "old_priority":
                existing_case["priority"],

            "new_priority":
                result["priority"],

            "old_assigned_to":
                existing_case["assigned_to"],

            "new_assigned_to":
                result["assigned_to"],

            "note":
                audit_note,

            "actor":
                result["assigned_to"]
                or existing_case["assigned_to"]
                or "SYSTEM"

        }
    )


    # Re-evaluate SLA immediately when priority,
    # investigation result, or closed_at changes.
    sync_sla_escalation_state(
        session,
        claim_id=result["claim_id"]
    )


    session.commit()

    session.close()


    return result
# =====================================
# FRAUD CASE HISTORY / AUDIT TRAIL
# =====================================

@router.get("/{claim_id}/case/history")
def get_fraud_case_history(claim_id: str):

    session = get_session()


    result = session.execute(
        text(
            """
            SELECT

                id,

                fraud_case_id,

                claim_id,

                event_type,

                old_status,

                new_status,

                old_priority,

                new_priority,

                old_assigned_to,

                new_assigned_to,

                note,

                actor,

                created_at

            FROM fraud_case_history

            WHERE claim_id = :claim_id

            ORDER BY created_at ASC
            """
        ),
        {
            "claim_id": claim_id
        }

    ).mappings().all()


    session.close()


    return result

