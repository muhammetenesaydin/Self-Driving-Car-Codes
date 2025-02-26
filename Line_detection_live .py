import cv2
import numpy as np

# Create a VideoCapture object to capture video from the camera
# Kamera görüntüsünü yakalamak için VideoCapture nesnesini oluşturuyoruz
cap = cv2.VideoCapture(0)

while True:
    # Read the frame from the camera
    # Kameradan görüntüyü okuyoruz
    ret, img = cap.read()
    if not ret:
        break  # Exit loop if the frame is not read (Çerçeve okunamazsa döngüden çık)

    # Copy the original image
    # Orijinal görüntüyü kopyalıyoruz
    imgg = np.copy(img)

    # Convert the image to grayscale
    # Görüntüyü gri tonlamaya çeviriyoruz
    gray = cv2.cvtColor(imgg, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    # Gürültüyü azaltmak için Gauss bulanıklığı uyguluyoruz
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform Canny edge detection
    # Canny algoritması ile kenar tespiti yapıyoruz
    canny = cv2.Canny(blur, 50, 150)

    # Detect lines using Hough Transform
    # Hough dönüşümü ile çizgileri tespit ediyoruz
    lines = cv2.HoughLines(canny, 1, np.pi / 180, 200)

    # Draw the detected lines on the image
    # Tespit edilen çizgileri görüntü üzerine çiziyoruz
    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            # Draw lines in white color
            # Çizgileri beyaz renkte çiziyoruz
            cv2.line(imgg, (x1, y1), (x2, y2), (255, 255, 255), 2)

    # Show the Canny edge detection result
    # Canny kenar tespitini gösteriyoruz
    cv2.imshow('Canny Edges', canny)

    # Show the final image with detected lines
    # Tespit edilen çizgilerle birlikte nihai görüntüyü gösteriyoruz
    cv2.imshow('Detected Lines', imgg)

    # Press 'q' to break the loop
    # 'q' tuşuna basarak döngüyü kırabilirsiniz
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources and close windows
# Kaynakları serbest bırak ve pencereleri kapat
cap.release()
cv2.destroyAllWindows()
