#!/usr/bin/env python

import cv2
import numpy as np
from utils import get_four_points


if __name__ == '__main__' :
    def mouse_handler(event, x, y, flags, data) :
    
        if event == cv2.EVENT_LBUTTONDOWN :
            cv2.circle(data['im'], (x,y),3, (0,0,255), 5, 16);
            cv2.imshow("Image", data['im']);
            if len(data['points']) < 4 :
                data['points'].append([x,y])

    def get_four_points(im):
    
        # Set up data to send to mouse handler
        data = {}
        data['im'] = im.copy()
        data['points'] = []
    
        #Set the callback function for any mouse event
        cv2.imshow("Image",im)
        cv2.setMouseCallback("Image", mouse_handler, data)
        cv2.waitKey(0)
    
        # Convert array to np.array
        points = np.vstack(data['points']).astype(float)
    
        return points

    # Read in the image.
    im_src = cv2.imread("book1.jpg")
    # Destination image
    size = (300,400,3)

    im_dst = np.zeros(size, np.uint8)

    
    pts_dst = np.array(
                       [
                        [0,0],
                        [size[0] - 1, 0],
                        [size[0] - 1, size[1] -1],
                        [0, size[1] - 1 ]
                        ], dtype=float
                       )
    
    
    # print '''
    #     Click on the four corners of the book -- top left first and
    #     bottom left last -- and then hit ENTER
    #     '''
    
    # Show image and wait for 4 clicks.
    if im_src is None:
        print("Error loading image!")
        exit()
    else:
        
        cv2.imshow("Image", im_src)
        # pts_src = get_four_points(im_src);
        
        # # for book1 points
        pts_src = np.array([
            [320., 260.],
            [535., 375.],
            [320., 670.],
            [75., 475.]
        ])
        print(pts_src)
        # Calculate the homography
        h, status = cv2.findHomography(pts_src, pts_dst)

        # Warp source image to destination
        im_dst = cv2.warpPerspective(im_src, h, size[0:2])

        # Show output
        cv2.imshow("Image", im_dst)
        cv2.waitKey(0)
        print(pts_src)
        # Save the output image
        cv2.imwrite('output_images/output-perspective.jpg', im_dst)
