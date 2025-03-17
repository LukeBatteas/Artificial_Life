import cv2
import numpy as np


folder = "lab_5_plots/temp_imgs_2/"
num_imgs = 62
  
# choose codec according to format needed
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
img0 = cv2.imread(folder+str(0) + '.png')
video = cv2.VideoWriter('final_2.avi', fourcc, 10, (img0.shape[0], img0.shape[1]))

for i in range(num_imgs):
    img = cv2.imread(folder+str(i) + '.png')
    video.write(img)

cv2.destroyAllWindows()
video.release()