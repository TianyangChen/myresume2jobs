#!/usr/bin/python
import gensim

class sentences_generator():
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        for line in open(self.filename):
            sentence = line.rstrip().split(' ')
            yield sentence

sentences = sentences_generator('data.txt')

model = gensim.models.Word2Vec(sentences)

model.save('w2v.model')