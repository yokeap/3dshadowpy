import cv2

# define camera and set resolution
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

# define background subtractor
background_subtr_method = cv2.createBackgroundSubtractorMOG2(5000, 16, True)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
    # frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    foreground_mask = background_subtr_method.apply(frame)
    background_img = background_subtr_method.getBackgroundImage()

    cv2.imshow('Input', frame)
    cv2.imshow("Foreground Masks", foreground_mask)
    cv2.imshow("Subtraction Result", background_img)


    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()