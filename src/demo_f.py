import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cv2
from render_img import *

# Give the heigth M and the width N of the canvas and create the inital total white canvas.
M=512
N=512
img=np.ones((M,N,3))

# Load the data from the hw1.npy file and assign the data to variables.
data=np.load('data/hw1.npy',allow_pickle=True)[()]
#d1=np.load('outfile.npy',allow_pickle=True)

vertices=data['vertices']
vcolors=data['vcolors']
depth=data['depth']
faces=data['faces']

# Select how the canvas will be shaded: In this script the choice is "Flat shading"
shading="f"
updated_img=render_img(faces,vertices,vcolors,depth,shading)

plt.figure(1)
fig1=plt.imshow(updated_img)
plt.show()

# Save the image from demo_f.py
image_path='outputs/demo_f_Flat_Shading.png'
updated_img=cv2.convertScaleAbs(updated_img, alpha=(255.0))
updated_img=cv2.cvtColor(updated_img,cv2.COLOR_RGB2BGR)
isDone=cv2.imwrite(image_path,updated_img)
if isDone:
    print("Done!")