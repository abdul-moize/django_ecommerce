"""
Contains functions that are used at multiple places
"""


def is_logged_in(request):
    """
    Checks if a user is logged in or not
    Args:
        request(HttpRequest):
    Returns:
        (bool): True if user is logged in
                False otherwise
    """
    return "_auth_user_id" in request.session
