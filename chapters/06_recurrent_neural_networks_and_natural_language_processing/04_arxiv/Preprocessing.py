import random
import numpy as np


class Preprocessing:

    VOCABULARY = \
        " $%'()+,-./0123456789:;=?ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
        "\\^_abcdefghijklmnopqrstuvwxyz{|}"

    def __init__(self, texts, length, batch_size,voca=None):
        self.texts = texts
        self.length = length
        self.batch_size = batch_size
        print("pre.voca=",len(voca))
        if voca is not None :
           self.VOCABULARY=voca

        self.lookup = {x: i for i, x in enumerate(self.VOCABULARY)}
        print ( self.lookup)

    def __call__(self, texts):
        batch = np.zeros((len(texts), self.length, len(self.VOCABULARY)))
        for index, text in enumerate(texts):
            text = [x for x in text if x in self.lookup]
            #print ("text=",text,",len(txt)=",len(text),",self.length= ",self.length)
            assert 2 <= len(text) <= self.length
            #if 2 <= len(text) <= self.length : 
            #    continue

            for offset, character in enumerate(text):
                code = self.lookup[character]
                batch[index, offset, code] = 1
        return batch

    def __iter__(self):
        windows = []
        for text in self.texts:
            for i in range(0, len(text) - self.length + 1, self.length // 2):
                windows.append(text[i: i + self.length])
        assert all(len(x) == len(windows[0]) for x in windows)
        while True:
            random.shuffle(windows)
            for i in range(0, len(windows), self.batch_size):
                batch = windows[i: i + self.batch_size]
                yield self(batch)