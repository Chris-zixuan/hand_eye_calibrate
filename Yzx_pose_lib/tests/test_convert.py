import numpy as np
import pytest
from Yzx_pose_lib.convert import PoseConverter


class TestConversion:
    def test_euler_matrix_roundtrip(self):
        converter = PoseConverter(order='zyx', degree=True)
        original_euler = [30.0, 45.0, 60.0]
        original_trans = [1.0, 2.0, 3.0]

        mat = converter.euler_to_matrix(original_euler, original_trans)

        recovered_euler, recovered_trans = converter.matrix_to_euler(mat)

        np.testing.assert_allclose(original_trans, recovered_trans, atol=1e-6)
        assert np.allclose(
            np.sin(np.radians(original_euler)),
            np.sin(np.radians(recovered_euler)),
            atol=1e-6
        )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
