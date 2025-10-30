from action import DummyAction, PythonAction, SoundAction
from item import Item

active = None

# Define the class for the menu
class Menu(Item):
    def __init__(self, name):
        # Initialize the menu with a name and an empty list of items
        super().__init__("menu")
        self.name = name
        self.code = "_MS"
        self.items = []
        self.item_max = 6

    def add_item(self, item):
        # Add an item (either a submenu or an action) to the menu
        if len(self.items) == self.item_max:
            raise Exception("No more than 6 items")
        else: 
            self.items.append(item)

    def __str__(self):
        return self.name

    def menu_str(self):
        # Create a string representation of the menu
        menu_string = self.code + "\n" + str(self) + "\n"
        index = 1
        for item in self.items:
            item_name = str(item)[:7] if len(str(item)) > 7 else str(item).ljust(7)
            menu_string += str(index) + ") " + item_name + (" " if index%2 != 0 else "\n")
            index += 1
        return menu_string.encode()
    
    def getAction(self, i):
        return self.items[i-1]


main = Menu("Menu nagusia")
menu = Menu("Keypad")
menu2 = Menu("Sounds")
menu.add_item(PythonAction("bw p", "./code/sendpw.py", ["bitwarden", "password"]))
menu.add_item(PythonAction("Uffi u", "./code/sendpw.py", ["uffi", "username"]))
menu.add_item(PythonAction("Uffi p", "./code/sendpw.py", ["uffi", "password"]))
menu2.add_item(SoundAction("Fartrb", "./sounds/fart-with-reverb.mp3"))
main.add_item(menu)
main.add_item(menu2)
