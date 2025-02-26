# Import necessary libraries  #  gerekli lkütüphaneleri yüklüyoruz 
import numpy as np
import matplotlib.pyplot as plt

def draw(x1, x2):
    # Doğruyu çizmek için plot fonksiyonu
    # Function to draw the line
    ln = plt.plot(x1, x2)

def sigmoid(score):
    # Sigmoid aktivasyon fonksiyonu
    # Sigmoid activation function
    return 1 / (1 + np.exp(-score))

def calculate_error(line_parameters, points, y):
    # Hata fonksiyonu (cross entropy)
    # Error function (cross entropy)
    n = points.shape[0]
    p = sigmoid(points @ line_parameters)  # @ operatörü ile matris çarpımı
    # Matrix multiplication using @ operator
    cross_entropy = -(1 / n) * (np.log(p).T @ y + np.log(1 - p).T @ (1 - y))
    return cross_entropy

def gradient_descent(line_parameters, points, y, alpha):
    # Gradyan inişi fonksiyonu
    # Gradient descent function
    n = points.shape[0]
    for i in range(2000):  # 2000 iterasyon yapılır
        # 2000 iterations
        p = sigmoid(points @ line_parameters)  # Sigmoid fonksiyonu uygulanır
        # Apply sigmoid function
        gradient = points.T @ (p - y) * (alpha / n)  # Gradyanın hesaplanması
        # Calculate the gradient
        line_parameters = line_parameters - gradient  # Ağırlıkların güncellenmesi
        # Update weights
        
        # Ağırlıkları ve bias'ı al
        # Extract weights and bias
        w1 = line_parameters.item(0)
        w2 = line_parameters.item(1)
        b = line_parameters.item(2)
        
        # Yeni doğruyu çizmek için x1 ve x2 hesaplanır
        # Calculate x1 and x2 for the new line
        x1 = np.array([points[:, 0].min(), points[:, 0].max()])
        x2 = -b / w2 + (x1 * (-w1 / w2))
        
    # Yeni doğruyu çiz
    # Draw the new line
    draw(x1, x2)

# Veri kümesi oluşturuluyor
# Creating the dataset
n_pts = 100
np.random.seed(0)
bias = np.ones(n_pts)

# Üst bölge verisi
# Upper region data
top_region = np.array([np.random.normal(10, 2, n_pts), np.random.normal(12, 2, n_pts), bias]).T

# Alt bölge verisi
# Lower region data
bottom_region = np.array([np.random.normal(5, 2, n_pts), np.random.normal(6, 2, n_pts), bias]).T

# Tüm veriler birleştiriliyor
# Combining all data
all_points = np.vstack((top_region, bottom_region))

# Başlangıç parametreleri (ağırlıklar ve bias)
# Initial parameters (weights and bias)
line_parameters = np.matrix([np.zeros(3)]).T

# Etiketler
# Labels
y = np.array([np.zeros(n_pts), np.ones(n_pts)]).reshape(n_pts * 2, 1)

# Grafik oluşturma
# Creating the plot
_, ax = plt.subplots(figsize=(4, 4))
ax.scatter(top_region[:, 0], top_region[:, 1], color='r')  # Üst bölgeyi kırmızı ile çiz
# Drawing the upper region in red
ax.scatter(bottom_region[:, 0], bottom_region[:, 1], color='b')  # Alt bölgeyi mavi ile çiz
# Drawing the lower region in blue

# Gradyan inişi ile doğruyu çiz
# Draw the line using gradient descent
gradient_descent(line_parameters, all_points, y, 0.06)

# Grafiği göster
# Show the plot
plt.show()
