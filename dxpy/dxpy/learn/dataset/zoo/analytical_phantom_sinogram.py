from tables import *

DEFAULT_FILE_NAME = 'analytical_phantom_sinogram.h5'


class AnalyticalPhantomSinogram(IsDescription):
    phantom = UInt16Col(shape=(256, 256))
    sinogram = UInt16Col(shape=())
    phantom_type = UInt8Col()


def create_dataset_from_tf_records():
    pass
