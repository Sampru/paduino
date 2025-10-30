import os
import subprocess
import pygame

from item import Item


pygame.mixer.init()
        
# Define the base Action class
class Action(Item):
    def __init__(self, name):
        # Initialize the name of the action
        super().__init__("action")
        self.name = name

    def __str__(self):
        # Return the name of the action as a string
        return self.name

    def execute(self):
        # Define a generic execute method to be overridden by subclasses
        raise NotImplementedError("Subclasses should implement this method")


# Define the PythonAction class to execute Python code
class PythonAction(Action):
    def __init__(self, name, code_file, args = []):
        # Initialize with a name and Python code to execute
        super().__init__(name)
        self.code_file = code_file
        self.args = args

    def execute(self):
        # Execute the Python code provided
        try:
            subprocess.run(["./.venv/Scripts/python.exe", self.code_file, *self.args])
        except Exception as e:
            print(f"Error executing Python code in {self.name}: {e}")



# Define the SoundAction class to play a sound
class SoundAction(Action):
    def __init__(self, name, sound_file):
        # Initialize with a name and sound file to play
        super().__init__(name)
        self.sound_file = sound_file

    def execute(self):
        # Play the specified sound file
        try:
            pygame.mixer.music.load(self.sound_file)
            pygame.mixer.music.play()
            print(f"Playing sound: {self.sound_file}")
        except Exception as e:
            print(f"Error playing sound in {self.name}: {e}")


# Define the SoundAction class to play a sound
class DummyAction(Action):
    def __init__(self, name, msg):
        # Initialize with a name and sound file to play
        super().__init__(name)
        self.msg = msg

    def execute(self):
        # Play the specified sound file
        print(self.msg)


# Define the OSAction class to execute OS commands
class OSAction(Action):
    def __init__(self, name, command):
        # Initialize with a name and OS command to execute
        super().__init__(name)
        self.command = command

    def execute(self):
        # Execute the OS command provided
        try:
            os.system(self.command)
        except Exception as e:
            print(f"Error executing OS command in {self.name}: {e}")

