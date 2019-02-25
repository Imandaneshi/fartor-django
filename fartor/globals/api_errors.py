API_ERRORS = {
    "validation_error": {
        "code": "validation_error",
        "status": 400,
        "description": "Invalid data or input",
        "actions": False,
    },
    "unknown_error": {
        "code": "unknown_error",
        "status": 500,
        "description": "Unknown error happened",
        "actions": False,
    },
    "user_not_found": {
        "code": "user_not_found",
        "status": 404,
        "description": "Unknown error happened",
        "actions": ["login", ],
    },
    "wrong_password": {
        "code": "wrong_password",
        "status": 400,
        "description": "Wrong password",
        "actions": ["login", ],
    },
    "not_authenticated": {
        "code": "not_authenticated",
        "status": 403,
        "description": "This request is not authenticated",
        "actions": ["self", ],
    },
}


def get_error_info(code):
    if code not in API_ERRORS:
        return None
    for k, v in API_ERRORS.items():
        if k == code:
            return {
                "code": v['code'],
                "status": v['status'],
                "description": v['description']
            }


def get_error(code=None, return_unknown=True, details=None):
    if not code:
        return API_ERRORS
    error = get_error_info(code)
    if error and details:
        error['details'] = details

    return error or (get_error_info('unknown_error')
                     if return_unknown else None)
