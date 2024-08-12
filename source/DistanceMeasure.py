from .ApplyGrid import applyGrid
from .CircleDetection import circleDetection
from .ExtractImage import extractImage
import numpy as np
from . import config as cfg
import cv2
import random
import json
import base64

class distanceMeasure():
    def __init__(self):
        self.final_dict = {}
        self.dpi = cfg.dpi 
        self.mm_per_inch = cfg.mm_per_inch
        self.pixels_per_mm = self.dpi / self.mm_per_inch
        self.extractionClass = extractImage()
        self.gridClass = applyGrid()
        self.circleDetectionClass = circleDetection()
    def convert_to_mm(self, value ):
        return value/ self.pixels_per_mm

    def add_to_final_dict(self, default, estimated, index):
            
            threshold = cfg.threshold
            target = cfg.target
            min_threshold = threshold
            max_threshold = threshold + target

            x_n = f"x_{index+1}"
            y_n = f"y_{index+1}"
            x_diff = self.convert_to_mm(default[0]) - self.convert_to_mm(estimated[0])
            y_diff = self.convert_to_mm(default[1]) - self.convert_to_mm(estimated[1])

            self.final_dict[x_n] ={
                                    "default" : self.convert_to_mm(default[0]),
                                    "estimated" : self.convert_to_mm(estimated[0]),
                                    "difference": x_diff,
                                    "threshold": threshold,
                                    "target" : target ,
                                    "result" : 0 if (x_diff >= -min_threshold and x_diff < min_threshold) and (x_diff >= -max_threshold and x_diff < max_threshold) else 1

                                    }
            self.final_dict[y_n] ={
                                    "default" : self.convert_to_mm(default[1]),
                                    "estimated" : self.convert_to_mm(estimated[1]),
                                    "difference": y_diff,
                                    "threshold": threshold,
                                    "target" : target, 
                                    "result" : 0 if (y_diff >= -min_threshold and y_diff < min_threshold) and (y_diff >= -max_threshold and y_diff < max_threshold) else 1
                                    }


    def get_utils(self, image):
        self.wraped_img = self.extractionClass.extract(image=image)
        self.grid_coordinate = self.gridClass.get_corrdinates()
        self.circle_centers = self.circleDetectionClass.detect(self.wraped_img)

    def get_distance(self, x1, x2, y1, y2):
        distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return distance
    
    def get_dict(self):
        circle_dict = {}
        x_positions, y_positions = self.grid_coordinate

        for (x_c, y_c, r_c) in self.circle_centers:
            x_mm_circle = x_c / self.pixels_per_mm
            y_mm_circle = y_c / self.pixels_per_mm
            r_mm = r_c / self.pixels_per_mm
            grids = []
            for i, x_g in enumerate(x_positions):
                for j, y_g in enumerate(y_positions):
                    x_mm_grid = x_g / self.pixels_per_mm
                    y_mm_grid = y_g / self.pixels_per_mm
                    distance = self.get_distance(x_mm_circle, x_mm_grid, y_mm_circle, y_mm_grid)
                    grids.append({(int(x_g), int(y_g)): distance})
        
            circle_dict[(int(x_c), int(y_c), int(r_c))] = grids

        return circle_dict
    
    def draw_distance(self, save=True, encode = True):
        image = self.wraped_img.copy()
        circle_dict = self.get_dict()

        for index , key_c in enumerate(circle_dict.keys()):
            min_dist = float('inf')
            closest_grid_point = key_c

            # Generate a random color for each circle
            circle_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            for grid_point in circle_dict[key_c]:
                grid_coords = list(grid_point.keys())[0]
                dist = grid_point[grid_coords]
                if dist < min_dist:
                    min_dist = dist
                    closest_grid_point = grid_coords
            
            self.add_to_final_dict(closest_grid_point, key_c, index)

            # draw cicle center coodinate
            cv2.circle(image, key_c[:-1], cfg.distance_circle_radius, (255, 255, 255), cfg.distance_circle_thickness)
            # draw grid center coordinate
            cv2.circle(image, closest_grid_point, cfg.distance_circle_radius, (0, 0, 255), cfg.distance_circle_thickness)
            # draw circle
            cv2.circle(image, key_c[:-1], key_c[-1], circle_color, 50)
            # draw distance between cicle coodinate and grid coordinate
            cv2.line(image, key_c[:-1], closest_grid_point, (0, 255, 0), 9)

            # Adding text with circle center coordinates
            text = f'({key_c[0] / self.pixels_per_mm:.2f}, {key_c[1] / self.pixels_per_mm:.2f}) mm'
            text_position_circle = (key_c[0], key_c[1] - 10)
            # cv2.putText(image, text, text_position_circle, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Adding text with grid center coordinate
            text = f'({closest_grid_point[0] / self.pixels_per_mm:.2f}, {closest_grid_point[1] / self.pixels_per_mm:.2f}) mm'
            text_position_grid = (closest_grid_point[0], closest_grid_point[1] - 10)
            # cv2.putText(image, text, text_position_grid, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Adding text with distance between circle center coordinate and grid center coordinate
            distance_text = f'{min_dist:.2f} mm'
            mid_point = (((key_c[0] + closest_grid_point[0]) // 2)+2, ((key_c[1] + closest_grid_point[1]) // 2)+2)
            cv2.putText(image, distance_text, mid_point, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if save:
            # save to the local dir
            cv2.imwrite("result/distance_mm.jpg", image)
            
            # decode  the image
            _, buffer = cv2.imencode('.jpg', image)
            img_base64 = base64.b64encode(buffer).decode('utf-8')

            # returnable json
            return_json = {"image": img_base64,
                           "json": self.final_dict }
            # with open("result/final.json", "w") as outfile:
                # json.dump(self.final_dict, outfile)
            return return_json
            

if __name__ == "__main__":
    cls = distanceMeasure()
    img_path = "/home/srv/Work/PythonScript/distance_calculation/image/IMG_6893.jpg"
    img = cv2.imread(img_path)
    cls.get_utils(image=img_path)
    cls.draw_distance()
