# Python
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf


tf.enable_eager_execution()

hello = tf.constant('Hello World from TensorFlow')


print(hello)


