"""/api/debts: money borrowed and lent, until it is paid back (US13)."""

from fastapi import APIRouter, Response, status

from app.core.deps import SIGN_IN_AGAIN, CurrentUser, DbSession
from app.schemas.debt import DebtIn, DebtListOut, DebtOut
from app.schemas.error import ErrorOut
from app.services import debt_service, transaction_service
from app.services.debt_service import DebtView

router = APIRouter(prefix="/debts", tags=["debts"])

NOT_SIGNED_IN = {401: {"model": ErrorOut, "description": f'"{SIGN_IN_AGAIN}"'}}
NOT_FOUND = {
    404: {
        "model": ErrorOut,
        "description": f'"{debt_service.DEBT_NOT_FOUND}": no such id, or another account\'s (BR4)',
    }
}


def debt_out(view: DebtView) -> DebtOut:
    debt = view.debt
    return DebtOut(
        id=debt.id,
        direction=debt.direction,
        person=debt.person,
        amount=debt.amount,
        note=debt.note,
        started_on=debt.started_on,
        due_on=debt.due_on,
        settled_on=debt.settled_on,
        overdue=view.overdue,
    )


@router.get(
    "",
    response_model=DebtListOut,
    summary="Every debt, open ones first, and what you owe and are owed (US13)",
    responses=NOT_SIGNED_IN,
)
def list_debts(db: DbSession, user: CurrentUser) -> DebtListOut:
    debts = debt_service.list_debts(db, user.id)
    return DebtListOut(
        items=[debt_out(view) for view in debts.items], owe=debts.owe, owed=debts.owed
    )


@router.post(
    "",
    response_model=DebtOut,
    status_code=status.HTTP_201_CREATED,
    summary="Write down one debt or loan (US13)",
    responses={
        **NOT_SIGNED_IN,
        422: {
            "model": ErrorOut,
            "description": (
                f'"{debt_service.PERSON_LENGTH}" (BR13) · '
                f'"{transaction_service.AMOUNT_NOT_POSITIVE}" (BR5) · '
                f'"{transaction_service.DATE_IN_FUTURE}" (BR11) · '
                f'"{debt_service.DUE_BEFORE_START}" (BR13)'
            ),
        },
    },
)
def add_debt(payload: DebtIn, db: DbSession, user: CurrentUser) -> DebtOut:
    return debt_out(debt_service.add_debt(db, user.id, **payload.model_dump()))


@router.post(
    "/{debt_id}/settle",
    response_model=DebtOut,
    summary="Mark a debt paid back today (US13, BR14)",
    responses={
        **NOT_SIGNED_IN,
        **NOT_FOUND,
        409: {"model": ErrorOut, "description": f'"{debt_service.ALREADY_SETTLED}" (BR14)'},
    },
)
def settle_debt(debt_id: int, db: DbSession, user: CurrentUser) -> DebtOut:
    return debt_out(debt_service.settle_debt(db, user.id, debt_id))


@router.delete(
    "/{debt_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a debt written down by mistake (US13)",
    responses={**NOT_SIGNED_IN, **NOT_FOUND},
)
def remove_debt(debt_id: int, db: DbSession, user: CurrentUser) -> Response:
    debt_service.remove_debt(db, user.id, debt_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
