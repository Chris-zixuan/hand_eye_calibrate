import numpy as np
from ..constants import EPSILON


def create_rotation_matrix_x(theta):
    """
    创建绕X轴旋转的旋转矩阵
    """
    return np.array([
        [1, 0, 0],
        [0, np.cos(theta), -np.sin(theta)],
        [0, np.sin(theta), np.cos(theta)],
    ])


def create_rotation_matrix_y(theta):
    """
    创建绕Y轴旋转的旋转矩阵
    """
    return np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)],
    ])


def create_rotation_matrix_z(theta):
    """
    创建绕Z轴旋转的旋转矩阵
    """
    return np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1],
    ])


def create_pose_matrix(rot_matrix, translation=np.zeros(3)):
    """
    创建4x4的齐次变换矩阵
    """
    pose = np.eye(4)
    pose[:3, :3] = rot_matrix
    pose[:3, 3] = translation
    return pose


def is_rotation_matrix(R):
    """验证是否为有效的旋转矩阵 (正交且行列式为 1)"""
    shouldBeIdentity = np.dot(R.T, R)
    I = np.identity(3, dtype=R.dtype)
    err = np.linalg.norm(I - shouldBeIdentity)
    return err < EPSILON
