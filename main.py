import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def show_image(image1, image2, image3):
    fig, axs = plt.subplots(1, 3)
    axs[0].imshow(image1.astype('uint8'))
    axs[1].imshow(image2.astype('uint8'))
    axs[2].imshow(image3.astype('uint8'))
    axs[0].title.set_text('Original - Bayer')
    axs[1].title.set_text('Original - X-Trans')
    axs[2].title.set_text('X-Trans - Bayer')
    plt.show()


def interpolation(img, edit_img, edit_img_0_1):   # funkcja ktora zlicza na okolo punkty w sume i liczy srednią
    for l in range(3):
        for x in range(img.shape[0]):
            for y in range(img.shape[1]):
                values, counter = 0, 0
                if edit_img_0_1[x, y, l] == 0:
                    for a in range(x - 1, x + 2):
                        for b in range(y - 1, y + 2):
                            if a > img.shape[0] - 1 or a < 0 or b > img.shape[1] - 1 or b < 0:
                                continue
                            if edit_img_0_1[a, b, l] == 1:
                                values += edit_img[a, b, l]
                                counter += 1
                    edit_img[x, y, l] = values / counter


image = cv.imread('demosaicking.bmp')
image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
print(image.shape)

bayer_img = np.zeros(image.shape)      # tutaj zapisuejmy kolory w odpowiednich pozycjach
bayer_img_0_1 = np.zeros(image.shape)  # zaznaczamy filtr bayera w jakich pozycjach sa kolory

xtrans_img = np.zeros(image.shape)
xtrans_img_0_1 = np.zeros(image.shape)

for x in range(image.shape[0]):      # wysokosc
    for y in range(image.shape[1]):  # szerokosc
        if (y % 3 == 0 and x % 3 == 0) or (y % 3 == 1 and x % 3 == 1) or (y % 3 == 1 and x % 3 == 2) or (y % 3 == 2 and x % 3 == 1) or (y % 3 == 2 and x % 3 == 2):
            xtrans_img[x, y, 1] = image[x, y, 1]
            xtrans_img_0_1[x, y, 1] = 1
        elif (x % 6 == 0 and y % 6 == 1) or (x % 6 == 0 and y % 6 == 5) or (x % 6 == 1 and y % 6 == 3) or (x % 6 == 2 and y % 6 == 0) or (x % 6 == 3 and y % 6 == 2 ) or (x % 6 == 3 and y % 6 == 4) or (x % 6 == 4 and y % 6 == 0) or (x % 6 == 5 and y % 6 == 3):
            xtrans_img[x, y, 2] = image[x, y, 2]
            xtrans_img_0_1[x, y, 2] = 1
        else:
            xtrans_img[x, y, 0] = image[x, y, 0]
            xtrans_img_0_1[x, y, 0] = 1

interpolation(image, xtrans_img, xtrans_img_0_1)

for x in range(image.shape[0]):         # wysokosc
    for y in range(image.shape[1]):     # szerokosc
        if (y % 2 == 0 and x % 2 == 0) or (y % 2 == 1 and x % 2 == 1):
            bayer_img[x, y, 1] = image[x, y, 1]
            bayer_img_0_1[x, y, 1] = 1
        if y % 2 == 1 and x % 2 == 0:
            bayer_img[x, y, 2] = image[x, y, 2]
            bayer_img_0_1[x, y, 2] = 1
        if y % 2 == 0 and x % 2 == 1:
            bayer_img[x, y, 0] = image[x, y, 0]
            bayer_img_0_1[x, y, 0] = 1

interpolation(image, bayer_img, bayer_img_0_1)

show_image(image-bayer_img, image-xtrans_img, xtrans_img-bayer_img)
