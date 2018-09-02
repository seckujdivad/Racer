import tkinter as tk
import importlib.util
import threading
import os
import sys

class UI:
    def __init__(self, window_title):
        self.page_cache = {}
        self.window_title = window_title
    
        threading.Thread(target = self.main_thread, name = 'UI main thread').start()
    
        self.cache_all_pages()
    
    def main_thread(self):
        self.root = tk.Tk()
        self.root.title(self.window_title)
        self.root.mainloop()
    
    def cache_all_pages(self):
        self.page_cache = {}
        self._recursive_cache_pages([])
    
    def _recursive_cache_pages(self, path):
        real_path = os.path.join(sys.path[0], 'uipages', *path)
        
        current_entry = self._dict_entry_from_list(path, self.page_cache)
        
        for item in os.listdir(real_path):
            if os.path.isfile(os.path.join(real_path, item)) and item.endswith('.py') and not os.path.isdir(os.path.join(real_path, item)):
                spec = importlib.util.spec_from_file_location('genericpage', os.path.join(real_path, item))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                current_entry[item[:len(item) - 3]] = module.Page({'frame': tk.Frame(self.root),
                                                                   'set title': self.set_title})
                
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
        page.show()
        
    def hide_page(self, address):
        page = self._dict_entry_from_list(address, self.page_cache)
        page.tools['frame'].pack_destroy()
        page.hide()
    
    def set_title(self, title):
        self.root.title('{} - {}'.format(self.window_title, title))