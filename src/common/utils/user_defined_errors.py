class UserErrors(Exception):
    def __init__(self, message=None, response_code=None):
        self.message = message if message else "Internal Server Error"
        self.response_code = response_code if response_code else 500
        self.type = "UserErrors"


class PermissionDeniedError(UserErrors):
    def __init__(self, message=None, response_code=None):
        self.message = message if message else "Could not validate credentials"
        self.response_code = response_code if response_code else 401
        self.type = "PermissionDeniedError"


class UserUser(UserErrors):
    def __init__(self, message=None, response_code=None):
        self.message = message if message else "user access: Access Denied"
        self.response_code = response_code if response_code else 400
        self.type = "PermissionDeniedError"
