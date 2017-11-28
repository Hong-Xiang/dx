def type_error_message(required_type, got_type, prefix=""):
    if not isinstance(prefix, str):
        from .common import DXPYTypeError
        raise DXPYTypeError(str, prefix, "Arg prefix of type_error_")
    if not prefix == "":
        return "{} is required to be {}, got {}.".format(prefix, required_type, got_type)
