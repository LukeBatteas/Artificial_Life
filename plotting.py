import itertools
import cv2
import os
import numpy as np

#User defined variables
name = "my_image_name" + ".png" #Name of the exported file
margin = 20 #Margin between pictures in pixels
w = 10 # Width of the matrix (nb of images)
h = 10 # Height of the matrix (nb of images)
n = w*h

filename_list = []

numbers = []

local_folder = "fingers"
final_folder = "lab_5_plots/temp_imgs_2/"

for file in os.listdir("rigid_body/"+local_folder+"/gen0/pop0"):
    if file.endswith(".png"):
        numbers.append(int(file.strip(".png")))

numbers.sort()

length = len(numbers)

m = 0

# If the memory runs out can use this
# upper = 20*m+20
# if(upper > length):
#     upper = length
for k in range(20*m, length):
    print(int(100*(k+1)/length), "%")

    for i in range(w):
        for j in range(h):
            filename_list.append("gen"+str(i)+"/pop"+str(j))

    imgs = [cv2.imread("rigid_body/"+local_folder+"/"+file+"/"+str(numbers[k]).zfill(4)+".png") for file in filename_list]

    #Define the shape of the image to be replicated (all images should have the same shape)
    img_h, img_w, img_c = imgs[0].shape

    #Define the margins in x and y directions
    m_x = margin
    m_y = margin

    #Size of the full size image
    mat_x = img_w * w + m_x * (w - 1)
    mat_y = img_h * h + m_y * (h - 1)

    #Create a matrix of zeros of the right size and fill with 255 (so margins end up white)
    imgmatrix = np.zeros((mat_y, mat_x, img_c),np.uint8)
    imgmatrix.fill(255)

    #Prepare an iterable with the right dimensions
    positions = itertools.product(range(h), range(w))

    for (y_i, x_i), img in zip(positions, imgs):
        x = x_i * (img_w + m_x)
        y = y_i * (img_h + m_y)
        imgmatrix[y:y+img_h, x:x+img_w, :] = img

    resized = cv2.resize(imgmatrix, (mat_x//3,mat_y//3), interpolation = cv2.INTER_AREA)
    compression_params = [cv2.IMWRITE_JPEG_QUALITY, 90]
    cv2.imwrite(final_folder+str(k)+".png", resized, compression_params)