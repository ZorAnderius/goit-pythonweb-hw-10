from typing import List, Optional
from datetime import date, timedelta
from calendar import monthrange

from sqlalchemy import select, extract, asc
from sqlalchemy.sql import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas import ContactsModel


class ContactsRepository:
    def __init__(self,session: AsyncSession):
        self.session = session

    async def get_contacts(self,
                           skip: Optional[int] = 0,
                           limit: Optional[int] = 10,
                           first_name: Optional[str] = None,
                           last_name: Optional[str] = None,
                           email: Optional[str] = None) -> List[Contact]:
        query = select(Contact).offset(skip).limit(limit)
        if first_name:
            query = query.where(Contact.first_name.ilike(f"%{first_name}%"))
        if last_name:
            query = query.where(Contact.last_name.ilike(f"%{last_name}%"))
        if email:
            query = query.where(Contact.email.ilike(f"%{email}%"))

        contacts = await self.session.execute(query)
        return list(contacts.scalars().all())

    async def get_contact_by_id(self, contact_id: int) -> Contact:
        query = select(Contact).where(Contact.id == contact_id)
        contact = await self.session.execute(query)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactsModel) -> Contact:
        contact = Contact(**body.model_dump(exclude_unset=True))
        self.session.add(contact)
        await self.session.commit()
        await self.session.refresh(contact)
        return contact

    async def update_contact(self, contact_id: int, body: ContactsModel) -> Contact:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            for key, value in body.model_dump(exclude_unset=True).items():
                setattr(contact, key, value)
        await self.session.commit()
        await self.session.refresh(contact)
        return contact

    async def delete_contact(self, contact_id: int):
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.session.delete(contact)
            await self.session.commit()
        return contact

    async def get_contacts_for_weekly_birthday(self, birthday_date: Optional[date]):
        today = birthday_date
        last_day_of_current_month = date(today.year, today.month, monthrange(today.year, today.month)[1])
        days_until_end_of_month = (last_day_of_current_month - today).days
        if days_until_end_of_month < 7:
            next_month = today.month + 1
            if today.month == 12:
                next_year = today.year + 1
                next_month = 1
            else:
                next_year = today.year
            first_day_of_next_month = date(next_year, next_month, 1)
            end_day_of_rang_month = date(next_year, next_month, (7-days_until_end_of_month))

            query = select(Contact).where(
                or_(
                    and_(
                        extract('month', Contact.dob) == today.month,
                        extract('day', Contact.dob) >= today.day,
                        extract('day', Contact.dob) <= last_day_of_current_month.day,
                    ),

                    and_(
                        extract('month', Contact.dob) == next_month,
                        extract('day', Contact.dob) >= first_day_of_next_month.day,
                        extract('day', Contact.dob) <= end_day_of_rang_month.day,
                    )
                )
            )
        else:
            query = select(Contact).where(
                and_(
                    extract('month', Contact.dob) == today.month,
                    extract('day', Contact.dob) >= today.day,
                    extract('day', Contact.dob) <= (today + timedelta(days=7)).day,
                )
            )

        contacts = await self.session.execute(query)
        return contacts.scalars().all()

