import numpy as np
from .constants import EPSILON
from .core.matrix import create_pose_matrix, is_rotation_matrix
from .core.quaternion import euler_to_quat, quat_to_matrix
from .utils import deg2rad, rad2deg


class PoseConverter:
    def __init__(self, order='zyx', degree=False):
        """
        :param order: 旋转顺序，如 'zyx', 'xyz'
        :param degree: 输入输出是否使用角度 (默认内部使用弧度)
        """
        self.order = order
        self.degree = degree

    def euler_to_matrix(self, euler_angles, translation=None):
        """
        欧拉角转 4x4 位姿矩阵
        :param euler_angles: [roll, pitch, yaw] 或 [x, y, z]
        :param translation: [x, y, z] 平移向量
        :return: 4x4 numpy array
        """
        angles = np.array(euler_angles)
        if self.degree:
            angles = deg2rad(angles)

        # 1. Euler -> Quaternion (更稳定)
        quat = euler_to_quat(angles, order=self.order)
        # 2. Quaternion -> Rotation Matrix
        rot_mat = quat_to_matrix(quat)

        if not is_rotation_matrix(rot_mat):
            raise ValueError("Invalid rotation matrix generated")

        # 3. Add Translation
        if translation is None:
            translation = [0, 0, 0]
        pose_mat = create_pose_matrix(rot_mat, translation)

        return pose_mat

    def matrix_to_euler(self, pose_matrix):
        """
        4x4 位姿矩阵转欧拉角
        :param pose_matrix: 4x4 numpy array
        :return: [roll, pitch, yaw], translation
        """
        R = pose_matrix[:3, :3]
        t = pose_matrix[:3, 3]

        # 这里需要实现具体的 Matrix -> Euler 逻辑
        # 注意处理万向节锁 (Gimbal Lock)，即 pitch = +/- 90 度时
        # 简化示例：调用核心逻辑
        euler = self._rot_mat_to_euler(R)

        if self.degree:
            euler = rad2deg(euler)

        return euler, t

    def _rot_mat_to_euler(self, R):
        """
        内部实现：旋转矩阵转欧拉角 (ZYX 顺序，即 Yaw-Pitch-Roll)
        需要处理万向节锁 (Gimbal Lock)
        """
        if self.order.lower() != 'zyx':
            raise NotImplementedError("仅支持 ZYX 顺序")

        # pitch (Y 轴旋转)
        sy = np.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)

        if sy > EPSILON:
            # 正常情况：pitch 不接近 +/- 90 度
            pitch = np.arcsin(-R[2, 0])
            yaw = np.arctan2(R[1, 0], R[0, 0])
            roll = np.arctan2(R[2, 1], R[2, 2])
        else:
            # 万向节锁：pitch 接近 +/- 90 度
            pitch = np.arcsin(-R[2, 0])
            roll = 0.0
            yaw = np.arctan2(-R[0, 1], R[1, 1])

        return np.array([roll, pitch, yaw])
