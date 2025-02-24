import cv2
import numpy as np

# Kameradan görüntü al
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Görüntü alınamadı!")
        break

    # Görüntüyü HSV renk uzayına çevir
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Kırmızı renk için alt ve üst limitler
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Kırmızı renk maskesi oluştur
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 | mask2

    # Maskeyi iyileştirmek için açma ve kapama işlemleri uygula
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Konturları bul
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Kontur alanını kontrol et (çok küçük veya büyük nesneleri yok say)
        area = cv2.contourArea(contour)
        if 500 < area < 5000:  # Bu aralığı ihtiyacına göre değiştir
            # Dikdörtgen bounding box çiz
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # "Balon" etiketini ekle
            cv2.putText(frame, "Balon", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Sonucu göster
    cv2.imshow("Balon Tespiti", frame)

    # Çıkış için 'q' tuşuna bas
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
