from sqlalchemy.orm import DeclarativeBase

from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, DateTime, Date, func
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    dob: Mapped[Optional[datetime]] = mapped_column("date_of_birth", Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )