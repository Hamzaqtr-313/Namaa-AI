from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_tenant_db
from app.models.conversation import Conversation
from app.models.task import Task
from app.models.user import User
from app.schemas.common import SuccessEnvelope

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/today", response_model=SuccessEnvelope[dict])
async def today(
    db: AsyncSession = Depends(get_tenant_db),
    _current_user: User = Depends(get_current_user),
) -> SuccessEnvelope[dict]:
    """"What needs attention today" — empty in a fresh tenant, per Phase 0 exit criteria."""
    pending_approvals = await db.scalar(
        select(func.count()).select_from(Conversation).where(Conversation.status == "pending_approval")
    )
    open_tasks = await db.scalar(
        select(func.count()).select_from(Task).where(Task.status.in_(["pending", "in_progress"]))
    )
    return SuccessEnvelope(
        data={
            "pending_approvals": pending_approvals or 0,
            "open_tasks": open_tasks or 0,
            "unassigned_conversations": 0,
        }
    )
