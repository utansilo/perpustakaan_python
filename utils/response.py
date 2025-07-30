def success_message(data=None, message="Success"):
    return {
        "status": "success",
        "message": message,
        "data": data
    }, 200

def error_message(message="Something went wrong", status_code=400):
    return {
        "status": "error",
        "message": message,
        "data": None
    }, status_code