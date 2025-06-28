class NabronirovalException(Exception):

    detail = "Непредвиденная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):

    detail = "Номер не найден"


class AllRoomsBookedException(NabronirovalException):

    detail = "Все номера заняты"


class ObjectAlreadyExistsException(NabronirovalException):

    detail = "Объект уже существует"


class WrongBookingDatesExceptions(NabronirovalException):

    detail = "Неверно указаны даты"

