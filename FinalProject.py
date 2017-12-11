import numpy as np
import cv2
import glob

cap = cv2.VideoCapture(0)
database = []

# Define the codec and create VideoWriter object
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
for file in glob.glob('C:\Users\megan\Desktop/plates/*.jpg'):
    im = cv2.imread(file)
    database.append(im)



while(cap.isOpened()):
    ret, frame = cap.read()


    for plate in database:


        # read in the puzzle and the query
        #plate = cv2.imread('C:\Users\megan\Desktop\plates\plate1.jpg')

        # get plate's dimensions
        (plateH, plateW) = plate.shape[:2]
        #print plateH

        # find the plate in the puzzle using Template Matching
        result = cv2.matchTemplate(frame, plate, cv2.TM_CCOEFF_NORMED)
        (_, max_val, min_loc, max_loc) = cv2.minMaxLoc(result)
        top_left = max_loc

        if max_val>=0.35:
            print max_val

            # extract plate from the image (for Squared Difference use minLoc instead of maxLoc)
            topLeft = max_loc
            botRight = (topLeft[0] + plateW, topLeft[1] + plateH)
            roi = frame[topLeft[1]:botRight[1], topLeft[0]:botRight[0]]


                # Put a red border around plate
            RED = [0, 0, 255]
            constant = cv2.copyMakeBorder(roi, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=RED)
            plate_box = cv2.resize(constant, (plateW, plateH))

                # put plate back in the image
            frame[topLeft[1]:botRight[1], topLeft[0]:botRight[0]] = plate_box
            break

    if ret==True:

        # write the frame
        #out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()