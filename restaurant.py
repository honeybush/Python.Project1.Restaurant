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
		self.order = ""
	def getOrder(self, menu):
		n = 1
		print "Welcome to Food Place! Here is the menu (enter the food item, not the number):"
		for food in menu:
			print str(n) + ". " + food
			n += 1
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
		self.storage = Storage()
		self.inglist = self.storage.giveIngList()
		self.waiter = Waiter()
		self.avai = False
		self.confirmOrder()
	def confirmOrder(self):
		menu = self.getMenu()
		order = self.waiter.getOrder(menu)
		order = order.lower()
		for food in self.foodlist:
			if food.name == order:
				self.avai = True
				self.cooking(food)
		if self.avai == False:
			self.waiter.giveFood(self.avai, "n/a")
	def getMenu(self):
		menu = []
		for food in self.foodlist:
			menu.append(food.name)
		return menu
	def cooking(self, food):
		for ing in food.ingredients:
			temp = ing.split(":")
			for i in self.inglist:
				if i.name == temp[0]:
					if i.amt >= int(temp[1]):
						i.amt -= int(temp[1])
					else:
						s = "(To the Chef) Out of "+i.name+". Buy some? (y/n)"
						r = raw_input(s)
						if r.lower() == "y":
							n = input("How many?")
							while int(temp[1]) > n+i.amt:
								if n <= 0:
									n = input("Please input a positive number. How many?")
								else:
									i.amt += n
									r = raw_input("Still not enough to cook the food. Buy more?(y/n)")
									if r.lower() == "y":
										n = input("How much?")
									else:
										self.waiter.giveFood(False, "n/a")
										self.storage.updateList(self.inglist)
										return
							i.amt += n
							i.amt -= int(temp[1])
						else:
							self.waiter.giveFood(False, "n/a")
							return
		self.waiter.giveFood(self.avai, food.name)
		self.storage.updateList(self.inglist)

start = Chef()