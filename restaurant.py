class Food(): #model
	def __init__(self):
		self.name = ""
		self.ingredients = []

class Ingredient(): #model
	def __init__(self):
		self.name = ""
		self.amt = 0

class Storage():#ingredient factory-ish
	def __init__(self):
		self.ing = []
		f = open("ingredients.txt", "r")
		for line in f:
			temp = Ingredient()
			temp2 = line.split(":")
			temp.name = temp2[0]
			temp3 = temp2[1]
			temp.amt = int(temp3[:len(temp3)-1])
			self.ing.append(temp)
		f.close()
	def giveIngList(self):
		return self.ing
	def buyIng(self, ing, amt):
		ing.amt += amt
		return ing
	def updateList(self, list):
		self.ing = list
		f = open("ingredients.txt", "w")
		for ing in self.ing:
			temp = ing.name+":"+str(ing.amt)+"\n"
			f.write(temp)
		f.close()

class Menu(): #food factory-ish
	def __init__(self):
		self.food = []
		f = open("recipes.txt", "r")
		for line in f:
			temp = Food()
			recipe = line.split(";")
			temp.name = recipe[0]
			ing = recipe[1:]
			#print len(ing)
			if len(ing) > 1:
				for ingredient in ing:
					if ingredient[len(ingredient)-1] == "\n":
						temp.ingredients.append(ingredient[:len(ingredient)-1])
					else:
						temp.ingredients.append(ingredient)
			else:
				_ing = ing[0]
				if _ing[len(_ing)-1] == "\n":
						temp.ingredients.append(_ing[:len(_ing)-1])
				else:
					temp.ingredients.append(_ing)
			#print temp.name, temp.ingredients
			self.food.append(temp)
		f.close()
	def giveMenu(self):
		return self.food

class Waiter(): #view
	def __init__(self):
		self.order = []
	def getOrder(self, menu):
		n = 1
		print "Welcome to Food Place! Here is the menu (enter the food item, not the number):"
		for food in menu:
			print str(n) + ". " + food
			n += 1
		r = raw_input("Dine in?(y/n)")
		if r.lower() == "y":
			while r.lower() == "y":
				order = raw_input("What is your order? ")
				amt = input("How many?")
				temp = order.lower()+":"+str(amt)
				self.order.append(temp)
				r = raw_input("Order more?")
			return self.order
		else:
			print "Please come any time!"
			exit(0)
	def giveFood(self, avai, food):
		if avai == True:
			print "Here is your", food + ". Enjoy your meal!"
		else:
			print "Sorry, the "+food+" you ordered is not available."

class Chef(): #control
	def __init__(self):
		self.menu = Menu()
		self.foodlist = self.menu.giveMenu()
		self.storage = Storage()
		self.inglist = self.storage.giveIngList()
		self.waiter = Waiter()
		self.avai = False
		self.confirmOrder()
	def confirmOrder(self):
		n = 0
		menu = self.getMenu()
		order = self.waiter.getOrder(menu)
		#print order
		for o in order:
			#print o
			temp = str(o)
			temp = o.split(":")
			#print temp
			for food in self.foodlist:
				if food.name == temp[0]:
					self.avai = True
					while n < int(temp[1]):
						self.cooking(food)
						n += 1
			if self.avai == False:
				self.waiter.giveFood(self.avai, food.name)
			n = 0
	def getMenu(self):
		menu = []
		for food in self.foodlist:
			menu.append(food.name)
		return menu
	def cooking(self, food):
		for ing in food.ingredients:
			temp = ing.split(":")
			for i in self.inglist:
				amt_n = int(temp[1])
				if i.name == temp[0]:
					if i.amt >= amt_n:
						i.amt -= amt_n
					else:
						s = "(To the Chef) Out of "+i.name+". Buy some? (y/n)"
						r = raw_input(s)
						if r.lower() == "y":
							n = input("How many?")
							while amt_n > n+i.amt:
								if n <= 0:
									n = input("Please input a positive number. How many?")
								else:
									i.amt += n
									r = raw_input("Still not enough to cook the food. Buy more?(y/n)")
									if r.lower() == "y":
										n = input("How much?")
									else:
										self.waiter.giveFood(False, food.name)
										self.storage.updateList(self.inglist)
										return
							i.amt += n
							i.amt -= amt_n
						else:
							self.waiter.giveFood(False, food.name)
							return
		self.waiter.giveFood(self.avai, food.name)
		self.storage.updateList(self.inglist)

start = Chef()