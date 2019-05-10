#!/usr/bin/env python
import os,sys,signal
import time

import numpy

# Add the local folder to the import path:
network_dir = os.path.dirname(os.path.abspath(__file__))
network_dir = os.path.dirname(network_dir)
sys.path.insert(0,network_dir)


# import the necessary
from src.utils import flags


def main():

    FLAGS = flags.uresnet()
    FLAGS.parse_args()
    # FLAGS.dump_config()

    

    if FLAGS.MODE is None:
        raise Exception()

    if FLAGS.DISTRIBUTED:
        from src.utils import distributed_trainer

        trainer = distributed_trainer.distributed_trainer()
    else:
        from src.utils import trainercore
        trainer = trainercore.trainercore()
        
    if FLAGS.MODE == 'train' or FLAGS.MODE == 'inference':
        if not FLAGS.SPARSE:
            if FLAGS.CONV_MODE == '3D':
                from src.networks import uresnet
                net = uresnet.UResNet
            else:
                from src.networks import uresnet_classic
                net = uresnet_classic.UResNet

        else:
            from src.networks import sparseuresnet
            net = sparseuresnet.UResNet

        FLAGS.set_net(net)
        trainer.initialize()
        trainer.batch_process()

    if FLAGS.MODE == 'iotest':
        trainer.initialize(io_only=True)

        time.sleep(0.1)
        for i in range(FLAGS.ITERATIONS):
            start = time.time()
            mb = trainer.fetch_next_batch()

            if FLAGS.SPARSE:
                print(mb['image'].shape)
                print("Label mean: ", numpy.mean(mb['label']))
                print("Image mean: ", numpy.mean(mb['image']))
            else:
                print(mb['image'].shape)
                print("Label mean: ", numpy.mean(mb['label']))
                print("Image mean: ", numpy.mean(mb['image']))
                print("Weight sum: ", numpy.sum(mb['weight']))
            end = time.time()
            if not FLAGS.DISTRIBUTED:
                print(i, ": Time to fetch a minibatch of data: {}".format(end - start))
            else:
                if trainer._rank == 0:
                    print(i, ": Time to fetch a minibatch of data: {}".format(end - start))
            # time.sleep(0.5)
            trainer._larcv_interface.next('primary')

    trainer.stop()

if __name__ == '__main__':
    main()