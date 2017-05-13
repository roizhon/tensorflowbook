import tensorflow as tf
import numpy as np
import os
import codecs
from helpers import overwrite_graph
from Preprocessing import Preprocessing
from PredictiveCodingModel import PredictiveCodingModel
from helpers import ensure_directory

class Sampling:

    @overwrite_graph
    def __init__(self, params):
        self.params = params

        # added
        voca=None
        if self.params.isUtf8 :
            voca=self.loadVoca(params.input_file)
        # added
        print("vaca=",voca)
        self.prep = Preprocessing([], 2, self.params.batch_size,voca)

        self.sequence = tf.placeholder(
            tf.float32, [1, 2, len(self.prep.VOCABULARY)])
        self.state = tf.placeholder(
            tf.float32, [1, self.params.rnn_hidden * self.params.rnn_layers])
        self.model = PredictiveCodingModel(
            self.params, self.sequence, self.state)
        self.sess = tf.Session()
        checkpoint = tf.train.get_checkpoint_state(self.params.checkpoint_dir)
        if checkpoint and checkpoint.model_checkpoint_path:
            tf.train.Saver().restore(
                self.sess, checkpoint.model_checkpoint_path)
        else:
            print('Sampling from untrained model.')
        print('Sampling temperature', self.params.sampling_temperature)

    def __call__(self, seed, length=100):
        text = seed
        state = np.zeros((1, self.params.rnn_hidden * self.params.rnn_layers))
        for _ in range(length):
            feed = {self.state: state}
            feed[self.sequence] = self.prep([text[-1] + '?'])
            prediction, state = self.sess.run(
                [self.model.prediction, self.model.state], feed)
            text += self._sample(prediction[0, 0])
        return text

    def _sample(self, dist):
        dist = np.log(dist) / self.params.sampling_temperature
        dist = np.exp(dist) / np.exp(dist).sum()
        choice = np.random.choice(len(dist), p=dist)
        choice = self.prep.VOCABULARY[choice]
        return choice

    def loadVoca(self,inputfile):
        cache_dir = './arxiv'
        cache_dir = os.path.expanduser(cache_dir)
        ensure_directory(cache_dir)
        filename = os.path.join(cache_dir, inputfile)

        with codecs.open(filename,'r', encoding='UTF-8') as file_:
            self.data = file_.readlines()
            
        self.vocaMap= {}
        self.VOCABULARY=''
        seq=0
        for i in range(len(self.data)):
            for j in range(len(self.data[i])): 
                if not self.data[i][j] in self.vocaMap  :
                    if self.data[i][j] == '\r' or self.data[i][j] == '\n' :
                        continue
                    #print (self.data[i][j] )
                    seq+=1 
                    self.vocaMap[self.data[i][j]]=seq
                    self.VOCABULARY += self.data[i][j]

        return  self.VOCABULARY
