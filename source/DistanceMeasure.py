from ApplyGrid import applyGrid
from CircleDetection import circleDetection
from ExtractImage import extractImage
import numpy as np
import config as cfg
import cv2
import argparse
import os

class distanceMeasure():
    def __init__(self):
        self.dpi = cfg.dpi  # Assuming the DPI (dots per inch) is 300
        self.mm_per_inch = cfg.mm_per_inch
        self.pixels_per_mm = self.dpi / self.mm_per_inch
        self.extractionClass = extractImage()
        self.gridClass = applyGrid()
        self.circleDetectionClass = circleDetection()

    def get_utils(self, image_path):
        self.wraped_img = self.extractionClass.extract(image_path=image_path)
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
    
    def draw_distance(self, save=True):
        image = self.wraped_img.copy()
        circle_dict = self.get_dict()

        for key_c in circle_dict.keys():
            min_dist = float('inf')
            closest_grid_point = key_c

            for grid_point in circle_dict[key_c]:
                grid_coords = list(grid_point.keys())[0]
                dist = grid_point[grid_coords]
                if dist < min_dist:
                    min_dist = dist
                    closest_grid_point = grid_coords

            cv2.circle(image, key_c[:-1], cfg.distance_circle_radius, (255, 255, 255), cfg.distance_circle_thickness)
            cv2.circle(image, closest_grid_point, cfg.distance_circle_radius, (0, 0, 255), cfg.distance_circle_thickness)
            cv2.circle(image, key_c[:-1], key_c[-1], (255, 0, 0), cfg.distance_circle_thickness)
            cv2.line(image, key_c[:-1], closest_grid_point, (0, 255, 0), 9)

            # Adding text with coordinates and distance
            text = f'({key_c[0] / self.pixels_per_mm:.2f}, {key_c[1] / self.pixels_per_mm:.2f}) mm'
            text_position_circle = (key_c[0], key_c[1] - 10)
            cv2.putText(image, text, text_position_circle, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            text = f'({closest_grid_point[0] / self.pixels_per_mm:.2f}, {closest_grid_point[1] / self.pixels_per_mm:.2f}) mm'
            text_position_grid = (closest_grid_point[0], closest_grid_point[1] - 10)
            cv2.putText(image, text, text_position_grid, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            distance_text = f'{min_dist:.2f} mm'
            mid_point = ((key_c[0] + closest_grid_point[0]) // 2, (key_c[1] + closest_grid_point[1]) // 2)
            cv2.putText(image, distance_text, mid_point, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if save:
            if not os.path.exists("result"):
                os.makedirs("result")
            result_path = "result/distance_mm.jpg"
            print(f"Saving image to {result_path}")
            success = cv2.imwrite(result_path, image)
            if not success:
                print("Failed to save image")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Measure distances in an image")
    parser.add_argument("image_path", type=str, help="Path to the image file")
    parser.add_argument("--save", action="store_true", help="Save the result image")

    args = parser.parse_args()

    cls = distanceMeasure()
    cls.get_utils(image_path=args.image_path)
    cls.draw_distance(save=args.save)
