from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = "Непредвиденная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class NabronirovalHTTPException(HTTPException):
    detail = "Непредвиденная ошибка"
    status_code = 500

    def __init__(self, *args, **kwargs):
        super().__init__(self.status_code, self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Номер не найден"


class AllRoomsBookedException(NabronirovalException):
    detail = "Все номера заняты"


class ObjectAlreadyExistsException(NabronirovalException):
    detail = "Объект уже существует"


class WrongBookingDatesExceptions(NabronirovalException):
    detail = "Неверно указаны даты"


class HotelAlreadyExistsException(NabronirovalException):
    detail = "Отель уже существует"


class HotelNotFoundException(NabronirovalException):
    detail = "Отель не существует"


class HotelAlreadyHttpExistsException(NabronirovalHTTPException):
    status_code = 409
    detail = "Отель уже существует"


class HotelNotFoundHTTPException(NabronirovalException):
    status_code = 404
    detail = "Отель не существует"


class WrongBookingDatesException(NabronirovalException):
    detail = "Неверные даты"


class WrongBookingDatesHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Неверные даты бронирования"


class RoomNotFoundException(NabronirovalException):
    detail = "Номер не найден"


class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Номер не найден"


class FacilityAlreadyExistsException(NabronirovalException):
    detail = "Удобство уже существует"


class FacilityAlreadyExistsHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Удобство уже существует"


class AllRoomsBookedHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Все номера заняты"


class UserAlreadyExistsException(NabronirovalException):
    detail = "Такой пользователь уже зарегистрирован"


class UserAlreadyExistsHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Такой пользователь уже зарегистрирован"


class UserNotFountException(NabronirovalException):
    detail = "Такой пользователь не зарегистрирован"


class UserNotFountHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Такой пользователь не зарегистрирован"


class UserWrongPasswordException(NabronirovalException):
    detail="Неверный пароль"


class UserWrongPasswordHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail="Неверный пароль"