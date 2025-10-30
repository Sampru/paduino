class Item:
    def __init__(self, type):
        # Initialize the name of the action
        self.type = type
    
    def get_type(self):
        # Define a generic execute method to be overridden by subclasses
        return self.type