import cv2
import os
import numpy as np

image_folder = 'trai_cay/tao'
output_folder = 'trai_cay_chuan_hoa/tao'

files = os.listdir(image_folder)

for file_name in files:
    name, ext = os.path.splitext(file_name)
    input_path = os.path.join(image_folder, file_name)
    output_path = os.path.join(output_folder, name + '.bmp')

    if not os.path.isfile(input_path):
        print(f"File {file_name} does not exist. Skipping...")
        continue

    imgin = cv2.imread(input_path, cv2.IMREAD_COLOR)

    if imgin is None:
        print(f"Failed to read image: {file_name}. Skipping...")
        continue

    M, N, P = imgin.shape
    if M < N:
        d = N - M
        pad = np.ones((d, N, 3), np.uint8) * 255
        imgout = np.vstack((imgin, pad))
        imgout = cv2.resize(imgout, (320, 320))
    elif M > N:
        d = M - N
        pad = np.ones((M, N, 3), np.uint8) * 255
        imgout = np.hstack((imgin, pad))
    else:
        imgout = imgin

    imgout = cv2.resize(imgout, (320, 320))
    cv2.imwrite(output_path, imgout)

print('Done')