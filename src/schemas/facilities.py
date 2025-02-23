from pydantic import BaseModel, ConfigDict


class Facility(BaseModel):
    title: str

class FacilityGet(Facility):
    id: int

    model_config = ConfigDict(from_attributes=True)
