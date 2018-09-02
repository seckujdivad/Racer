import tkinter as tk

class Page:
    def __init__(self, tools):
        self.tools = tools
        
        title_label = tk.Label(self.tools['frame'], text = 'Racer', **self.tools['styling']('large', 'label'))
        
        title_label.grid(row = 0, column = 0, sticky = 'NESW')
    
    def show(self):
        pass
    
    def hide(self):
        pass