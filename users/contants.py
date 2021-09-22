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
# form actions
ACTION_LOGIN = "/"
ACTION_REGISTER = "/register/"
# urls
HOME_PAGE_URL = "/admin/"
LOGIN_PAGE_URL = "/"
REGISTER_PAGE_URL = "/"
# Templates
LOGIN = "login_register.html"
REGISTER = "login_register.html"
