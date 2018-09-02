import tkinter as tk

class Page:
    def __init__(self, tools):
        self.tools = tools
        
        label = tk.Label(self.tools['frame'], text = 'Hi')
        
        label.pack()
    
    def show(self):
        pass
    
    def hide(self):
        pass