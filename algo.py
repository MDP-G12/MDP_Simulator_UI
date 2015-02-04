import time

# ----------------------------------------------------------------------
# class definition of algoAbstract.
# 
#   - explore()
#		robot starts doing exploration
# 
#   - findSP()
#		Finding Shortest Path, based on the known maps.
# 
#   - run()
#		robot starts running according shortest path algorithm
# ----------------------------------------------------------------------
class algoAbstract:
	# def __init__(self):

	def explore(self):
		raise NotImplementedError

	def findSP(self):
		raise NotImplementedError

	def run(self):
		raise NotImplementedError



# ----------------------------------------------------------------------
# class definition of algoFactory.
# 
#   - explore()
#		robot starts doing exploration
# 
#   - findSP()
#		Finding Shortest Path, based on the known maps.
# 
#   - run()
#		robot starts running according shortest path algorithm
# ----------------------------------------------------------------------
class algoFactory:
	def __init__(self, simulator, algoName="BF1"):
		if (algoName == "BF1"):
			self.algo = algoBF1(simulator)
		else:
			raise NameError('algoName not found')

	def explore(self):
		self.algo.explore()



# ----------------------------------------------------------------------
# class definition of algoBF1.
# Implementation class of algoAbstract using algorithm Brute Force #1
# ----------------------------------------------------------------------
class algoBF1(algoAbstract):
	def __init__(self, simulator):
		self.sim = simulator

	def explore(self):
		i = 1
		while (True):
			if ((i%20) > 0):
				self.sim.move_delay(i)
			else:
				self.sim.right_delay(i)
			i = i + 1
			if (i > 200):
				break
