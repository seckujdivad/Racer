import tkinter as tk

class Page:
    def __init__(self, tools):
        self.tools = tools
        
        label_title = tk.Label(self.tools['frame'], text = 'Racer', **self.tools['styling']('large', 'label'))
        
        button_play = tk.Button(self.tools['frame'], text = 'Play', **self.tools['styling']('medium', 'button'))
        
        label_title.grid(row = 0, column = 0, sticky = 'NESW')
        button_play.grid(row = 1, column = 0, sticky = 'NESW')
    
    def show(self):
        pass
    
    def hide(self):
        pass