def capture_area():
    import cv2
    import numpy as np
    from PIL import ImageGrab

    # Define a function to capture a selected area of the screen
    def grab_screen(bbox=None):
        # Capture the screen
        img = ImageGrab.grab(bbox=bbox)
        img_np = np.array(img)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        return img_np

    # Get the bounding box coordinates from the user
    print("Please select the area of the screen to capture.")
    bbox = cv2.selectROI("Screen Capture", np.zeros((1, 1, 3), dtype=np.uint8), fromCenter=False)

    # Capture the selected area
    screen_image = grab_screen(bbox)

    # Save or return the captured image
    return screen_image