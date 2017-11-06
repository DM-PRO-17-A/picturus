from ctypes import *
trip = cdll.LoadLibrary('./test_queue.so')

py_list = [1, 2, 3, 4, 5]
c_array = (c_int * len(py_list))(*py_list)

print(trip.iterate_input(c_array))
