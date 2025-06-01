from src.schemas.hotels import Hotel


async def test_add_hotel(db, setup_database):
    hotel_data = Hotel(title="OnlyOneStar", location="Anapa")
    await db.hotels.add(data=hotel_data)
    await db.commit()

