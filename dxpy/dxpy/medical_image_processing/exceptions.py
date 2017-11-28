class MedicalImageProcessingError(Exception):
    pass


class InputVerifacationError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
