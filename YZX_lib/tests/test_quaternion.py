import pytest
import numpy as np
from YZX_lib.transform import euler_to_quat, quat_to_matrix, is_rotation_matrix


class TestQuaternion:
    def test_euler_to_quat_shape(self):
        """测试欧拉角转四元数的输出形状"""
        euler = np.array([0.1, 0.2, 0.3])
        quat = euler_to_quat(euler)
        assert quat.shape == (4,)

    def test_euler_to_quat_normalized(self):
        """测试生成的四元数是否归一化"""
        euler = np.array([np.pi/4, np.pi/3, np.pi/6])
        quat = euler_to_quat(euler)
        norm = np.linalg.norm(quat)
        np.testing.assert_allclose(norm, 1.0, atol=1e-6)

    def test_quat_to_matrix_shape(self):
        """测试四元数转旋转矩阵的输出形状"""
        quat = np.array([0, 0, 0, 1])  # 单位四元数
        R = quat_to_matrix(quat)
        assert R.shape == (3, 3)

    def test_quat_to_matrix_identity(self):
        """测试单位四元数转旋转矩阵"""
        quat = np.array([0, 0, 0, 1])
        R = quat_to_matrix(quat)
        np.testing.assert_allclose(R, np.eye(3), atol=1e-6)

    def test_quat_to_matrix_is_rotation(self):
        """测试四元数转旋转矩阵是否为有效旋转矩阵"""
        euler = np.array([0.1, 0.2, 0.3])
        quat = euler_to_quat(euler)
        R = quat_to_matrix(quat)
        assert is_rotation_matrix(R)

    def test_euler_quat_matrix_roundtrip(self):
        """测试欧拉角 -> 四元数 -> 矩阵的往返转换"""
        original_euler = np.array([0.1, 0.2, 0.3])
        quat = euler_to_quat(original_euler)
        R = quat_to_matrix(quat)
        assert is_rotation_matrix(R)
