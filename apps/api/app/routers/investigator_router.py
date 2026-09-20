from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import text
from pydantic import BaseModel
from typing import Optional

from database import get_session


router = APIRouter(
    prefix="/investigators",
    tags=["Investigators"]
)


# =====================================
# REQUEST MODELS
# =====================================

class CreateInvestigatorRequest(BaseModel):
    employee_code: Optional[str] = None
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    role: str = "INVESTIGATOR"
    unit: Optional[str] = None
    status: str = "ACTIVE"
    max_active_cases: int = 20


class UpdateInvestigatorRequest(BaseModel):
    employee_code: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    unit: Optional[str] = None
    status: Optional[str] = None
    max_active_cases: Optional[int] = None


def normalize_role(value: Optional[str]):
    if value is None:
        return None

    result = value.strip().upper()

    if result not in [
        "INVESTIGATOR",
        "SUPERVISOR",
        "ANALYST"
    ]:
        raise HTTPException(
            status_code=400,
            detail="Role tidak valid."
        )

    return result


def normalize_status(value: Optional[str]):
    if value is None:
        return None

    result = value.strip().upper()

    if result not in [
        "ACTIVE",
        "INACTIVE"
    ]:
        raise HTTPException(
            status_code=400,
            detail="Status tidak valid."
        )

    return result


# =====================================
# ACTIVE INVESTIGATORS
# =====================================

@router.get("/active")
def get_active_investigators():

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                iu.id,
                iu.employee_code,
                iu.full_name,
                iu.email,
                iu.phone,
                iu.role,
                iu.unit,
                iu.status,
                iu.max_active_cases,

                COUNT(fc.id) FILTER (
                    WHERE fc.closed_at IS NULL
                ) AS active_cases,

                COUNT(fc.id) FILTER (
                    WHERE fc.closed_at IS NOT NULL
                ) AS closed_cases

            FROM investigator_users iu

            LEFT JOIN fraud_cases fc
                ON fc.assigned_investigator_id = iu.id

            WHERE iu.status = 'ACTIVE'

            GROUP BY
                iu.id,
                iu.employee_code,
                iu.full_name,
                iu.email,
                iu.phone,
                iu.role,
                iu.unit,
                iu.status,
                iu.max_active_cases

            ORDER BY
                CASE iu.role
                    WHEN 'SUPERVISOR' THEN 1
                    WHEN 'INVESTIGATOR' THEN 2
                    WHEN 'ANALYST' THEN 3
                    ELSE 4
                END,
                iu.full_name ASC
            """
        )
    ).mappings().all()

    session.close()

    return result


# =====================================
# LIST INVESTIGATORS
# =====================================

@router.get("")
def get_investigators(
    search: Optional[str] = Query(default=None),
    role: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=5, le=100)
):

    session = get_session()

    role_value = normalize_role(role) if role else None
    status_value = normalize_status(status) if status else None

    search_value = (
        f"%{search.strip()}%"
        if search and search.strip()
        else None
    )

    offset = (page - 1) * page_size

    params = {
        "search": search_value,
        "role": role_value,
        "status": status_value,
        "limit": page_size,
        "offset": offset
    }

    where_clause = """
        WHERE
            (
                :search IS NULL
                OR iu.full_name ILIKE :search
                OR iu.employee_code ILIKE :search
                OR iu.email ILIKE :search
                OR iu.unit ILIKE :search
            )
            AND
            (
                :role IS NULL
                OR iu.role = :role
            )
            AND
            (
                :status IS NULL
                OR iu.status = :status
            )
    """

    total = session.execute(
        text(
            f"""
            SELECT COUNT(*)
            FROM investigator_users iu
            {where_clause}
            """
        ),
        params
    ).scalar_one()

    items = session.execute(
        text(
            f"""
            SELECT
                iu.id,
                iu.employee_code,
                iu.full_name,
                iu.email,
                iu.phone,
                iu.role,
                iu.unit,
                iu.status,
                iu.max_active_cases,
                iu.created_at,
                iu.updated_at,

                COUNT(fc.id) AS total_cases,

                COUNT(fc.id) FILTER (
                    WHERE fc.closed_at IS NULL
                ) AS active_cases,

                COUNT(fc.id) FILTER (
                    WHERE fc.closed_at IS NOT NULL
                ) AS closed_cases

            FROM investigator_users iu

            LEFT JOIN fraud_cases fc
                ON fc.assigned_investigator_id = iu.id

            {where_clause}

            GROUP BY
                iu.id,
                iu.employee_code,
                iu.full_name,
                iu.email,
                iu.phone,
                iu.role,
                iu.unit,
                iu.status,
                iu.max_active_cases,
                iu.created_at,
                iu.updated_at

            ORDER BY
                iu.status ASC,
                iu.full_name ASC

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
        }
    }


# =====================================
# CREATE INVESTIGATOR
# =====================================

