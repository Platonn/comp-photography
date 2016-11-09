import numpy as np


class HomographyFinder:
	def __init__(self, points1, points2):
		self.A = np.zeros((8, 9))
		self.rowCursor = 0
		pointPairs = zip(points2, points1)  # caution: change places 1 and 2
		self.__buildA(pointPairs)

	def __buildA(self, pointPairs):
		for (p1, p2) in pointPairs:
			[y, x, _] = p1
			[yPrim, xPrim, _] = p2
			coefficientRow1 = [y, x, 1, 0, 0, 0, -y * yPrim, -x * yPrim, -yPrim]
			coefficientRow2 = [0, 0, 0, y, x, 1, -y * xPrim, -x * xPrim, -xPrim]
			self.__appendCoeffitientsRow(coefficientRow1)
			self.__appendCoeffitientsRow(coefficientRow2)

	def __appendCoeffitientsRow(self, coeffitientsRow):
		self.A[self.rowCursor] = coeffitientsRow
		self.rowCursor += 1

	def solve(self):
		(U, S, V) = np.linalg.svd(self.A, full_matrices=True)
		solution = V[-1, :]
		result = solution.reshape(3, 3)

		# spike
		# (U, s, V) = np.linalg.svd(A, full_matrices=True)
		# H = V[8, :]
		# result = H.reshape((3, 3))

		return result

	def solveNumpy(self):
		return np.linalg.solve(self.A, [0, 0, 0, 0, 0, 0, 0, 0])