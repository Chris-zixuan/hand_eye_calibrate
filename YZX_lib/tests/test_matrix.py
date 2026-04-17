import pytest
import numpy as np
from YZX_lib.transform import (
    create_rotation_matrix_x,
    create_rotation_matrix_y,
    create_rotation_matrix_z,
    create_pose_matrix,
    is_rotation_matrix
)


class TestMatrix:
    def test_create_rotation_matrix_x(self):
        """测试绕X轴旋转矩阵"""
        theta = np.pi / 4
        R = create_rotation_matrix_x(theta)
        assert R.shape == (3, 3)
        assert is_rotation_matrix(R)

    def test_create_rotation_matrix_y(self):
        """测试绕Y轴旋转矩阵"""
        theta = np.pi / 4
        R = create_rotation_matrix_y(theta)
        assert R.shape == (3, 3)
        assert is_rotation_matrix(R)

    def test_create_rotation_matrix_z(self):
        """测试绕Z轴旋转矩阵"""
        theta = np.pi / 4
        R = create_rotation_matrix_z(theta)
        assert R.shape == (3, 3)
        assert is_rotation_matrix(R)

    def test_create_pose_matrix(self):
        """测试创建位姿矩阵"""
        R = np.eye(3)
        t = np.array([1, 2, 3])
        pose = create_pose_matrix(R, t)
        assert pose.shape == (4, 4)
        np.testing.assert_allclose(pose[:3, :3], R, atol=1e-6)
        np.testing.assert_allclose(pose[:3, 3], t, atol=1e-6)
        np.testing.assert_allclose(pose[3, :], [0, 0, 0, 1], atol=1e-6)

    def test_is_rotation_matrix_valid(self):
        """测试有效的旋转矩阵验证"""
        R = np.eye(3)
        assert is_rotation_matrix(R)

    def test_is_rotation_matrix_invalid(self):
        """测试无效的旋转矩阵验证"""
        R = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        assert not is_rotation_matrix(R)
