# define Python user-defined exceptions
class CustomException(Exception):
    """Base class for other exceptions"""


class BadAlgorithmParams(CustomException):
    """Raised when Bad Algorithm Params"""

    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super(BadAlgorithmParams, self).__init__(message)

        # Now for your custom code...
        self.errors = errors


class DatasetConnectionFailed(CustomException):
    """Raised when the input value is too large"""

    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super(DatasetConnectionFailed, self).__init__(message)

        # Now for your custom code...
        self.errors = errors


class ModelDoesNotExist(CustomException):
    """Raised when the input value is too large"""

    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super(ModelDoesNotExist, self).__init__(message)

        # Now for your custom code...
        self.errors = errors


class ModelAlreadyInMemory(CustomException):
    """Raised when the input value is too large"""

    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super(ModelAlreadyInMemory, self).__init__(message)

        # Now for your custom code...
        self.errors = errors


class InvalidPredictionParams(CustomException):
    """Raised when the input value is too large"""

    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super(InvalidPredictionParams, self).__init__(message)

        # Now for your custom code...
        self.errors = errors


class ModelNotInMemory(CustomException):
    """Raised when the input value is too large"""

    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super(ModelNotInMemory, self).__init__(message)

        # Now for your custom code...
        self.errors = errors



