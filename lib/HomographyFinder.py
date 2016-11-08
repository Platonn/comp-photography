import numpy as np
import math


class HomographyFinder:
	def __init__(self, points1, points2):
		self.A = np.zeros((8, 9))
		self.rowCursor = 0
		pointsPairs = zip(points1, points2)
		#print pointsPairs

		self.__buildA(pointsPairs)

		#print self.A

	def __buildA(self, pointsPairs):
		for (p1, p2) in pointsPairs:
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
		svdSolution = np.linalg.svd(self.A, full_matrices=True)
		(U, S, V) = svdSolution

		solution = np.append(S, [0])

		#print len(tempResult)
		#print np.round(tempResult[0], 2)
		#print tempResult[1]
		#print np.round(tempResult[2], 2)
		#result = tempResult[1]

		result = solution.reshape(3,3)
		print result
		return result
