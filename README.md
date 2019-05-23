# Sparse Cosmic Tagger

This repository implements submanifold Sparse convolutions for multiplane semantic segmentation, particularly for the cosmic tagging challenge.


### Submanifold sparse convolution ResNet

Implementation of a standard resnet architecture with submanifold sparse convolutions. Available for 2D and 3D.  In 2D, its possible to use the multiplane archicture with shared weights across planes, which merges downstream.

# Dependencies
 - The IO model is based on larcv, so you need larcv data files to run this.  
 - The sparse convolution requires the submanifold sparse convolution functions, from facebook.
 - Pytorch is the neural network framework
 - To run in a distrubuted way, horovod and mpi4py are required. 

# Running

Run 
```
bin/uresnet.py [ train | iotest | prof ] [options]
```

to execute the algorithm.