import cv2 
import numpy as np
from . import config as cfg


class extractImage():

    def __init__(self):
        # Detect the markers in the image
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters()

    def detect_marker(self,image):
        corners, ids, rejected = cv2.aruco.detectMarkers(image, self.aruco_dict, parameters=self.aruco_params)

        return corners, ids, rejected

    def extract(self, image,save = True):
        # image = cv2.imread(image_path)

        corners, ids, rejected = self.detect_marker(image=image)

        if ids is not None and len(ids) == 4:
        # Flatten the ids list
            ids = ids.flatten()

            # Dictionary to store the marker id and its corresponding corners
            marker_corners = {}
            
            for marker_corner, marker_id in zip(corners, ids):
                # Get the corner points of each marker
                marker_corners[marker_id] = marker_corner[0]

            # Sort the marker ids to maintain a consistent order
            sorted_ids = sorted(marker_corners.keys())

            # Get the corners of the markers in order
            pts = np.array([marker_corners[sorted_ids[0]][0], marker_corners[sorted_ids[1]][1],
                            marker_corners[sorted_ids[2]][2], marker_corners[sorted_ids[3]][3]], dtype='float32')

            # Create a blank 990mm x 990mm image
            dpi = cfg.dpi  
            mm_per_inch = cfg.mm_per_inch
            pixels_per_mm = dpi / mm_per_inch
            size_in_pixels = int(990 * pixels_per_mm)
            blank_image = np.zeros((size_in_pixels, size_in_pixels, 3), dtype=np.uint8)

            # Define the destination points (corners of the blank image)
            dst_pts = np.array([[0, 0], [size_in_pixels - 1, 0], [size_in_pixels - 1, size_in_pixels - 1], [0, size_in_pixels - 1]], dtype='float32')

            # Get the actual marker sizes and add padding if necessary
            marker_size = max(np.linalg.norm(pts[0] - pts[1]), np.linalg.norm(pts[1] - pts[2]))
            padding_size = cfg.padding_size
            padding =  int(marker_size / padding_size)

            # Adjust the destination points to ensure markers fit well within the corners with padding
            dst_pts[0] += [padding, padding]
            dst_pts[1] += [-padding, padding]
            dst_pts[2] += [-padding, -padding]
            dst_pts[3] += [padding, -padding]

            # Compute the perspective transform matrix
            M = cv2.getPerspectiveTransform(pts, dst_pts)

            # Warp the original image to the new image size
            warped = cv2.warpPerspective(image, M, (size_in_pixels, size_in_pixels))
            
            return warped
        else:
            print("Could not detect 4 markers.")


if __name__=="__main__": 
    cls = extractImage()
    img =cls.extract("/home/srv/Work/PythonScript/distance_calculation/image/IMG_6893.jpg")
    cv2.imwrite("result/extracted_image.jpg",img)


