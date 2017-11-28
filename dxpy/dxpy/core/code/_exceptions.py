class DXPYTypeError(TypeError):
    def __init__(self, required_type, got_object_or_type, prefix=None):
        from ._message import type_error_message
        if not isinstance(got_object_or_type, type):
            got_object_or_type = type(got_object_or_type)
        super().__init__(type_error_message(required_type, got_object_or_type, prefix))
