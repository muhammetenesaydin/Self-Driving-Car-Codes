import cv2
import numpy as np

# Kamera görüntüsünü yakalamak için VideoCapture nesnesini oluşturuyoruz
cap = cv2.VideoCapture(0)

while True:
    # Kameradan görüntüyü okuyoruz
    ret, img = cap.read()
    if not ret:
        break
    
    # Görüntüyü kopyalıyoruz
    imgg = np.copy(img)
    
    # Grayscale dönüşümü
    gray = cv2.cvtColor(imgg, cv2.COLOR_BGR2GRAY)
    
    # Gaus bulanıklaştırma
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Canny kenar tespiti
    canny = cv2.Canny(blur, 50, 150)
    
    # Hough dönüşümü ile çizgileri bulma
    lines = cv2.HoughLines(canny, 1, np.pi/180, 200)
    
    # Çizgileri görüntü üzerine çizme
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
            
            # Çizgileri beyaz renkte çiziyoruz
            cv2.line(imgg, (x1, y1), (x2, y2), (255, 255, 255), 2)
    
    # Sonuç görüntüsünü gösterme
    cv2.imshow('Canny Edges', canny)
    cv2.imshow('Detected Lines', imgg)
    
    # 'q' tuşuna basarak döngüyü kırabilirsiniz
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırakma
cap.release()
cv2.destroyAllWindows()
