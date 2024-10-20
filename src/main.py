import numpy as np
import matplotlib.pyplot as plt

def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def lerp(t, a, b):
    return a + t * (b - a)

def grad(hash, x, y):
    h = hash & 3
    u = x if h < 2 else y
    v = y if h < 2 else x
    return (u if h & 1 == 0 else -u) + (v if h & 2 == 0 else -v)

def perlin(x, y, permutation):
    xi = int(x) & 255
    yi = int(y) & 255
    xf = x - int(x)
    yf = y - int(y)

    u = fade(xf)
    v = fade(yf)

    aa = permutation[permutation[xi] + yi]
    ab = permutation[permutation[xi] + yi + 1]
    ba = permutation[permutation[xi + 1] + yi]
    bb = permutation[permutation[xi + 1] + yi + 1]

    x1 = lerp(u, grad(aa, xf, yf), grad(ba, xf - 1, yf))
    x2 = lerp(u, grad(ab, xf, yf - 1), grad(bb, xf - 1, yf - 1))
    return lerp(v, x1, x2)

def generate_permutation():
    p = np.arange(256, dtype=int)
    np.random.shuffle(p)
    return np.tile(p, 2)

def generate_perlin_noise(width, height, scale=50):
    permutation = generate_permutation()
    noise = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            x = i / scale
            y = j / scale
            noise[i][j] = perlin(x, y, permutation)
    return noise


def main(width: int=200, height: int=200):
    noise = generate_perlin_noise(width, height)

    plt.imshow(noise, cmap='gray')
    plt.colorbar()
    plt.show()

if __name__ == "__main__":
    main()