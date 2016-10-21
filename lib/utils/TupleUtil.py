# import timeit
# from operator import mul
#
# class TupleUtil:
# 	@staticmethod
# 	def mult_by_scalar(tuple_in, scalar):
# 		return tuple(value * scalar for value in tuple_in)
#
# 	@staticmethod
# 	def mult_by_tuple(tuple1, tuple2):
# 		if len(tuple1) != len(tuple2): raise Exception('Tuples lenghts not equal!')
# 		return tuple(map(mul, tuple1, tuple2))
#
# 	@staticmethod
# 	def mult_2d_array_by_scalar(array, scalar):
# 		rows_num = array.length
# 		cols_num = array[0].length
# 		for y in range(0, rows_num):
# 			for x in range(0, cols_num):
# 				array[y][x] = TupleUtil.mult_by_scalar(array[y][x], scalar)
#
# 	@staticmethod
# 	def mult_2d_array_by_tuple(array, tuple):
# 		rows_num = array.length
# 		cols_num = array[0].length
# 		for y in range(0, rows_num):
# 			for x in range(0, cols_num):
# 				array[y][x] = TupleUtil.mult_by_tuple(array[y][x], tuple)
