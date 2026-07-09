import cv2
import numpy as np
from pathlib import Path

image_name = "test.JPG"
radius = 35
spots = []

img = cv2.imread(image_name)
if img is None:
    print("Image not found.")
    exit()

mask = np.zeros(img.shape[:2], dtype=np.uint8)

def redraw():
    display = img.copy()
    mask[:] = 0

    for x, y, r in spots:
        cv2.circle(display, (x, y), r, (0, 0, 255), 2)
        cv2.circle(mask, (x, y), r, 255, -1)

    cv2.putText(display, f"Spots: {len(spots)}  Radius: {radius}  Z=Undo  S=Save  Q=Quit",
                (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Dust Remover", display)

def click_spot(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        spots.append((x, y, radius))
        redraw()

cv2.namedWindow("Dust Remover", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Dust Remover", click_spot)
redraw()

print("Left click = add spot")
print("Z = undo last spot")
print("C = clear all")
print("+ = bigger brush")
print("- = smaller brush")
print("S = save cleaned image")
print("Q = quit")

while True:
    key = cv2.waitKey(1) & 0xFF

    if key == ord("z"):
        if spots:
            spots.pop()
            redraw()

    elif key == ord("c"):
        spots.clear()
        redraw()

    elif key in [ord("+"), ord("=")]:
        radius += 5
        redraw()

    elif key in [ord("-"), ord("_")]:
        radius = max(5, radius - 5)
        redraw()

    elif key == ord("s"):
        cleaned = cv2.inpaint(img, mask, 9, cv2.INPAINT_TELEA)
        out_name = Path(image_name).stem + "_manual_cleaned.JPG"
        cv2.imwrite(out_name, cleaned)
        print("Saved:", out_name)

    elif key == ord("q") or key == 27:
        break

cv2.destroyAllWindows()