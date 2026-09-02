from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, false

class SoftDeleteMixin:
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, 
        default=False, 
        nullable=False, 
        server_default=false()
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), 
        default=None, 
        nullable=True
    )