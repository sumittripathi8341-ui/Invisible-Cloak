import cv2
import numpy as np

print("""
Harry :  Hey !! Would you like to try my invisibility cloak ??
         It's awesome !!

         Prepare to get invisible .....................
""")

# Open webcam
cap = cv2.VideoCapture(0)

# Load background video
bg_video = cv2.VideoCapture('video1.mp4')

if not cap.isOpened() or not bg_video.isOpened():
    print("❌ Error reading from webcam or background video.")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    ret_bg, back = bg_video.read()

    # Loop the video if it ends
    if not ret_bg:
        bg_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret_bg, back = bg_video.read()

    if not ret or not ret_bg:
        break

    # Resize background to match webcam frame size
    back = cv2.resize(back, (frame.shape[1], frame.shape[0]))

    # Convert current frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define red color range (lower and upper)
    lower_red1 = np.array([0, 80, 20])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    lower_red2 = np.array([160, 80, 20])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # Combine masks
    mask = mask1 + mask2

    # Apply the mask to background
    part1 = cv2.bitwise_and(back, back, mask=mask)

    # Invert mask and apply to original frame
    mask_inv = cv2.bitwise_not(mask)
    part2 = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Combine both results
    final_output = cv2.addWeighted(part1 + part2, 1, part1 + part2, 0, 0)

    cv2.imshow("🧙‍♂️ Invisibility Cloak", final_output)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
bg_video.release()
cv2.destroyAllWindows()
