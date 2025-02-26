# Import necessary libraries  # Gerekli kütüphaneleri içe aktar
import cv2
import numpy as np
import matplotlib.pyplot as plt

def Canny(img):
    """
    Edge detection function using Canny algorithm.
    Kenar tespiti için Canny algoritmasını kullanan fonksiyon.

    :param img: Input image (Giriş görüntüsü)
    :return: Image with detected edges (Tespit edilen kenarlarla birlikte görüntü)
    """
    gray = cv2.cvtColor(imgg, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale (Gri tonlamaya çevir)
    blur = cv2.GaussianBlur(gray, (5,5), 0)  # Apply Gaussian blur to reduce noise (Gürültüyü azaltmak için Gauss bulanıklığı uygula)
    canny = cv2.Canny(blur, 50, 150)  # Detect edges using Canny algorithm (Canny algoritması ile kenarları tespit et)
    return canny

def region_of_interest(img):
    """
    Define a region of interest to focus on lane detection.
    Şerit tespiti için ilgi alanını belirleyen fonksiyon.

    :param img: Input image (Giriş görüntüsü)
    :return: Masked image focusing on the region of interest (İlgi alanına odaklanmış maskeleme uygulanmış görüntü)
    """
    height = img.shape[0]  # Get the height of the image (Görüntünün yüksekliğini al)
    polygons = np.array([[(200, height), (1100, height), (550, 250)]])  # Define a triangular region (Üçgen bir bölge belirle)
    mask = np.zeros_like(img)  # Create a black mask (Siyah bir maske oluştur)
    cv2.fillPoly(mask, polygons, 255)  # Fill the polygon with white (Üçgen bölgeyi beyaz ile doldur)
    masked_image = cv2.bitwise_and(img, mask)  # Apply the mask to the image (Maskeyi görüntüye uygula)
    return masked_image

# Read the test image  # Test görüntüsünü oku
img = cv2.imread('test_image.jpg')
lane = np.copy(img)  # Make a copy of the original image (Orijinal görüntünün bir kopyasını oluştur)
imgg = np.copy(img)  # Another copy for processing (İşlem için başka bir kopya oluştur)

# Apply region of interest function  # İlgi alanı fonksiyonunu uygula
img = region_of_interest(img)

# Apply Canny edge detection  # Canny kenar tespiti uygula
canny = Canny(img)

# Apply region of interest to Canny output  # Canny çıktısına ilgi alanı uygula
cropped = region_of_interest(canny)

# Display the result  # Sonucu göster
cv2.imshow("result", cropped)
cv2.waitKey(0)
