from pynput.keyboard import Controller
import configparser
import sys
import time

args = sys.argv[1:]

config = configparser.ConfigParser()
config.read('./config/config.ini')

keyboard = Controller()
for char in config[args[0]][args[1]]:
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(0.05)