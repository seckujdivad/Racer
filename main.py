import tkinter as tk
import sys
import os
import json

import modules.engine
import modules.ui

class App:
    def __init__(self):
        self.ui = modules.ui.UI('Racer')
        self.ui.load_page(['init'])
        
if __name__ == '__main__':
    App()