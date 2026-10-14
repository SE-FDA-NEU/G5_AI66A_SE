"""/api/categories: the kinds of spending and of money received (BR6)."""

from fastapi import APIRouter

from app.core.deps import SIGN_IN_AGAIN, CurrentUser, DbSession
from app.schemas.error import ErrorOut
from app.schemas.transaction import CategoryOut
from app.services import category_service

router = APIRouter(prefix="/categories", tags=["transactions"])


@router.get(
    "",
    response_model=list[CategoryOut],
    summary="The 11 categories, kinds of spending first (US03)",
    responses={401: {"model": ErrorOut, "description": f'"{SIGN_IN_AGAIN}"'}},
)
def list_categories(db: DbSession, _user: CurrentUser) -> list[CategoryOut]:
    return [CategoryOut.model_validate(c) for c in category_service.list_categories(db)]
