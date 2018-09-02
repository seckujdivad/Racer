class Display:
    def __init__(self, canvas, coords):
        self.canvas = canvas
        self.coords = coords
        
        self.objects = []
        
    def draw(self, coords, colour, tags = []):
        scr_coords = self.frac_to_screen(coords)
        #self.print_coordinates(coords)
        self.objects.append({'canvobj': self.canvas.create_polygon(*scr_coords, fill = colour, outline = colour),
                             'colour': colour,
                             'tags': tags,
                             'coords': scr_coords})
    
    def clear_all(self):
        for object in self.objects:
            self._clear_object(object)
    
    def clear_tags(self, tags):
        if type(tags) == list:
            for tag in tags:
                self._clear_tag(tag)
        elif type(tags) == str:
            self._clear_tag(tags)
        else:
            raise TypeError('clear_tags only takes list or string, not "{}"'.format(type(tags)))
    
    def _clear_tag(self, tag):
        for object in self.objects:
            if tag in object['tags']:
                self._clear_object(object)
    
    def _clear_object(self, object):
        self.canvas.delete(object['canvobj'])
    
        self.objects.remove(object)
    
    def frac_to_screen(self, coords):
        width = self.get_width()
        height = self.get_height()
        
        out_coords = []
        
        for x, y in coords:
            x = (x + 1) / 2
            y = 0 + ((y + 1) / 2)
            out_coords.append((x * width) + self.coords[0])
            out_coords.append((y * height) + self.coords[1])
        return out_coords
    
    def move_screen_coords(self, x, y, coords):
        output_coords = []
        for i in range(0, len(coords), 2):
            output_coords.append(coords[i] + x)
            output_coords.append(coords[i + 1] + y)
        return output_coords
    
    def get_width(self):
        return self.coords[2] - self.coords[0]
    
    def get_height(self):
        return self.coords[3] - self.coords[1]
    
    def print_coordinates(self, coordinates, decimal_places = 2):
        print('Shape ({} sides):'.format(len(coordinates)))
        for x, y in coordinates:
            print('({}, {})'.format(round(x, decimal_places), round(y, decimal_places)))