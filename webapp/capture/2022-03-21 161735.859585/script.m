rgbImage = imread('imgRoi.jpg');
imshow(rgbImage)
hsvImage = rgb2hsv(rgbImage);
sImage = hsvImage(:, :, 2);
figure;
imshow(sImage);
sValue = sImage(:);
sds = datastats(sValue)
sBinImage = imbinarize(sImage, sds.std);
figure;
imshow(sBinImage);