@router.post("")
def create_investigator(
    payload: CreateInvestigatorRequest
):

    session = get_session()

    full_name = payload.full_name.strip()

    if not full_name:
        session.close()

        raise HTTPException(
            status_code=400,
            detail="Nama investigator wajib diisi."
        )

    role = normalize_role(payload.role)
    status = normalize_status(payload.status)

    if payload.max_active_cases < 0:
        session.close()

        raise HTTPException(
            status_code=400,
            detail="Maksimal kasus aktif tidak boleh negatif."
        )

    duplicate = session.execute(
        text(
            """
            SELECT id
            FROM investigator_users
            WHERE LOWER(TRIM(full_name)) = LOWER(TRIM(:full_name))
            LIMIT 1
            """
        ),
        {
            "full_name": full_name
        }
    ).first()

    if duplicate:
        session.close()

        raise HTTPException(
            status_code=409,
            detail="Nama investigator sudah terdaftar."
        )

    result = session.execute(
        text(
            """
            INSERT INTO investigator_users
            (
                employee_code,
                full_name,
                email,
                phone,
                role,
                unit,
                status,
                max_active_cases
            )
            VALUES
            (
                :employee_code,
                :full_name,
                :email,
                :phone,
                :role,
                :unit,
                :status,
                :max_active_cases
            )
            RETURNING *
            """
        ),
        {
            "employee_code":
                payload.employee_code.strip()
                if payload.employee_code else None,

            "full_name": full_name,

            "email":
                payload.email.strip()
                if payload.email else None,

            "phone":
                payload.phone.strip()
                if payload.phone else None,

            "role": role,

            "unit":
                payload.unit.strip()
                if payload.unit else None,

            "status": status,

            "max_active_cases":
                payload.max_active_cases
        }
    ).mappings().first()

    session.commit()
    session.close()

    return result

@router.get("/capacity")
def get_investigator_capacity():

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                iu.id,
                iu.employee_code,
                iu.full_name,
                iu.role,
                iu.unit,
                iu.status,
                iu.max_active_cases,

                COUNT(fc.id) FILTER (
                    WHERE fc.closed_at IS NULL
                ) AS active_cases,

                GREATEST(
                    iu.max_active_cases
                    -
                    COUNT(fc.id) FILTER (
                        WHERE fc.closed_at IS NULL
                    ),
                    0
                ) AS available_capacity,

                CASE
                    WHEN iu.max_active_cases <= 0
                    THEN 100.00
                    ELSE ROUND(
                        (
                            COUNT(fc.id) FILTER (
                                WHERE fc.closed_at IS NULL
                            )::numeric
                            /
                            iu.max_active_cases::numeric
                        ) * 100,
                        2
                    )
                END AS utilization_percent,

                CASE
                    WHEN
                        COUNT(fc.id) FILTER (
                            WHERE fc.closed_at IS NULL
                        ) > iu.max_active_cases
                    THEN 'OVER_CAPACITY'

                    WHEN
                        iu.max_active_cases <= 0
                        OR
                        COUNT(fc.id) FILTER (
                            WHERE fc.closed_at IS NULL
                        ) >= iu.max_active_cases
                    THEN 'FULL'

                    WHEN
                        (
                            COUNT(fc.id) FILTER (
                                WHERE fc.closed_at IS NULL
                            )::numeric
                            /
                            NULLIF(
                                iu.max_active_cases,
                                0
                            )::numeric
                        ) >= 0.80
                    THEN 'NEAR_LIMIT'

                    ELSE 'AVAILABLE'
                END AS capacity_status

            FROM investigator_users iu

            LEFT JOIN fraud_cases fc
                ON fc.assigned_investigator_id = iu.id

            WHERE iu.role = 'INVESTIGATOR'

            GROUP BY
                iu.id,
                iu.employee_code,
                iu.full_name,
                iu.role,
                iu.unit,
                iu.status,
                iu.max_active_cases

            ORDER BY
                CASE
                    WHEN iu.status = 'ACTIVE'
                    THEN 0
                    ELSE 1
                END,
                active_cases ASC,
                iu.full_name ASC
            """
        )
    ).mappings().all()

    session.close()

    return result


# =====================================
# UPDATE INVESTIGATOR
# =====================================

@router.patch("/{investigator_id}")
def update_investigator(
    investigator_id: str,
    payload: UpdateInvestigatorRequest
):

    session = get_session()

    existing = session.execute(
        text(
            """
            SELECT *
            FROM investigator_users
            WHERE id = :id
            """
        ),
        {
            "id": investigator_id
        }
    ).mappings().first()

    if not existing:
        session.close()

        raise HTTPException(
            status_code=404,
            detail="Investigator tidak ditemukan."
        )

    role = (
        normalize_role(payload.role)
        if payload.role is not None
        else None
    )

    status = (
        normalize_status(payload.status)
        if payload.status is not None
        else None
    )

    if (
        payload.max_active_cases is not None
        and payload.max_active_cases < 0
    ):
        session.close()

        raise HTTPException(
            status_code=400,
            detail="Maksimal kasus aktif tidak boleh negatif."
        )

    full_name = (
        payload.full_name.strip()
        if payload.full_name is not None
        else None
    )

    result = session.execute(
        text(
            """
            UPDATE investigator_users
            SET
                employee_code = COALESCE(:employee_code, employee_code),
                full_name = COALESCE(:full_name, full_name),
                email = COALESCE(:email, email),
                phone = COALESCE(:phone, phone),
                role = COALESCE(:role, role),
                unit = COALESCE(:unit, unit),
                status = COALESCE(:status, status),
                max_active_cases = COALESCE(
                    :max_active_cases,
                    max_active_cases
                ),
                updated_at = CURRENT_TIMESTAMP
            WHERE id = :id
            RETURNING *
            """
        ),
        {
            "id": investigator_id,

            "employee_code":
                payload.employee_code.strip()
                if payload.employee_code else None,

            "full_name": full_name,

            "email":
                payload.email.strip()
                if payload.email else None,

            "phone":
                payload.phone.strip()
                if payload.phone else None,

            "role": role,

            "unit":
                payload.unit.strip()
                if payload.unit else None,

            "status": status,

            "max_active_cases":
                payload.max_active_cases
        }
    ).mappings().first()

    # Sinkronkan legacy assigned_to bila nama berubah
    if full_name is not None:

        session.execute(
            text(
                """
                UPDATE fraud_cases
                SET assigned_to = :full_name
                WHERE assigned_investigator_id = :id
                """
            ),
            {
                "id": investigator_id,
                "full_name": full_name
            }
        )

    session.commit()
    session.close()

    return result
