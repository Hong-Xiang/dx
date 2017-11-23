import numpy as np


def random_crop_offset(input_shape, target_shape, *, batched=False):
    max_offset = [s - t for s, t in zip(input_shape, target_shape)]
    if any(map(lambda x: x < 0, max_offset)):
        raise ValueError("Invalid input_shape {} or target_shape {}.".format(
            input_shape, target_shape))
    if not batched:
        offset = []
        for s in max_offset:
            if s == 0:
                offset.append(0)
            else:
                offset.append(np.random.randint(0, s))    
        return offset
    else:
        offsets = []
        if max_offset[0] > 0:
            raise ValueError("Random crop offset input_shape[0] and target_shape[0]")
