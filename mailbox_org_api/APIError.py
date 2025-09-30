class APIError(Exception):
    """Custom exception for API errors."""
    def __init__(self, message, code=None):
        super().__init__(f'Error {code} - {message}')