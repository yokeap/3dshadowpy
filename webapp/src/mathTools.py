import numpy as np
import math
from scipy import interpolate


def magnitudeCompute3D(origin, destination):
    origin = np.array(origin)
    destination = np.array(destination)
    diffVect = origin - destination
    return math.sqrt((diffVect[0] * diffVect[0]) + (diffVect[1] * diffVect[1]) + (diffVect[2] * diffVect[2]))


def unitVector2D(origin, dest):
    l1 = np.array([origin[0] - dest[0], origin[1] - dest[1]])
    magnitude = math.sqrt((l1[0] * l1[0]) + (l1[1] * l1[1]))
    return np.array([l1[0]/magnitude, l1[1]/magnitude])


def splineEstimate(xy, splineResolution):
    numberOrPoints = xy.shape[0]
    xy = xy.T  # transpose to row
    knots = xy
    originalSpacing = np.arange(1, numberOrPoints + 1)
    finerSpacing = np.arange(1, numberOrPoints, splineResolution)
    splines = interpolate.splrep(originalSpacing, knots[0], k=3)
    splinesX = interpolate.splev(finerSpacing, splines)
    splines = interpolate.splrep(originalSpacing, knots[1], k=3)
    splinesY = interpolate.splev(finerSpacing, splines)
    # must be swap Y before X
    splinesXY = [splinesX.tolist(), splinesY.tolist()]
    return splinesXY


def homographyTransform(homographyMatrix, inputMatrix, scale):
    scale = 1 / scale
    homographyMatrix = np.array(homographyMatrix)
    # inputMatrix = np.array(inputMatrix)
    inputMatrix = np.array(
        [[inputMatrix[0] * scale], [inputMatrix[1] * scale], [1]], dtype=object)
    PR = np.matmul(homographyMatrix, inputMatrix)
    newX = PR[0]/PR[2]
    newY = PR[1]/PR[2]
    worldUnit = [newX.tolist()[0], newY.tolist()[0], 0]
    # print(worldUnit)

    # worldUnit = np.array([[newX], [newY], [0]])
    # worldUnit = np.array([newX, newY, 0], dtype=object)
    return worldUnit


# compute the position of 2-rays intersection
def rayintersect(origin1, origin2, unitVect1, unitVect2):
    origin1 = np.array(origin1)
    origin2 = np.array(origin2)
    unitVect1 = np.array(unitVect1)
    unitVect2 = np.array(unitVect2)
    W = origin1 - origin2
    u_dot_u = np.dot(unitVect1, unitVect1)
    v_dot_v = np.dot(unitVect2, unitVect2)
    u_dot_v = np.dot(unitVect1, unitVect2)
    w_dot_u = np.dot(W, unitVect1)
    w_dot_v = np.dot(W, unitVect2)

    denom = (u_dot_u * v_dot_v) - (u_dot_v * u_dot_v)

    s = ((u_dot_v/denom) * w_dot_v) - ((v_dot_v/denom) * w_dot_u)
    t = -((u_dot_v/denom) * w_dot_u) + ((u_dot_u/denom) * w_dot_v)

    position = (origin1 + (s*unitVect1)) + (origin2 + (t*unitVect2))
    position = position/2
    return np.array(position)


def calHeightFromShadow(posShadowUpperImg, posCentroidImg, posShadowUpperWorld, posCentroidWorld, posVirlightWorld):
    posShadowUpperImg = np.array(posCentroidImg)
    posCentroidImg = np.array(posCentroidImg)
    posShadowUpperWorld = np.array(posShadowUpperWorld)
    posCentroidWorld = np.array(posCentroidWorld)
    posVirlightWorld = np.array(posVirlightWorld)
    diffPosShadowImg = posCentroidImg - posShadowUpperImg
    diffPosShadowWorld = posCentroidWorld - posShadowUpperWorld
    shadowRange = math.sqrt((diffPosShadowWorld[0] * diffPosShadowWorld[0]) + (
        diffPosShadowWorld[1] * diffPosShadowWorld[1]))
    # compute base length from shadow edge and virtual light source (in world coordinate)
    uLength = magnitudeCompute3D(posShadowUpperWorld, posVirlightWorld)
    vLength = magnitudeCompute3D(
        [posVirlightWorld[0], posVirlightWorld[1], 0], posVirlightWorld)
    wLength = magnitudeCompute3D(
        posShadowUpperWorld, [posVirlightWorld[0], posVirlightWorld[1], 0])
    angle = math.acos(((uLength ** 2) + (wLength ** 2) -
                       (vLength ** 2)) / (2 * uLength * wLength))
    skeletonHeight = shadowRange * angle
    return skeletonHeight


# calculate area of polygon based on Shoelace method
def polyArea(x, y):
    return 0.5*np.abs(np.dot(x, np.roll(y, 1))-np.dot(y, np.roll(x, 1)))

def otsu(hist_channel):
    is_normalized = True
    # Set total number of bins in the histogram
    bins_num = 256

    # Get the image histogram
    hist, bin_edges = np.histogram(hist_channel, bins=bins_num)

    # Get normalized histogram if it is required
    if is_normalized:
        hist = np.divide(hist.ravel(), hist.max())

    # Calculate centers of bins
    bin_mids = (bin_edges[:-1] + bin_edges[1:]) / 2.

    # Iterate over all thresholds (indices) and get the probabilities w1(t), w2(t)
    weight1 = np.cumsum(hist)
    weight2 = np.cumsum(hist[::-1])[::-1]

    # Get the class means mu0(t)
    mean1 = np.cumsum(hist * bin_mids) / weight1
    # Get the class means mu1(t)
    mean2 = (np.cumsum((hist * bin_mids)[::-1]) / weight2[::-1])[::-1]

    inter_class_variance = weight1[:-1] * weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2

    # Maximize the inter_class_variance function val
    index_of_max_val = np.argmax(inter_class_variance)

    threshold = bin_mids[:-1][index_of_max_val]
    # print("Otsu's algorithm implementation thresholding result: ", threshold)
    return threshold
