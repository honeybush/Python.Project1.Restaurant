class Food(): #model
	def __init__(self):
		self.name = ""

class Waiter(): #view
	def __init__(self):
		self.order = ""
	def getOrder(self):
		order = raw_input("What is your order? ")
		return order
	def giveFood(self, food):
		print "Here is your", food + ". Enjoy your meal!"

class Chef(): #control
	def __init__(self):
		self.food = Food()
		self.waiter = Waiter()
		self.cooking()
	def cooking(self):
		food = self.waiter.getOrder()
		self.food.name = food
		self.waiter.giveFood(self.food.name)

start = Chef()