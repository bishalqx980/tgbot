def calc(math):
    try:
        return eval(math)
    except Exception as e:
        error_msg = f"Error Math: {e}"
        print(error_msg)
        return error_msg