class NoDifferenceError(Exception):
    """
    This exception represents a case where Schoology returns a String with the API
    and makes it easier to tell what went wrong.
    """
    pass


class NoDataError(Exception):
    """
    This exception represents a case where Schoology returns no data or invalid JSON
    from a standard API endpoint.
    """
    pass
