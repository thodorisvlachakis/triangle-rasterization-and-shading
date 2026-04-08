import numpy as np
import math
from compute_lines_triangle import *
from sort_vertices import *
# This function takes as input an image that is a canvas of dimension M×N and an RGB vector corresponds to every point of this
# canvas. Also, the function takes as input the integer coordinates of the three vertices of a triangle and their RGB colors.
# Having this triangle and these three RGB vectors, function calculates the RGB vector (i.e the color) that corresponds to the
# trianlge. This RGB vector is a vector mean of the three RGB vectors of the triangle vertices. Function shades the triangle
# giving the above RGB vector to it. So, the image that is outputed by function is same with inputed image apart from this (given)
# triangle that is shaded with the color represented by the calculated RGB vector. 

# INPUTS:
# img : a 3-dimensional array M×Ν×3 which describes the inputed image that is wanted to be updated by the function "f_shading".
#       The third dimension of the array is a vector of length 3 that represents the RGB color of the point (x,y) whose
#       coordinates correspond to the first two dimensions of the array (x at the second and y at the first column, beacause M
#       represents the heigth and N represents the width of the canvas). 
# vertices : an integer array of dimension 3×2 whose each row contains the 2-dimensinal coordinates of a vertex of the triangle.
# vcolors : an array of dimension 3×3 whose each row contains the RGB color (values belong to interval [0,1]) of the
#           corresponding vertex of the triangle.
# OUTPUTS:
# updated_img: a 3-dimensional array M×Ν×3 which describes the outputed image. The third dimension of the array is a vector
#              of length 3 that represents the RGB color of the point (x,y) whose coordinates correspond to the first two
#              dimensions of the array (x at the second and y at the first column). This array contains all the points of the
#              triangle with the calculated RGB vectors and the pre-existing points of the input image, i.e the array img. The
#              pre-existing RGB vectors for points that corresponds to the points of the triangle are getting overlapped by
#              calculated RBG vectors.

