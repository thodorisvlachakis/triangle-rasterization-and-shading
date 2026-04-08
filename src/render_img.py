import numpy as np
import math
from f_shading import *
from g_shading import *
# This function is called Object Coloring function. The Object Coloring Function forms an object on a white canvas and stores 
# this result (that is, this image) in a 3D array, which is also the output of the function. The Color Object Function creates
# a “canvas” of dimensions M×N (where M=N=512), which it initializes as a white canvas. The function takes as input a number of
# vertices that define a number of triangles on this canvas. The set of these triangles may form an object and in any case it
# is the set of triangles, to which the Triangle Filling Algorithm will be applied to form the object on the white canvas.
# It is assumed that this object is an object of three-dimensional space, which is projected in two dimensions. In this context,
# each of the vertices given as an argument is characterized by an integer, which indicates the depth of the corresponding
# vertex before projecting the object in two dimensions. Also, to each of these peaks corresponds a vector of three color
# components that represents the color of that vertex. Having arrays for all these "data", as well as an array defining the
# triangles (that is, which vertices from the set of vertices, that is, from the array that has the 2D coordinates of each
# vertex of the given set of vertices stored, form each triangle) the Function Object Painter computes a 3D matrix of dimensions
# M×N×3, which models an image, on which the white canvas initialized by the function is depicted and on which the object
# denoted by the triangles given as input parameters is formed. How the object is colored, that is, each of the triangles that
# make up that object, is determined by an input parameter to the function, the shading variable. This variable states, if the
# coloring mode is chosen to be the one defined by the Flat Shading Function or the one defined by the Gouraud Shading Function,
# in which case the corresponding routine inside this function is called. Additionally, the Object Coloring Function chooses to
# calculate, first, the vectors corresponding to the colors of the points of triangles with greater depth (i.e. triangles that
# are further away in the three-dimensional space) and therefore to "color" the triangles with greater depth first , i.e. the
# most distant triangles in 3D space. We note that the depth of a triangle corresponds to the center of gravity of the depth of
# the three vertices that define the triangle. So, in order to achieve the coloring, first, of the most "distant" triangles, the
# Object Coloring Function first calculates a depth_triangles vector of length K (assuming that K is the number of triangles
# described in the faces table and thus given as input to function), whose i-th element corresponds to the depth of the triangle
# defined by the three vertices defined by the i-th line of the faces array. The function then sorts the depth_triangles array
# in descending order of values. Any change that occurs in elements of the depth_triangles array also occurs in the rows of the
# faces array (each row refers to the vertices that define the triangle, whose depth is represented in the corresponding
# element of the depth_triangles array) since the i-th row of the faces array corresponds to the i-th element of the depth_triangles
# array, in the sense that that element contains the information about the depth of the triangle, so even after sorting the
# depth_triangles array, the matching of the i-th row of the faces array with the i-th element of the depth_triangles array to
# be preserved. In this way the Object Coloring Function achieves the sorting of the triangles described in the faces table in
# descending order of triangle depth value. Thus, depending on the value of the shading variable (“f” or “g”) the function is called
# iteratively (running one by one the lines of the faces table from the 1st to the Kth and thus satisfying the requirement for
# coloring first the "longer" triangles) f_shading or g_shading, respectively, giving as argument the current state of the canvas,
# the vertices defined by the faces array and whose coordinates are stored in the vertices array, as well as the corresponding
# colors of these vertices from the vcolors table and taking as output the "refreshed" state of the canvas after and the
# coloring of the particular triangle.

