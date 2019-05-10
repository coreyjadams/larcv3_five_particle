from . import larcv_io



# Here, we set up a bunch of template IO formats in the form of callable functions:

def train_io(input_file, prepend_names=""):
    data_proc = gen_sparse2d_data_filler(name=prepend_names + "data", producer="\"data\"")
    label_proc = gen_sparse2d_data_filler(name=prepend_names + "label", producer="\"segment\"")


    config = larcv_io.ThreadIOConfig(name="TrainIO")

    config.add_process(data_proc)
    config.add_process(label_proc)

    config.set_param("InputFiles", input_file)

    return config


def test_io(input_file, prepend_names="aux_"):
    data_proc = gen_sparse2d_data_filler(name=prepend_names + "data", producer="\"data\"")
    label_proc = gen_sparse2d_data_filler(name=prepend_names + "label", producer="\"segment\"")


    config = larcv_io.ThreadIOConfig(name="TestIO")

    config.add_process(data_proc)
    config.add_process(label_proc)

    config.set_param("InputFiles", input_file)

    return config


def gen_sparse2d_data_filler(name, producer):

    proc = larcv_io.ProcessConfig(proc_name=name, proc_type="BatchFillerImage2D")

    proc.set_param("Verbosity",         "3")
    proc.set_param("ImageProducer",  producer)
    proc.set_param("Channels",          "[0,1,2]")
    proc.set_param("CaffeMode",     "false")
    return proc

