

class TectonException(Exception):
    """
    Base class for all Tecton specific exceptions
    """


class TectonClientException(TectonException):
    """
     Class that declares a TectonClientException,
     exceptions thrown by the client
    """


class TectonServerException(TectonException):
    """
     Class that declares a TectonServerException,
     exceptions thrown by the server
    """


INVALID_KEY = "API Key cannot be empty"
INVALID_URL = "Cannot connect to Tecton because the URL is invalid"
