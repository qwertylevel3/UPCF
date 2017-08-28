import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    plt.figure(figsize=(8, 5), dpi=80)
    plt.subplot(111)

    y1 = [2, 3, 3, 5, 6]
    y2 = [1, 2, 3, 3, 4]
    x = [1, 2, 3, 4, 5]

    X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
    C = np.cos(X)
    S = np.sin(X)
    plt.plot(x, y1, color="blue", linewidth=2.5, linestyle="-", label="y1")
    plt.plot(x, y2, color="red", linewidth=2.5, linestyle="-", label="y2")

    plt.legend(loc='upper left')

    plt.show()
