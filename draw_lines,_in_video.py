# Import necessary libraries  # Gerekli kütüphaneleri içe aktar
import cv2
import numpy as np


def make_points(image, line):
    """
    Convert slope and intercept into endpoints for drawing lines.
    Eğim ve kesişim noktalarını çizgi uç noktalarına dönüştür.
    """
    slope, intercept = line
    y1 = int(image.shape[0])  # Bottom of the image (Görüntünün alt kısmı)
    y2 = int(y1 * 3 / 5)  # Slightly lower than the middle (Ortanın biraz altı)
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return [[x1, y1, x2, y2]]


def average_slope_intercept(image, lines):
    """
    Compute average slope and intercept for left and right lane lines.
    Sol ve sağ şerit çizgileri için ortalama eğimi ve kesişimi hesapla.
    """
    left_fit = []
    right_fit = []
    if lines is None:
        return None
    for line in lines:
        for x1, y1, x2, y2 in line:
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:  # y is reversed in image (Görüntüde y ekseni ters olduğu için)
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_points(image, left_fit_average)
    right_line = make_points(image, right_fit_average)
    return [left_line, right_line]


def canny(img):
    """
    Apply Canny edge detection.
    Canny kenar tespiti uygula.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    kernel = 5
    blur = cv2.GaussianBlur(gray, (kernel, kernel), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny


def display_lines(img, lines):
    """
    Draw detected lane lines on the image.
    Algılanan şerit çizgilerini görüntü üzerinde çiz.
    """
    line_image = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image


def region_of_interest(img):
    """
    Define the region of interest for lane detection.
    Şerit tespiti için ilgi alanını belirle.
    """
    height = img.shape[0]
    mask = np.zeros_like(img)
    triangle = np.array([[(200, height), (550, 250), (1100, height)]], np.int32)
    cv2.fillPoly(mask, triangle, 255)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


# Capture video feed  # Video akışını yakala
cap = cv2.VideoCapture("test2.mp4")
while cap.isOpened():
    _, frame = cap.read()
    canny_image = canny(frame)
    cropped_canny = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_canny, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    cv2.imshow("result", combo_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
