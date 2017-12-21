class DXPYTypeError(TypeError):
    def __init__(self, required_type, got_type_or_object, object_name="Something"):
        if not isinstance(got_type_or_object, type):
            got_type_or_object = type(got_type_or_object)
        super("{} is required to be instance of {}, got {}.".format(object_name,
                                                                    required_type,
                                                                    got_type_or_object))
