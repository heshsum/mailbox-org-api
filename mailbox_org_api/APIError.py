class APIError(Exception):
    """Custom exception for API errors."""

    def __init__(self, message: str, code: int | None = None):
        self.message = message
        self.code = code
        err_str = f'Error {code} - {message}' if code is not None else message
        super().__init__(err_str)