def f_shading(img,vertices,vcolors):
    updated_img=img
    N=img.shape[1]
    M=img.shape[0]
    # Declare the color has to be given to the triangle
    color_RGB=(1/3)*( np.asarray(vcolors[0,:]) + np.asarray(vcolors[1,:]) +np.asarray(vcolors[2,:]) )

    sorted_vertices_by_y=sort_vertices(vertices,2)
    
    # Compute the lines that pass through the vertices of the triangle
    # Because of sorting the vertices both the first and the last row of triangle_lines refer to the vertex with the minimum y
    # The first and the second row of triangle_lines refer to the vertex with the "medium" y
    # The second and the last row of triangle_lines refer to the vertex with the maximum y
    triangle_lines=compute_lines_triangle(sorted_vertices_by_y)

    # Compute ymin and ymax for searching lines
    ymin=sorted_vertices_by_y[0,1]
    ymax=sorted_vertices_by_y[2,1]

    # active_lines is a vector of length 3. If its i element is 1 then the i-th line is active for the searching line y.
    # active_lines will be updated during the algorithm execution.
    # active_points is an array of dimension 2×3 whose each row contains the coordinates of the point of intersection of the
    # searching line with the line inclued in some row of triangle_lines, at the first two columns. At the third column there
    # is the characteristic number for the active line which the active point belong to. The characteristic number is: 
    # 0 for active line between vertices "1" and "2" (sorted), 1 for active line between vertices "2" and "3" (sorted),
    # 2 for active line between vertices "1" and "3" (sorted).
    # active_points will be updated during the algorithm execution.
    #active_points=np.array((2,3))

    # Compute active lines for the searching line y=ymin
    active_lines=np.array([1,0,1])

    # Since we have triangle the number of active points for every searching line y between ymin and ymax is 2. For y=ymin
    # and y=ymax there is only one active point (since y min and ymax are integers). For these cases we assume that the
    # active point is double.
    # Compute active points for the searching line y=ymin

    active_points=np.array([ [sorted_vertices_by_y[0,0],sorted_vertices_by_y[0,1], 0],
                           [sorted_vertices_by_y[0,0],sorted_vertices_by_y[0,1], 2] ])
    
    # Check if there are horizontal lines and save this information
    horizontal_lines=np.array([0,0,0])
    for i in range(3):
        if triangle_lines[i,0]==0:
            horizontal_lines[i]=1
            # If a line is horizontal, exclude it from active_lines
            active_lines[i]=0

    # Special case: All the vertices are in the same horizontal line, so there is no actual triangle
    # This is a special case as well as the case where the vertices are in the same vertical line but this case is contained below
    # instead of this case where (1/m)=infinity for all the triangle lines.
    if (horizontal_lines[0]==1 and horizontal_lines[1]==1) or (horizontal_lines[0]==1 and horizontal_lines[2]==1) or (horizontal_lines[1]==1 and horizontal_lines[2]==1) :
        sorted_vertices_by_x=sort_vertices(sorted_vertices_by_y,1)
        x1=sorted_vertices_by_x[0,0]
        x2=sorted_vertices_by_x[2,0]
        for x in range(x1,x2+1):
            updated_img[M-1-x,sorted_vertices_by_y[0,1],:]=color_RGB
        
        return updated_img
    
    # If the line between vertices "1" and "2" (sorted) is horizontal, start scanning from ymin +1 and update active_lines and
    # active_points
    if horizontal_lines[0]==1:
        ymin=ymin+1
        active_lines[1]=1
        # First active point belongs to the line between vertices "1" and "3" (sorted)
        if(np.isinf(triangle_lines[2,0])==False):
            # This is a non-vertical active line
            # Update the active point
            active_points[0,1]=ymin
            active_points[0,0]=active_points[0,0] + 1/triangle_lines[2,0]
            active_points[0,2]=2
        else:
            # This is a vertical active line
            active_points[0,1]=ymin
            active_points[0,0]=active_points[0,0]
            active_points[0,2]=2
        
        # Second active point belongs to the line between vertices "2" and "3" (sorted). This is active point will be calculated
        # by using the vertex "2" (as initial point of this line) which belongs to the same horizontal line with vertex "1" (sorted).
        if(np.isinf(triangle_lines[1,0])==False):
            # This is a non-vertical active line
            # Update the active point
            active_points[1,1]=ymin
            active_points[1,0]=sorted_vertices_by_y[1,0] + 1/triangle_lines[1,0]
            active_points[1,2]=1
        else:
            # This is a vertical active line
            active_points[1,1]=ymin
            active_points[1,0]=sorted_vertices_by_y[1,0]
            active_points[1,2]=1

    # Start scanning by searching lines

    for y in range(ymin,ymax+1):
        # sort active_points by x
        active_points=sort_vertices(active_points,1)
        cross_count=0
        update_now=0
        # Start scanning of search line y
        for x in range (M):
            cross_count=0
            for i in range(active_points.shape[0]):
                if x>=active_points[i,0]:
                    cross_count=cross_count+1
            if (cross_count % 2) !=0:
                # draw pixel
                updated_img[M-1-x,y,:]=color_RGB
        
        # Update the list of active_lines for the next searching line
        
        # First case: The line between vertices "1" and "2" (sorted) is active, but for the next searching line must be excluded.
        # 1st Sub-case: The line between vertices "2" and "3" (sorted) must be included, if and only if is not horizontal. 
        if y<sorted_vertices_by_y[1,1] and (y+1)>=sorted_vertices_by_y[1,1] and horizontal_lines[1]!=1:
            active_lines[0]=0
            active_lines[1]=1
            # Declare a variable to know when update the list of active_lines and which case it is.
            update_now=1
        # 2nd Sub-case: The line between vertices "2" and "3" (sorted) is horizontal, which means that this line is same with 
        # the searcing line y+1 and we assume that it belongs to the triangle "above" the triangle we shade.
        if y<sorted_vertices_by_y[1,1] and (y+1)>=sorted_vertices_by_y[1,1] and horizontal_lines[1]==1:
            active_lines[0]=0
            active_lines[1]=0
            active_lines[2]=0
            # Declare a variable to know when update the list of active_lines and which case it is.
            update_now=2

        # Second case: What happens when y+1=ymax? 
        # 1st Sub-case: Searching line y has active lines both the line between vertices "2" and "3" and the line between vertices
        # "1" and "3" (sorted), respectively. This means that the line between vertices "2" and "3" (sorted) is not horizontal.
        if y+1==ymax and horizontal_lines[1]!=1:
            active_points=np.array([ [sorted_vertices_by_y[2,0],sorted_vertices_by_y[2,1], 1],
                           [sorted_vertices_by_y[2,0],sorted_vertices_by_y[2,1], 2] ])
            update_now=3

        # 2nd Sub-case: Searching line y has active lines both the line between vertices "1" and "2" and the line between vertices
        # "1" and "3" (sorted), respectively. This means that the line between vertices "2" and "3" (sorted) is horizontal. This
        # case is the 2nd Sub-Case of the First case already implemented.

        # Last Case: The current searcing line is y=ymax and there is no need to update for the next searching line
        if y==ymax:
            update_now==4

        # Update the list of active_points for the next searching line
        if update_now==0:
            # This means no update occurred.
            # Find the active line which each active point belongs to and update the active_points for the next searching line.
            for i in range(2):
                for j in range(len(active_lines)):
                    if active_lines[j]==1:
                        if active_points[i,2]==j:
                            # The active line, which the active point belongs to, is found
                            if (np.isinf(triangle_lines[j,0])==False):
                                # This means that the active line is non-vertical
                                active_points[i,0]=active_points[i,0] + 1/triangle_lines[j,0]
                                active_points[i,1]=y+1
                            else:
                                # This means that the active line is vertical
                                # Update only the y-coordinate.
                                active_points[i,1]=y+1

        elif update_now==1:
            # This means that the line between vertices "2" and "3" (sorted) is now active for y+1
            # Find the active point that belongs to the line between vertices "1" and "2" (sorted), because this has to be excluded.
            # Use the characteristic number of the point !!!
            for i in range(2):
                if(active_points[i,2]==0):
                    # The active point, which belongs to the line between vertices "1" and "2" (sorted) and must be excluded, is found.
                    # Include the vertex "2" (sorted) in the active_points.
                    active_points[i,0]=sorted_vertices_by_y[1,0]
                    active_points[i,1]=sorted_vertices_by_y[1,1]
                    active_points[i,2]=1
                elif(active_points[i,2]==2):
                    # This active point belongs to the line between vertices "1" and "3" (sorted) and will be updated classically.
                    if (np.isinf(triangle_lines[2,0])==False):
                         # This means that the active line is non-vertical
                        active_points[i,0]=active_points[i,0] + 1/triangle_lines[2,0]
                        active_points[i,1]=y+1
                    else:
                        # This means that the active line is vertical
                        # Update only the y-coordinate.
                        active_points[i,1]=y+1
                        
        elif update_now==2:
            # In this case the line between vertices "2" and "3" is horizontal and it is assumed that belongs to the "above"
            # triangle, so the scanning process is over.
            y=ymax # This will terminate the "for" loop.
    
    # Last part of shading: Decide on horizontal (if it exists) line between two of three vertices of the triangle.
    # Beacause of "agreement", we assume that if a horizontal line determines an "upper border" of the triangle is not
    # considered to belong to the triangle (it belongs to the "above" triangle). So, if the line between vertices "1" and "2"
    # (sorted) is horizontal , it is considered as part of the triangle. If the line between vertices "2" and "3" (sorted) is 
    # horizontal, it is ont considered as part of the triangle.
    # Note: Because of sorting the vertices by y, the line between vertices "1" and "3" (sorted) can't be horizontal !!!
    if horizontal_lines[0]==1:
        # This means that the vertices "1" and "2" (sorted) has the same y(=ymin) coordinate
        if sorted_vertices_by_y[0,0]<=sorted_vertices_by_y[1,0]:
            x1=sorted_vertices_by_y[0,0]
            x2=sorted_vertices_by_y[1,0]
        else:
            x1=sorted_vertices_by_y[1,0]
            x2=sorted_vertices_by_y[0,0]
        for x in range(x1,x2):
            updated_img[M-1-x,sorted_vertices_by_y[0,1],:]=color_RGB

    return updated_img