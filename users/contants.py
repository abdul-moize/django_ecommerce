"""
Contains values that dont change after initial assignment
"""
# codes for roles
CUSTOMER = "CU"
CONTENT_MANAGER = "CM"
SALES_MANAGER = "SM"
SYSTEM_ADMIN = "SA"

# code -> name dictionary
ROLES = {
    CUSTOMER: "Customer Role",
    CONTENT_MANAGER: "Content Manager",
    SALES_MANAGER: "Sales Manager",
    SYSTEM_ADMIN: "System Admin",
}
# directory containing css file
LOGIN_CSS_DIRECTORY = "/login_register/style.css"
# form actions
ACTION_LOGIN = "/users/login/"
ACTION_REGISTER = "/users/"
# urls
HOME_PAGE_URL = "/"
LOGIN_PAGE_URL = "/users/login/"
REGISTER_PAGE_URL = "/users/login/"
# Templates
LOGIN = "login_register/index.html"
REGISTER = "login_register/index.html"
LOGIN_SUCCESS = "login_success/index.html"
LOGIN_FAILURE = "login_failure/index.html"
REGISTER_SUCCESS = "register_success/index.html"
REGISTER_FAILURE = "register_failure/index.html"
# Contexts
LOGIN_CONTEXT = {
    "path_css": LOGIN_CSS_DIRECTORY,
    "action_login": ACTION_LOGIN,
    "action_register": ACTION_REGISTER,
}
REGISTER_CONTEXT = {
    "path_css": LOGIN_CSS_DIRECTORY,
    "action_login": ACTION_LOGIN,
    "action_register": ACTION_REGISTER,
}
LOGIN_SUCCESS_CONTEXT = {"home_page": HOME_PAGE_URL}
LOGIN_FAILURE_CONTEXT = {"login_page": LOGIN_PAGE_URL}
REGISTER_FAILURE_CONTEXT = {"register_page": REGISTER_PAGE_URL}
REGISTER_SUCCESS_CONTEXT = {"login_page": LOGIN_PAGE_URL}
