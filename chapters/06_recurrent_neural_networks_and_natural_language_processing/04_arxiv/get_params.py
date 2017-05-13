import tensorflow as tf

from helpers import AttrDict

def get_params():
    #return get_params_abstract()
    return get_params_three_country()

def get_params_abstract():
    max_length = 50
    sampling_temperature = 0.7
    rnn_cell = tf.contrib.rnn.GRUCell
 
    rnn_hidden = 200
    rnn_layers = 2
    learning_rate = 0.002
    optimizer = tf.train.AdamOptimizer(0.002)
 
    gradient_clipping = 5
    batch_size = 100
    epochs = 20
    epoch_size = 200

    checkpoint_dir = './arxiv-predictive-coding'
    input_file='abstracts___.txt'
    isUtf8= True
    return AttrDict(**locals())

def get_params_three_country():
    max_length = 50
    sampling_temperature = 0.7
    rnn_cell = tf.contrib.rnn.GRUCell

#    rnn_hidden = 512
#    rnn_layers = 3
#    learning_rate = 0.0002
#    optimizer = tf.train.AdamOptimizer(0.0002)

    rnn_hidden = 200
    rnn_layers = 2
    learning_rate = 0.002
    optimizer = tf.train.AdamOptimizer(0.002)
 
    gradient_clipping = 5
    batch_size = 100
    epochs = 20
    epoch_size = 200

    checkpoint_dir = './arxiv-predictive-coding1'
    input_file='three_country.txt'
    isUtf8= True
    return AttrDict(**locals())



	##  rnn_cell = tf.nn.rnn_cell.GRUCell
