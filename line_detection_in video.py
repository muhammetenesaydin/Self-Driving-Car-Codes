import cv2
import numpy as np


def make_coordinates(image, line):
    """
    Convert slope and intercept values to pixel coordinates.
    Eğim ve kesişim noktalarını piksel koordinatlarına çevirir.
    """
    slope, intercept = line
    y1 = image.shape[0]  # Image height (Görüntü yüksekliği)
    y2 = int(y1 * (3 / 5))  # Draw the line up to 3/5 of the height (Görüntünün 3/5'ine kadar çiz)
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return [[x1, y1, x2, y2]]


def average_slope_intercept(image, lines):
    """
    Compute the average slope and intercept for left and right lane lines.
    Sol ve sağ şerit çizgileri için ortalama eğim ve kesişim noktalarını hesaplar.
    """
    left_fit = []
    right_fit = []
    if lines is None:
        return None

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)  # Find slope & intercept (Eğim ve kesişim noktalarını bul)
        slope, intercept = parameters
        if slope < 0:  # Negative slope → Left lane (Negatif eğim → Sol şerit)
            left_fit.append((slope, intercept))
        else:  # Positive slope → Right lane (Pozitif eğim → Sağ şerit)
            right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)

    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    
    return np.array([left_line, right_line])


def canny(image):
    """
    Apply Canny edge detection after converting to grayscale and blurring.
    Gri tonlamaya çevirme ve bulanıklaştırma sonrası Canny kenar tespiti uygular.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    return edges


def region_of_interest(image):
    """
    Apply a mask to focus on the region of interest (ROI).
    Görüntünün belirli bir bölgesini maske ile izole eder.
    """
    height = image.shape[0]
    polygons = np.array([[(200, height), (1100, height), (550, 250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def display_lines(image, lines):
    """
    Draw detected lane lines on the image.
    Tespit edilen şerit çizgilerini görüntü üzerine çizer.
    """
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)  # Blue color (Mavi renk)
    return line_image


# Open video file (Test videosu açma)
cap = cv2.VideoCapture("test2.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Apply processing steps (İşleme adımları uygulanıyor)
    canny_image = canny(frame)
    cropped_canny = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_canny, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    average_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, average_lines)
    
    # Combine original image with detected lane lines (Orijinal görüntüyü tespit edilen çizgilerle birleştir)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 0)
    
    # Display result (Sonucu göster)
    cv2.imshow("Lane Detection", combo_image)

    # Press 'q' to exit (Çıkmak için 'q' tuşuna bas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources (Kaynakları serbest bırak)
cap.release()
cv2.destroyAllWindows()
