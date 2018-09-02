import json
import os
import math
import numpy

class Scene:
    def __init__(self, path):
        self.path = path
        
        self.manifest = {}
        self.materials = {}
        self.models = {}
        self.bsp = []
        
        self.load_manifest()
        self.load_assets()
        
        with open(os.path.join(self.path, 'scene.json'), 'r') as file:
            self.scene = json.load(file)
        
    def render(self, display):
        self.populate_bsp()
        self.apply_camera_data()
        self.zbuffer_bsp()
        
        for poly in self.bsp:
            display.draw(self.poly_to_scrcoords(poly['coordinates'], display), poly['material data']['colour'], ['scene render'])
    
    def load_assets(self):
        self.load_materials()
        self.load_models()
    
    def load_materials(self):
        for mat_name in self.manifest['materials']:
            with open(os.path.join(self.path, self.manifest['materials'][mat_name]), 'r') as file:
                self.materials[mat_name] = json.load(file)
    
    def load_models(self):  
        for mdl_name in self.manifest['models']:
            with open(os.path.join(self.path, self.manifest['models'][mdl_name]), 'r') as file:
                mdl = json.load(file)
                
            for i in range(len(mdl['polygons'])):
                mdl['polygons'][i]['material data'] = self.materials[mdl['polygons'][i]['material']]
                
            self.models[mdl_name] = mdl
    
    def load_manifest(self):
        with open(os.path.join(self.path, 'manifest.json'), 'r') as file:
            self.manifest = json.load(file)
    
    def populate_bsp(self):
        self.bsp = []
        for model in self.scene['scene']['models']:
            for poly in self.models[model['model']]['polygons']:
                transformed_poly = []
                for x, y, z in poly['coordinates']:
                    transformed_poly.append(self.tools.transform(*self.tools.scale(*self.tools.rotate(x, y, z, *model['rotation']), *model['scale']), *model['coords']))
                self.bsp.append({'coordinates': transformed_poly,
                                 'material data': self.materials[poly['material']]})
        
        for brush in self.scene['scene']['brushes']:
            self.bsp.append({'coordinates': brush['coords'],
                             'material data': self.materials[brush['material']]})
        
        #### code for checking for intersecting polygons goes here (IN FUTURE)
    
    def apply_camera_data(self):
        for poly in self.bsp:
            new_coordinates = []
            for x, y, z in poly['coordinates']:
                new_coordinates.append(self.tools.rotate(*self.tools.transform(x, y, z,  0 - self.scene['camera']['coords'][0], 0 - self.scene['camera']['coords'][1], 0 - self.scene['camera']['coords'][2]), self.scene['camera']['rotation'][0], self.scene['camera']['rotation'][1], self.scene['camera']['rotation'][2]))
            poly['coordinates'] = new_coordinates
    
    def poly_to_scrcoords(self, coords, display):
        output_coords = []
        for x, y, z in coords:
            x, y = self.scenecoords_to_scrcoords(x, y, z, display)
            output_coords.append([x, y])
        return output_coords
            
    def scenecoords_to_scrcoords(self, x, y, z, display):
        #find fov and vertical fov
        fov = self.scene['camera']['fov'] * 2
        vertical_fov = fov * (display.get_height() / display.get_width())
        
        if z <= 0: #point is behind camera
            return 0 - ((x / z) * (360 / fov)), 0 - ((y / z) * (360 / vertical_fov))
        return (x / z) * (360 / fov), (y / z) * (360 / vertical_fov)
    
    def zbuffer_bsp(self):
        for poly in self.bsp:
            all_r = []
            for x, y, z in poly['coordinates']:
                all_r.append(math.hypot(x, math.hypot(y, z)))
            poly['r'] = sum(all_r) / len(all_r)
        
        self.bsp.sort(key = lambda poly: poly['r'], reverse = True)
    
    class tools:
        def transform(x0, y0, z0, x1, y1, z1):
            return [x0 + x1, y0 + y1, z0 + z1]
        
        def rotate(x, y, z, xrot, yrot, zrot):
            #convert to radians
            xrot = math.radians(xrot)
            yrot = math.radians(yrot)
            zrot = math.radians(zrot)
            
            #shorten function names
            cos = math.cos
            sin = math.sin
        
            #x rotation
            mat_x = numpy.matrix([[1, 0, 0],
                                  [0, cos(xrot), 0 - sin(xrot)],
                                  [0, sin(xrot), cos(xrot)]])
            
            #y rotation
            mat_y = numpy.matrix([[cos(yrot), 0, sin(yrot)],
                                  [0, 1, 0],
                                  [0 - sin(yrot), 0, cos(yrot)]])
            
            #z rotation
            mat_z = numpy.matrix([[cos(zrot), 0 - sin(zrot), 0],
                                  [sin(zrot), cos(zrot), 0],
                                  [0, 0, 1]])
            
            #all rotations
            out = mat_x * mat_y * mat_z * numpy.matrix([[x], [y], [z]])
            
            x, y, z = out.tolist()
            x, y, z = x[0], y[0], z[0]
            return x, y, z
        
        def scale(x, y, z, scale_x, scale_y, scale_z):
            return x * scale_x, y * scale_y, z * scale_z