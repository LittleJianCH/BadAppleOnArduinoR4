import cv2
import numpy as np

video = cv2.VideoCapture('../video/Bad_Apple.mp4')


rows = 8
cols = 12

width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
rate = int(video.get(cv2.CAP_PROP_FPS))

region_height = height // rows
region_width = width // cols

print("Video Resolution: {}x{}".format(width, height))
print("Frame Count: {}".format(count))
print("Frame Duration: {}".format(1.0 / rate))


result = []
while video.isOpened():
    ret, frame = video.read()
    
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    matrix = np.zeros((rows, cols), dtype=np.uint8)
    
    for i in range(rows):
        for j in range(cols):
            start_row = i * region_height
            end_row = min((i + 1) * region_height, height)
            start_col = j * region_width
            end_col = min((j + 1) * region_width, width)
            
            region = gray[start_row:end_row, start_col:end_col]
            
            black_pixels = np.count_nonzero(region == 0)
            white_pixels = np.count_nonzero(region == 255)
            
            if black_pixels > white_pixels:
                matrix[i, j] = 1 # light
            else:
                matrix[i, j] = 0

    vector = matrix.flatten();
    matrix = np.reshape(vector, (-1, 32))

    numbers = []
    for vec in matrix:
        num = 0
        for x in vec:
            num = num * 2 + x
        numbers.append(num)

    result.append(numbers)

video.release()

f = open("../arduino/Bad_Apple.h", "w")

f.write("const unsigned long frames[" + str(len(result)) + "][3] = {")
for tup in result:
    f.write("{" + str(tup[0]) + ", " + str(tup[1]) + ", " + str(tup[2]) + "}, ")
f.write("};")
