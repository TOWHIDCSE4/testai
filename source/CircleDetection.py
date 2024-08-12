import cv2
import numpy as np
from ultralytics import YOLO
from . import config as cfg


class circleDetection():

    def __init__(self):
        self.dpi = cfg.dpi  # Assuming the DPI (dots per inch) is 300
        self.mm_per_inch = cfg. mm_per_inch
        self.pixels_per_mm = self.dpi / self.mm_per_inch
        self.model = YOLO(cfg.ckpt_path)

    def detect(self, image):
        self.output = image.copy()
        circle_centers = []
        results = self.model(self.output)
        boxes = results[0].boxes.xyxy
        for box in boxes:
            x_min, y_min , x_max, y_max = box
            
            x_min = int(x_min)
            y_min = int(y_min)
            x_max = int(x_max)
            y_max = int(y_max)

            x_center = (x_min+ x_max) / 2
            y_center = (y_min+ y_max) / 2

            radius = int(min(x_max - x_min, y_max - y_min) / 2)
            circle_centers.append((int(x_center),int(y_center),int(radius)))

        return circle_centers
        
    def draw_circle(self,circle_centers, save = True):
        for (x,y,r) in circle_centers:
            cv2.circle(self.output, (x, y), r, (0, 255, 0), 10)
            cv2.rectangle(self.output, (x - 5, y - 5), (x + 5, y + 5), (0, 135, 255), -1)
            
            x_mm = x / self.pixels_per_mm
            y_mm = y / self.pixels_per_mm
            r_mm = r / self.pixels_per_mm

            # Plot the center coordinates in mm on the image
            text = f'({x_mm:.2f}mm, {y_mm:.2f}mm)'
            cv2.putText(self.output, text, (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        if save:
            cv2.imwrite("result/detect_with_mm.jpg", self.output)
        else: 
            cv2.imshow("990mm x 990mm Grid", self.output)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


if __name__=="__main__": 
    cls = circleDetection()
    img_path ="/home/srv/Work/PythonScript/distance_calculation/source/result/extracted_image.jpg"
    img = cv2.imread(img_path)
    circles = cls.detect(image=img)
    cls.draw_circle(circle_centers=circles)







    # def detect(self, image):
    #     self.output = image.copy()
    #     circle_centers = []
    #     # Convert the image to grayscale
    #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #     # Apply GaussianBlur to reduce noise and improve circle detection
    #     gray_blurred = cv2.GaussianBlur(gray, (15, 15), 1)
    #     print(cfg.dp)

    #     # Apply Hough Circle Transform to detect circles
    #     detected_circles = cv2.HoughCircles(gray_blurred, 
    #                                         cv2.HOUGH_GRADIENT,
    #                                         dp=cfg.dp,
    #                                         minDist=cfg.minDist,
    #                                         param1=cfg.param1,
    #                                         param2=cfg.param2, 
    #                                         minRadius=cfg.minRadius, 
    #                                         maxRadius=cfg.maxRadius)
        
    #     if detected_circles is not None:

    #         detected_circles = np.uint16(np.around(detected_circles))
    #         for (x, y, r) in detected_circles[0, :]:
    #             # y = (image_size - y)
    #             circle_centers.append((x, y, r))
    #             # cv2.circle(output, (x, y), r, (0, 255, 0), 10)
    #             # cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 135, 255), -1)
    #         return circle_centers