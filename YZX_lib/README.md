# 项目目录结构

建议采用标准的 Python 包结构，便于维护和测试。

```
my_pose_lib/
├── __init__.py          # 包入口，暴露主要 API
├── constants.py         # 定义常量（轴定义、旋转顺序、单位）
├── exceptions.py        # 自定义异常（如 GimbalLockError）
├── core/
│   ├── __init__.py
│   ├── matrix.py        # 基础矩阵运算 (基于 numpy)
│   ├── quaternion.py    # 四元数运算 (建议作为内部中间表示)
│   └── euler.py         # 欧拉角逻辑
├── convert.py           # 高层转换接口 (Euler <-> Matrix <-> Quaternion)
├── utils.py             # 工具函数 (角度弧度转换、数值容差判断)
└── tests/
    ├── __init__.py
    ├── test_euler.py
    └── test_matrix.py
```

---

# 核心设计原则

在写代码之前，必须明确以下几点，这决定了库的可用性：

| 原则 | 说明 |
|------|------|
| **旋转顺序 (Rotation Order)** | 是 XYZ 还是 ZYX？是静坐标系 (Extrinsic) 还是动坐标系 (Intrinsic)？建议默认使用机器人学常见的 ZYX (Yaw-Pitch-Roll) 内旋 |
| **单位 (Units)** | 内部计算统一使用 弧度 (radians)，输入输出可提供角度选项 |
| **内部表示 (Internal Representation)** | 强烈建议内部使用 四元数 (Quaternion) 作为中间媒介。因为 欧拉角 <-> 四元数 <-> 矩阵 的转换比 欧拉角 <-> 矩阵 直接转换更稳定，且容易处理万向节锁 |
| **数值容差 (Epsilon)** | 浮点数比较不能直接用 ==，需要设置 eps=1e-6 |

---

# 开发建议

| 类别 | 说明 |
|------|------|
| **依赖** | 只依赖 numpy。不要依赖 scipy，因为你的目标是自己实现算法。但你可以用 scipy.spatial.transform.Rotation 作为测试时的"标准答案"来验证你的库是否正确 |
| **文档** | 使用 Google Style 或 NumPy Style 编写 Docstring。明确说明每个函数的输入输出形状 (Shape) |
| **性能** | 如果涉及大量转换，考虑使用 numpy 的广播机制支持批量处理（即输入 (N, 3) 的欧拉角数组，输出 (N, 4, 4) 的矩阵数组） |

---

这个框架为你提供了一个清晰的起点。你可以先从 ZYX 顺序的右手坐标系开始实现，跑通单元测试后，再扩展支持其他旋转顺序。
