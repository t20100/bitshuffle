import unittest
import os
import glob

import numpy as np
import h5py
from h5py import h5f, h5d, h5z, h5t, h5s, filters
from subprocess import Popen, PIPE, STDOUT

from bitshuffle import h5


os.environ["HDF5_PLUGIN_PATH"] = ""


class TestFilter(unittest.TestCase):

    def test_plugins(self):
        shape = (32 * 1024,)
        chunks = (4 * 1024,)
        dtype = np.int64
        data = np.arange(shape[0])
        fname = "tmp_test_filters.h5"
        f = h5py.File(fname)
        h5.create_dataset(f, "range", shape, dtype, chunks,
                filter_pipeline=(32008, 32000),
                filter_flags=(h5z.FLAG_MANDATORY, h5z.FLAG_MANDATORY),
                filter_opts=None)
        f["range"][:] = data

        f.close()
        #os.system('h5dump -H -p tmp_test_filters.h5')

        f = h5py.File(fname, 'r')
        d = f['range'][:]
        self.assertTrue(np.all(d == data))
        f.close()

    def tearDown(self):
        files = glob.glob("tmp_test_*")
        for f in files:
            os.remove(f)


if __name__ == "__main__":
    unittest.main()