# INPUTS:
# img : a 3-dimensional array M×Ν×3 which describes the inputed image that is wanted to be updated by the function "f_shading".
#       The third dimension of the array is a vector of length 3 that represents the RGB color of the point (x,y) whose
#       coordinates correspond to the first two dimensions of the array. 
# faces : A matrix of dimension K×3, each row of which includes the three vertices that define a triangle. Each element of a
#         line of this array is a number, from 0 to L-1, that acts as a pointer to the corresponding line of the vertices array
#         in which the coordinates of the vertices are stored.
# vertices : An L×2 array, each row of which contains the 2D coordinates of a vertex (which we assume is inside the canvas).
#            In the first column of the table are stored the x-intercepts of the vertices and in the second column the
#            y-ordinates of the vertices.
# vcolors : An array of dimension L×3, each line of which includes the color coordinates (R,G,B) of the corresponding vertex of
#           the triangle declared in the corresponding line of the vertices array.
# depth : An array of dimension L×1, each element of which declares the depth of the corresponding vertex (the depth it has in
#         the three-dimensional space before the projection in the two dimensions), which is declared in the corresponding row
#          of thevertices array.
# shading : A variable that specifies how to color the triangles, i.e. whether to use the f_shading or g_shading coloring
#           function. Valid values ​​it takes are “f” (for f_shading) and “g” (for g_shading).

# OUTPUTS:
# img: a 3-dimensional array M×Ν×3 which describes the outputed image. The third dimension of the array is a vector
#      of length 3 that represents the RGB color of the point (x,y) whose coordinates correspond to the first two
#      dimensions of the array. This array contains all the points of the final image defined by the K triangles that are
#      given as input of the function, with the calculated RGB vector for each point.


def render_img(faces,vertices,vcolors,depth,shading):
    M=512
    N=512
    # Declare image img as a canvas which is totally white, at first
    img=np.ones((M,N,3))
    
    if shading!="f" and shading!="g":
        return ["Invalid value for variable shading",img]
    
    # Define depth_triangles.
    # depth_triangles: a vector of length K whose i-th element describes the depth of the i-th triangle which is described in
    #                  the i-th row of the array faces. The depth of a triangle is the center of gravity of the depth of its 
    #                  three vertices.
    depth_triangles=np.zeros(faces.shape[0])
    for i in range(faces.shape[0]):
        f=faces[i,0]
        s=faces[i,1]
        t=faces[i,2]
        depth_triangles[i]=(1/3)*( depth[f] + depth[s] + depth[t] )

    # Sort the vector depth_triangles in descending order of "depth". Also, the rows of the array faces will change order in
    # the same way as the elements of the vector depth_triangles which they correspond to.
    for i in range(len(depth_triangles)-1):
        max=depth_triangles[i]
        s=-1
        for j in range(i+1,len(depth_triangles)):
            if depth_triangles[j]>max:
                max=depth_triangles[j]
                # declare maximum's position
                s=j
        # swap
        if s!=-1:
            # swap the elements of the vector depth_triangle
            depth_triangles[i], depth_triangles[s]=depth_triangles[s], depth_triangles[i]
            # swap the rows of the array faces
            faces[[i,s]]=faces[[s,i]]

    # Since the triangles, which have to be shaded, are sorted in descending order of "depth", we start shading the triangles
    # on the (image) img accesssing the array faces (it is sorted, now) from row "0" to "K-1" (it has K rows).
    for i in range(faces.shape[0]):
        # Declare which are the vertices of the tringle that will be shaded in i-th iteration
        f=faces[i,0]
        s=faces[i,1]
        t=faces[i,2]
        # Define the triangle by its vertices !!!
        temp_vertices=np.array([ [vertices[f,0], vertices[f,1]], [vertices[s,0], vertices[s,1]], [vertices[t,0], vertices[t,1]] ])
        
        # Define the colors of each vertex of the triangle defined above.
        temp_colors=np.array([ [vcolors[f,0], vcolors[f,1], vcolors[f,2]], [vcolors[s,0], vcolors[s,1], vcolors[s,2]],
                     [vcolors[t,0], vcolors[t,1], vcolors[t,2]] ])
        
        # Now, shade the triangle in the image img considering how you should shade.
        if shading=="f":
            img=f_shading(img,temp_vertices,temp_colors)
        elif shading=="g":
            img=g_shading(img,temp_vertices,temp_colors)
    
    return img
