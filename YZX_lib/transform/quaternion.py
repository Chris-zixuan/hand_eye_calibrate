import numpy as np


def euler_to_quat(euler, order='XYZ'):
    """
    将欧拉角转换为四元数
    """
    # 假设 order='zyx' (Yaw-Pitch-Roll)
    cr, sr = np.cos(euler[0] * 0.5), np.sin(euler[0] * 0.5)
    cp, sp = np.cos(euler[1] * 0.5), np.sin(euler[1] * 0.5)
    cy, sy = np.cos(euler[2] * 0.5), np.sin(euler[2] * 0.5)

    w = cr * cp * cy + sr * sp * sy
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy

    return np.array([x, y, z, w])


def quat_to_matrix(q):
    """四元数转旋转矩阵"""
    x, y, z, w = q
    R = np.array([
        [1 - 2*y*y - 2*z*z, 2*x*y - 2*z*w,     2*x*z + 2*y*w],
        [2*x*y + 2*z*w,     1 - 2*x*x - 2*z*z, 2*y*z - 2*x*w],
        [2*x*z - 2*y*w,     2*y*z + 2*x*w,     1 - 2*x*x - 2*y*y]
    ])
    return R
