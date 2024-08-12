import numpy as np 
import cv2 
from . import config as cfg


class applyGrid():
    
    def __init__(self):
        self.x_grid_sizes = cfg.x_grid_sizes
        self.y_grid_sizes = cfg.y_grid_sizes

        # Calculate the number of grid points
        self.x_points = len(self.x_grid_sizes) + 1
        self.y_points = len(self.y_grid_sizes) + 1

        # Initialize the image
        self.dpi = cfg.dpi
        self.mm_per_inch = cfg.mm_per_inch
        self.pixels_per_mm = self.dpi / self.mm_per_inch
        self.image_size = int(990 * self.pixels_per_mm)

    def get_corrdinates(self):

        # Calculate the pixel positions for the grid lines
        x_positions = np.cumsum([0] + self.x_grid_sizes) * self.pixels_per_mm
        y_positions = np.cumsum([0] + self.y_grid_sizes) * self.pixels_per_mm

        return x_positions , y_positions
        
    def get_grid(self,image, with_points= True, save= True):
        x_positions , y_positions = self.get_corrdinates()

        if with_points:
            # Draw the grid lines
            for x in x_positions:
                cv2.line(image, (int(x), 0), (int(x), self.image_size), cfg.grid_line_color, cfg.grid_line_thickness)
            for y in y_positions:
                cv2.line(image, (0, int(y)), (self.image_size, int(y)), cfg.grid_line_color, cfg.grid_line_thickness)
            # Print the x, y values of each matching point and mark them on the image
            for i, x in enumerate(x_positions):
                for j, y in enumerate(y_positions):
                    x_mm = x / self.pixels_per_mm
                    # y_mm = (image_size - y) / pixels_per_mm  # Adjust to start y from the bottom
                    y_mm = y/self.pixels_per_mm
                    text = f'x={x_mm:.1f}mm, y={round(y_mm):.1f}mm'
                    cv2.circle(image, (int(x), int(y)), cfg.grid_circle_radius, cfg.grid_circle_color, cfg.grid_circle_thickness)
                    cv2.putText(image, text, (int(x) + 10, int(y) - 10), cfg.grid_font, cfg.grid_font_scale, cfg.grid_font_color, cfg.grid_font_thickness)

        else: 
            # Draw the grid lines
            for x in x_positions:
                cv2.line(image, (int(x), 0), (int(x), self.image_size), cfg.grid_line_color, cfg.grid_line_thickness)
            for y in y_positions:
                cv2.line(image, (0, int(y)), (self.image_size, int(y)), cfg.grid_line_color, cfg.grid_line_thickness)


        if save: 
            cv2.imwrite("result/990mm_x_990mm_grid.jpg", image)

        else: 
            cv2.imshow("990mm x 990mm Grid", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


if __name__=="__main__": 
    cls = applyGrid()
    image = cv2.imread("/home/srv/Work/PythonScript/distance_calculation/source/result/extracted_image.jpg")
    cls.get_grid(image, with_points= True, save= True)

    # img =cls. extract("/home/srv/Work/PythonScript/distance_calculation/image/IMG_6893.jpg")
    # cv2.imwrite("result/extracted_image.jpg",img)




        



