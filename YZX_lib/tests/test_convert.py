import pytest
import numpy as np
from YZX_lib.convert import PoseConverter


class TestConversion:
    def test_euler_matrix_roundtrip(self):
        """测试欧拉角到矩阵的往返转换"""
        converter = PoseConverter(order='zyx', degree=True)
        original_euler = [30.0, 45.0, 60.0]
        original_trans = [1.0, 2.0, 3.0]

        # 欧拉角转矩阵
        mat = converter.euler_to_matrix(original_euler, original_trans)
        assert mat.shape == (4, 4), "位姿矩阵应为 4x4 形状"

        # 矩阵转欧拉角
        recovered_euler, recovered_trans = converter.matrix_to_euler(mat)
        assert len(recovered_euler) == 3, "欧拉角应为 3 个元素"
        assert len(recovered_trans) == 3, "平移向量应为 3 个元素"

        # 验证平移向量
        np.testing.assert_allclose(original_trans, recovered_trans, atol=1e-6)

        # 验证旋转（使用正弦值比较，处理角度多解问题）
        assert np.allclose(
            np.sin(np.radians(original_euler)),
            np.sin(np.radians(recovered_euler)),
            atol=1e-6
        )

    def test_euler_matrix_roundtrip_radians(self):
        """测试弧度单位的欧拉角到矩阵的往返转换"""
        converter = PoseConverter(order='zyx', degree=False)
        original_euler = [np.pi/6, np.pi/4, np.pi/3]  # 30°, 45°, 60°
        original_trans = [0.5, 1.0, 1.5]

        # 欧拉角转矩阵
        mat = converter.euler_to_matrix(original_euler, original_trans)
        assert mat.shape == (4, 4)

        # 矩阵转欧拉角
        recovered_euler, recovered_trans = converter.matrix_to_euler(mat)

        # 验证平移向量
        np.testing.assert_allclose(original_trans, recovered_trans, atol=1e-6)

        # 验证旋转
        assert np.allclose(
            np.sin(original_euler),
            np.sin(recovered_euler),
            atol=1e-6
        )

    def test_matrix_to_euler_no_translation(self):
        """测试无平移的矩阵转欧拉角"""
        converter = PoseConverter(order='zyx', degree=True)
        original_euler = [0.0, 0.0, 0.0]
        original_trans = [0.0, 0.0, 0.0]

        mat = converter.euler_to_matrix(original_euler, original_trans)
        recovered_euler, recovered_trans = converter.matrix_to_euler(mat)

        np.testing.assert_allclose(original_trans, recovered_trans, atol=1e-6)
        assert np.allclose(
            np.sin(np.radians(original_euler)),
            np.sin(np.radians(recovered_euler)),
            atol=1e-6
        )
