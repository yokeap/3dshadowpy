import numpy as np
import math


def magnitudeCompute3D(origin, destination):
    origin = np.array(origin)
    destination = np.array(destination)
    diffVect = origin - destination
    return math.sqrt((diffVect[0] * diffVect[0]) + (diffVect[1] * diffVect[1]) + (diffVect[2] * diffVect[2]))


def unitVector2D(origin, dest):
    l1 = np.array([origin[0] - dest[0], origin[1] - dest[1]])
    magnitude = math.sqrt((l1[0] * l1[0]) + (l1[1] * l1[1]))
    return np.array([l1[0]/magnitude, l1[1]/magnitude])


def homographyTransform(homographyMatrix, inputMatrix):
    homographyMatrix = np.array(homographyMatrix)
    inputMatrix = np.array(inputMatrix)
    PR = np.matmul(homographyMatrix, inputMatrix)
    newX = PR[0]/PR[2]
    newY = PR[1]/PR[2]
    # worldUnit = np.array([[newX], [newY], [0]])
    worldUnit = np.array([newX, newY, 0], dtype=object)
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
