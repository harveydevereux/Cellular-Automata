from dynamic_ext import *
import numpy as np

A = np.array([[0,1,1,1],[0,1,1,1],[0,1,1,1],[0,0,0,0]])

G = Grid(A)
print(A)
while(A.sum() > 0):
    A = G.get_next_gen(5)
    print(A)
