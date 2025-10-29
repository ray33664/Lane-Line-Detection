# ============================================
# Lane Line Detection Project (Image-based)
# Author: Emily Willis (Ray Sensei)
# ============================================

import cv2
import numpy as np
import os

# Step 1: Create input and output folders if missing
os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Step 2: Define region of interest
def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([
        [(100, height), (image.shape[1]-100, height), (image.shape[1]//2, int(height/2) + 50)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked = cv2.bitwise_and(image, mask)
    return masked

# Step 3: Detect edges using Canny
def detect_edges(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    return edges

# Step 4: Detect and draw lines
def detect_lines(image, original):
    lines = cv2.HoughLinesP(image, 1, np.pi/180, 50, minLineLength=100, maxLineGap=50)
    line_image = np.zeros_like(original)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 5)
    combined = cv2.addWeighted(original, 0.8, line_image, 1, 1)
    return combined

# Step 5: Process image
def process_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("❌ Error: Could not read image. Make sure road.jpg is in the 'input' folder.")
        return
    edges = detect_edges(image)
    cropped = region_of_interest(edges)
    result = detect_lines(cropped, image)
    output_path = os.path.join("output", "lane_output.jpg")
    cv2.imwrite(output_path, result)
    print(f"✅ Lane-detected image saved at: {output_path}")
    cv2.imshow("Lane Detection Result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Step 6: Run the program
input_image_path = os.path.join("input", "road.jpg")
process_image(input_image_path)
