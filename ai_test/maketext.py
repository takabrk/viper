#!/usr/bin/env python
#-*- coding:utf-8 -*-

import codecs
from markovChain import PrepareChain
from markovChain import GenerateText

f = open("input.txt")
text = f.read()
f.close()

chain = PrepareChain(text)
triplet_freqs = chain.make_triplet_freqs()
chain.save(triplet_freqs,True)

generator = GenerateText()
gg = generator.generate()
print(gg)
print(type(gg))
f2 = codecs.open("test111.txt","w","utf-8")
f2.write(gg)
f2.close()