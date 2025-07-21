from src.exceptions import ObjectAlreadyExistsException, FacilityAlreadyExistsException
from src.schemas.facilities import Facility
from src.services.base import BaseService


class FacilitiesService(BaseService):

    async def get_facilities(self):
        return await self.db.facilities.get_all()

    async def add_facilities(self, title: Facility):
        try:
            facility = await self.db.facilities.add(data=title)
            await self.db.commit()
            return facility
        except ObjectAlreadyExistsException:
            raise FacilityAlreadyExistsException

