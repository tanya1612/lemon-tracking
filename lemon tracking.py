import cv2
import numpy as np

#Definig lower and upper bounds in HSV for yellow
lowerBound = np.array([21, 100, 100])
upperBound = np.array([28, 255, 255])

#Capture video from source
cap = cv2.VideoCapture('http://192.168.43.1:8080/video')

#Applying operations on initial frame

#Defining structuring element for Opening and Closing operations
kernelOpen = np.ones((10, 10))
kernelClose = np.ones((20, 20))

#Reading frame from video
ret, frame = cap.read()

#Resizing the frame to 340x220
frame = cv2.resize(frame, (340, 220))

#Conversting color of frame from BGR to HSV
hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#Detecting yellow color in the frma
lemon = cv2.inRange(hsvFrame, lowerBound, upperBound)

#Noise reduction using opening and closing
lemonOpen = cv2.morphologyEx(lemon, cv2.MORPH_OPEN, kernelOpen)
lemonClose = cv2.morphologyEx(lemon, cv2.MORPH_CLOSE, kernelClose)
lemonFinal = lemonClose

#Finding boundaries of lemon in first frame
inicontour = cv2.findContours(lemonFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#Intended work: keep reading frames till lemon appears on it
while len(inicontour) == 0:
    inicontour = cv2.findContours(lemonFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame = cap.read()

#Get boundaries of rectangle around the lemon
ix, iy, iw, ih = cv2.boundingRect(inicontour[0])
#Calculating centroid
icentre = (ix + iw/2, iy + ih/2)

#Checking initial position of lemon
left = False
right = False
if icentre[0] <= .03*340:
    left = True
elif icentre[0] >= .97*340:
    right = True

while ret:
    #Reading and resizing frame
    ret, frame = cap.read()
    frame = cv2.resize(frame, (340, 220))

    #Converting to HSV
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lemon = cv2.inRange(hsvFrame, lowerBound, upperBound)
    lemonOpen = cv2.morphologyEx(lemon, cv2.MORPH_OPEN, kernelOpen)
    lemonClose = cv2.morphologyEx(lemon, cv2.MORPH_CLOSE, kernelClose)
    lemonFinal = lemonClose

    #Finding the contours
    contours = cv2.findContours(lemonFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Detecting condition for failure
    if len(contours) == 0:
            print('Fall')
            cap.release()
            cv2.destroyAllWindows()
            exit()

    #Checking for all contours
    for contour in contours:

        #Detecting boundaries of lemon
        x, y, w, h = cv2.boundingRect(contour)
        #Calculating centroid
        centre = (x + w/2, y + h/2)

        #Drawing a rectangle around the lemon
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)


        #Checking conditions for success
        if left:
            if centre[0] >= .97*340:
                print('Success')
                cap.release()
                cv2.destroyAllWindows()
                exit()
        elif right:
            if centre[0] <= .03*340:
                print('Success')
                cap.release()
                cv2.destroyAllWindows()
                exit()
        else:
            if centre[0] >= .97*340 or centre[0] <= .03*340:
                print('Success')
                cap.release()
                cv2.destroyAllWindows()
                exit()

    #Displaying the frames
    cv2.imshow("Final morph", lemonFinal)
    cv2.imshow("actualFrame", frame)

    #Wait for a 'q' to be pressed
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

#Releasing the input video source
cap.release()

#Destroying all the opened windows
cv2.destroyAllWindows()
