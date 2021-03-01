class Recipe:
    product = []
    component = []
    requirements = []
    name = "Recipe"
    perMinute = False
    frequency = 60

    def __init__(self, name="Recipe"):
        self.name = name
        self.product = list()
        self.component = list()
        self.requirements = list()
        pass

    def AddProduct(self, name, count):
        self.product.append([name, count].copy())

    def AddRequirement(self, name):
        self.requirements.append(name)

    def AddComponent(self, name, count):
        self.component.append([name, count].copy())

    def ChangeCountType(self, count):
        self.perMinute = not self.perMinute
        self.frequency = count

    def __str__(self):
        res = self.name + " generates " + self.product.__str__() + " from " + self.component.__str__()

        if self.perMinute:
            res += " crafting " + str(self.frequency) + " per minute"

        if len(self.requirements) == 0:
            res += " and has no special requirements"
        else:
            res += " but requires " + str(self.requirements)

        return res


class Factory:
    name = "Factory"
    efficiency = 1

    def __init__(self, name="Factory", efficiency=1):
        self.name = name
        self.efficiency = efficiency
