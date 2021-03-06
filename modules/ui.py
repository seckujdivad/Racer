import tkinter as tk
import importlib.util
import threading
import os
import sys
import json

class UI:
    def __init__(self, window_title):
        self.window_title = window_title
        
        self.page_cache = {}
        self.styling = {}
        self.binds = {}
        self.current_page = None
    
        threading.Thread(target = self.main_thread, name = 'UI main thread').start()
    
        self.cache_styling()
        self.cache_all_pages()
    
    def main_thread(self):
        self.root = tk.Tk()
        self.root.title(self.window_title)
        self.root.mainloop()
    
    def cache_all_pages(self):
        self.page_cache = {}
        self._recursive_cache_pages([])
    
    def _recursive_cache_pages(self, path):
        real_path = os.path.join(sys.path[0], 'ui', 'pages', *path)
        
        current_entry = self._dict_entry_from_list(path, self.page_cache)
        
        for item in os.listdir(real_path):
            if os.path.isfile(os.path.join(real_path, item)) and item.endswith('.py') and not os.path.isdir(os.path.join(real_path, item)):
                spec = importlib.util.spec_from_file_location('genericpage', os.path.join(real_path, item))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                current_entry[item[:len(item) - 3]] = module.Page({'frame': tk.Frame(self.root),
                                                                   'set title': self.set_title,
                                                                   'get styling': self.get_styling,
                                                                   'set weight': self.set_weight,
                                                                   'bind': self.bind,
                                                                   'call bind': self.call_bind})
                
            elif not item == '__pycache__':
                current_entry[item] = {}
                recursive_path = path.copy()
                recursive_path.append(item)
                self._recursive_cache_pages(recursive_path)
    
    def _dict_entry_from_list(self, list, dictionary):
        cpos = dictionary
        for item in list:
            cpos = cpos[item]
        return cpos
    
    def load_page(self, address):
        page = self._dict_entry_from_list(address, self.page_cache)
        page.tools['frame'].pack(fill = tk.BOTH, expand = True)
        
        if 'show' in dir(page):
            page.show()
        
        self.hide_page(self.current_page)
        self.current_page = address
        
    def hide_page(self, address):
        page = self._dict_entry_from_list(address, self.page_cache)
        page.tools['frame'].pack_destroy()
        
        if 'hide' in dir(page):
            page.hide()
        
        self.current_page = None
    
    def set_title(self, title):
        self.root.title('{} - {}'.format(self.window_title, title))
    
    def get_styling(self, font_type, widget):
        output_dict = self.styling['widgets'][widget]
        output_dict['font'] = (self.styling['fonts'][font_type]['typeface'], self.styling['fonts'][font_type]['size'])
        return output_dict
    
    def set_weight(self, frame, width, height, weight_ = 1, do_rows = True, do_columns = True):
        for x in range(width):
            for y in range(height):
                if do_columns:
                    frame.rowconfigure(y, weight = weight_)
            if do_rows:
                frame.columnconfigure(x, weight = weight_)
    
    def cache_styling(self):
        with open(os.path.join(sys.path[0], 'ui', 'styling.json'), 'r') as file:
            self.styling = json.load(file)
    
    def bind(self, event, function):
        if event in self.binds:
            self.binds[event].append(function)
        else:
            self.binds[event] = function
    
    def call_bind(self, event): 
        if event in self.binds:
            for function in self.binds[event]:
                function()
    
    def clear_bound(self, event):
        self.binds[event] = []
    
    def clear_from_bind(self, event, function):
        if event in self.binds:
            if function in self.binds[event]:
                self.binds[event].remove(function)