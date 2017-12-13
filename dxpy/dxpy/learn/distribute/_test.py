import tensorflow as tf
import numpy as np


def dataset():
    nb_total = 10000
    x = np.random.uniform(size=[nb_total])
    y = np.sin(x)


