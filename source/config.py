import cv2
dpi=300
mm_per_inch = 25.4

padding_size = 8

# Grid
x_grid_sizes = [120, 190, 190, 190, 180, 120]
y_grid_sizes = [120, 190, 190, 190, 180, 120]
# Define text properties
grid_font = cv2.FONT_HERSHEY_SIMPLEX
grid_font_scale = 3
grid_font_color = (255, 255, 255)  # White color for text
grid_font_thickness = 5
# Define line and circle properties
grid_line_color = (0, 255, 0)  # Green color for grid lines
grid_line_thickness = 3  # Thickness of the grid lines
grid_circle_color = (0, 0, 255)  # Red color for circles
grid_circle_radius = 10  # Radius of the circles
grid_circle_thickness = 2  # Thickness of the circle edges

# Define circle parameters
ckpt_path="/home/mahedi/projects/personal project/towhid_sourob/full project/testai/best.pt"
dp=1.30
minDist=2100
param1=48
param2=30 
minRadius=200 
maxRadius=210

# Distance 
distance_circle_radius= 5
distance_circle_thickness =10
threshold = 2.5
target = 1