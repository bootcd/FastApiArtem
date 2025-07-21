
from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsBookedException, WrongBookingDatesExceptions, \
    RoomNotFoundException, RoomNotFoundHTTPException, WrongBookingDatesHTTPException, AllRoomsBookedHTTPException
from src.schemas.bookings import Booking, BookingPost
from src.services.bookings import BookingsService

router = APIRouter(prefix="/bookings", tags=["Bookings, Бронирования"])

@router.post("/")
async def add_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking: BookingPost,
):
    try:
        return await BookingsService(db).add_booking(booking, user_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    except WrongBookingDatesExceptions:
        raise WrongBookingDatesHTTPException

    except AllRoomsBookedException:
        raise AllRoomsBookedHTTPException


@router.get("/")
async def get_bookings(
        db: DBDep,
):
    return BookingsService(db).get_bookings()


@router.get("/me")
async def get_bookings_me(
        db: DBDep,
        user_id: UserIdDep
):
    return await BookingsService(db).get_bookings_me(user_id)

