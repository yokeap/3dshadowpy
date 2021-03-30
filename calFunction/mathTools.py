import numpy as np
import math


def unitVector2D(origin, dest):
    l1 = np.array([[origin[0] - dest[0]], [origin[1] - dest[1]]])
    magnitude = math.sqrt((l1[0] * l1[0]) + (l1[1] * l1[1]))
    return np.array([l1[0]/magnitude, l1[1]/magnitude])


def homographyTransform(homographyMatrix, inputMatrix):
    PR = np.multiply(homographyMatrix, inputMatrix)
    newX = PR[0, 0]/PR[2, 0]
    newY = PR[1, 0]/PR[2, 0]
    worldUnit = [newX, newY, 0]
    return worldUnit

# compute the position of 2-rays intersection


def rayintersect(origin1, origin2, unitVect1, unitVect2):
    O = origin1 - origin2
    u_dot_u = np.dot(unitVect1, unitVect1)
    v_dot_v = np.dot(unitVect2, unitVect2)
    u_dot_v = np.dot(unitVect1, unitVect2)
    w_dot_u = np.dot(W, unitVect1)
    w_dot_v = np.dot(W, unitVect2)

    denom = (u_dot_u * v_dot_v) - (u_dot_v * u_dot_v)

    s = ((u_dot_v/denom) * w_dot_v) - ((v_dot_v/denom) * w_dot_u)
    t = -((u_dot_v/denom) * w_dot_u) + ((u_dot_u/denom) * w_dot_v)

    position = (origin1 + s*unitVect1) + (origin2 + t*unitVect2)
    position = position/2
    return position
