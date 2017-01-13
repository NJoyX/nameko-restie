from . import codes


class HttpError(Exception):
    error_code = 'BAD_REQUEST'
    status_code = 400


class BadRequest(HttpError):
    pass


class InvalidArgumentsError(HttpError):
    error_code = 'INVALID_ARGUMENTS'


class NotFoundError(HttpError):
    status_code = codes.NOT_FOUND
    error_code = 'NOT_FOUND'


class MethodNotAllowed(HttpError):
    status_code = codes.METHOD_NOT_ALLOWED
    error_code = 'METHOD_NOT_ALLOWED'


class NoContent(HttpError):
    status_code = codes.NO_CONTENT
    error_code = 'NO_CONTENT'
