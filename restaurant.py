class Food(): #model
	def __init__(self):
		self.name = ""

class Menu():
	def __init__(self):
		self.food = []
		f = open("recipes.txt", "r")
		for line in f:
			temp = Food()
			if line[len(line)-1] == "\n":
				temp.name = line[:len(line)-1]
			else:
				temp.name = line
			print temp.name
			self.food.append(temp)
		f.close()
	def giveMenu(self):
		return self.food

class Waiter(): #view
	def __init__(self):
		self.order = ""
	def getOrder(self):
		order = raw_input("What is your order? ")
		return order
	def giveFood(self, avai, food):
		if avai == True:
			print "Here is your", food + ". Enjoy your meal!"
		else:
			print "Sorry, the food you ordered is not available."

class Chef(): #control
	def __init__(self):
		self.menu = Menu()
		self.foodlist = self.menu.giveMenu()
		self.waiter = Waiter()
		self.avai = False
		self.confirmOrder()
	def confirmOrder(self):
		order = self.waiter.getOrder()
		order = order.lower()
		for food in self.foodlist:
			if food.name == order:
				self.avai = True
				self.cooking(food)
		if self.avai == False:
			self.waiter.giveFood(self.avai, "n/a")
	def cooking(self, food):
		self.waiter.giveFood(self.avai, food.name)

start = Chef()