import cv2

# 画像読込
image = cv2.imread('22968524.jpg')
print(image.shape)

# 矩形描画
start_point = (370, 600)
end_point = (1680, 1750)
color = (0, 0, 255)
thickness = 4
cv2.rectangle(image, start_point, end_point, color, thickness)

# リサイズ
width = int(image.shape[1] * 0.2)
hight = int(image.shape[0] * 0.2)
resized_image = cv2.resize(image, (width, hight))
print(resized_image.shape)

# 結果表示
cv2.imshow('Rectangle', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
