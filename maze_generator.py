import numpy as np
import random as rr
import matplotlib.pyplot as plt
import os
import sys
import shutil
import multiprocessing
import glob
import IPython

def randGridMaze(number, width=101, height=101):
    shape = (height,width)
    Z = np.random.choice([0,1], size=shape, p=[.70,.30])
    plt.figure()
    plt.imshow(Z, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.savefig("pics/randGrid/maze{0:0=2d}.png".format(number))
    np.savetxt("arrs/randGrid/{0:0=2d}.txt".format(number),Z,fmt='%d')
    

if __name__ == "__main__":
    if os.path.exists("arrs"):
        shutil.rmtree("arrs")
    if os.path.exists("pics"):
        shutil.rmtree("pics")
    if os.path.exists("maze.png"):
        os.remove("maze.png")
    
    for i in ["",  "/randGrid/"]: 
        os.mkdir("pics"+i)
        os.mkdir("arrs"+i)

    ### specify the number of grids you want to generate
    n_grids = int(sys.argv[1])
    

    multiprocessing.freeze_support()
    num_proc = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes = num_proc)

    nn = [i for i in range(n_grids)]
    pool.map(randGridMaze, nn)

    pool.close()
    pool.join()
