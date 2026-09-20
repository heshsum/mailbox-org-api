class APIError(Exception):
    """Custom exception for API errors."""

    def __init__(self, message: str, code: int | None = None):
        self.message = message
        self.code = code
        super().__init__(f'Error {code} - {message}')
