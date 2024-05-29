import numpy as np
import cv2

# Define chessboard size
chessboard_size = (7, 7)  # Number of internal corners per a chessboard row and column

# Generate the chessboard pattern
square_size = 50  # Square size in pixels
pattern_size = (chessboard_size[0] + 1, chessboard_size[1] + 1)

# Create a blank image
img = np.zeros((pattern_size[1] * square_size, pattern_size[0] * square_size), dtype=np.uint8)

# Draw the chessboard
for i in range(pattern_size[1]):
    for j in range(pattern_size[0]):
        if (i + j) % 2 == 0:
            cv2.rectangle(img, (j * square_size, i * square_size), ((j + 1) * square_size, (i + 1) * square_size), 255, -1)

# Save the chessboard pattern
cv2.imwrite('chessboard.png', img)

# Display the chessboard pattern
cv2.imshow('Chessboard', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
