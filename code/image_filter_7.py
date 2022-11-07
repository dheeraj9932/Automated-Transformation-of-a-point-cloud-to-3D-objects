import numpy as np


def image_filter(img, k):
    black_pixels = []
    for i,value in enumerate(img):
      for j, value in enumerate(img[i]):
        if value[0] == 0 and value[1] == 0 and value[2] == 0:
          black_pixels.append([i,j])
    # print(black_pixels)

    def filter(img, r,c, k):
      k = k
      red = 0; green = 0; blue = 0
      for i in range(2*k + 1):
        row = i-k
        for j in range(2*k + 1):
          col = j-k
          if r + row >= img.shape[0] or r + row < 0 or c + col >= img.shape[1] or c + col < 0:
            continue
          else:
              # if red < img[r + row][c + col][0]: red = img[r + row][c + col][0]
              # if green < img[r + row][c + col][1]: red = img[r + row][c + col][1]
              # if blue < img[r + row][c + col][2]: red = img[r + row][c + col][2]
            red = red + img[r + row][c + col][0]
            green = green + img[r + row][c + col][1]
            blue = blue + img[r + row][c + col][2]
      normaliser = (2*k + 1)**2
      # print("normaliser is "+str(normaliser))
      # print("red : "+str(red/normaliser)+" green : "+str(green/normaliser) + " blue : "+str(blue/normaliser))
      img[r][c][0] = int(red/normaliser)
      img[r][c][1] = int(green/normaliser)
      img[r][c][2] = int(blue/normaliser)
      # img[r][c][0] = int(red)
      # img[r][c][1] = int(green)
      # img[r][c][2] = int(blue)
      return None

    for i, value in enumerate(black_pixels):
      r = value[0]; c = value[1]
      # print(r, c)
      # print("run")
      filter(img, r, c, k)
    return img