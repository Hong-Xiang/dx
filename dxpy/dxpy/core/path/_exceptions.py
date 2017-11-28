class PathTypeError(TypeError):
    def __init__(self, wrong_type):
        super().__init__("Can not convert {} to Path.".format(wrong_type))


class PathValueError(ValueError):
    def __init__(self, wrong_value):
        super().__init__("Can not parst {} as Path.".format(wrong_value))
