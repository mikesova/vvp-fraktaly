import numpy as np
from numba import njit

@njit
def julia_set(x_min: float,
              x_max: float,
              y_min: float,
              y_max: float,
              width: int,
              height: int,
              c: complex,
              max_iter: int) -> np.ndarray:
    
    """
    Vypočítá Juliovu množinu pro daný výřez komplexní roviny a pevné číslo c.

    Parametry:
        x_min (float): Minimální hodnota reálné části (osa x).
        x_max (float): Maximální hodnota reálné části (osa x).
        y_min (float): Minimální hodnota imaginární části (osa y).
        y_max (float): Maximální hodnota imaginární části (osa y).
        width (int): Šířka výsledného obrázku (v pixelech).
        height (int): Výška výsledného obrázku (v pixelech).
        c (complex): Komplexní konstanta určující tvar Juliovy množiny.
        max_iter (int): Maximální počet iterací pro posouzení divergence.

    Návratová hodnota:
        np.ndarray: 2D pole (height x width) obsahující počet iterací do divergence
                    pro každý bod. Pokud bod nediverguje, je v něm hodnota `max_iter`.
    """

    image = np.zeros((height, width), dtype=np.int32)

    for y in range(height):
        imag = y_min + (y / height) * (y_max - y_min)
        for x in range(width):
            real = x_min + (x / width) * (x_max - x_min)
            z = complex(real, imag)
            for i in range(max_iter):
                z = z*z + c
                if (z.real*z.real + z.imag*z.imag) >= 4.0:
                    image[y, x] = i
                    break
            else:
                image[y, x] = max_iter

    return image