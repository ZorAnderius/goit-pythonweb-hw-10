from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date

from src.database.models import Contact
from src.repository.contacts import ContactsRepository
from src.schemas import ContactsModel, UpdateContactModel


class ContactsServices:
    def __init__(self, db: AsyncSession):
        self.repository = ContactsRepository(db)

    async def get_contacts(self,
                           skip: Optional[int] = 0,
                           limit: Optional[int] = 10,
                           first_name: Optional[str] = None,
                           last_name: Optional[str] = None,
                           email: Optional[str] = None) -> List[Contact]:
        return await self.repository.get_contacts(skip, limit, first_name, last_name, email)

    async def get_contact_by_id(self, contact_id: int):
        return await self.repository.get_contact_by_id(contact_id)

    async def create_contact(self, body: ContactsModel) -> Contact:
        return await self.repository.create_contact(body)

    async def update_contact(self, contact_id: int, body: UpdateContactModel) -> Contact:
        return await self.repository.update_contact(contact_id, body)

    async def delete_contact(self, contact_id: int):
        return await self.repository.delete_contact(contact_id)

    async def get_contacts_for_weekly_birthday(self, birthday_date: Optional[date]) -> List[Contact]:
        return await self.repository.get_contacts_for_weekly_birthday(birthday_date)