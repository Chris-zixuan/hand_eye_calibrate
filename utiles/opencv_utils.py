# coding = utf-8
import cv2
import numpy as np


class OpenCVUtils:
    """
    opencv 工具类，常用方法封装
    """

    def __init__(self):
        """
        初始化
        """
        pass

    @staticmethod
    def find_chessboard_corners(image_path: str, pattern_size: tuple[int, int], flags=None):
        """
        查找棋盘格角点

        Args:
            image_path: 图片路径
            pattern_size: 内角点 (cols, rows)
            flags: findChessboardCorners 的 flags 参数

        Returns:
            ret: 是否找到角点
            corners: 角点坐标数组
            gray: 灰度图
        """
        if flags is None:
            flags = cv2.CALIB_CB_ADAPTIVE_THRESH + \
                cv2.CALIB_CB_NORMALIZE_IMAGE + cv2.CALIB_CB_FILTER_QUADS
        else:
            flags = flags

        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, flags)
        return ret, corners, gray

    @staticmethod
    def refine_corners(gray, corners, win_size=(5, 5), zero_zone=(-1, -1), criteria=None):
        """
        亚像素角点精化

        Args:
            gray: 灰度图
            corners: 初始角点
            win_size: 搜索窗口大小
            zero_zone: 死区大小
            criteria: 迭代终止条件

        Returns:
            精化后的角点坐标
        """
        if criteria is None:
            criteria = (cv2.TERM_CRITERIA_MAX_ITER |
                        cv2.TERM_CRITERIA_EPS, 30, 0.001)
        if corners is None or len(corners) == 0:
            raise ValueError("corners 不能为空")

        return cv2.cornerSubPix(gray, corners.astype(np.float32), win_size, zero_zone, criteria)

    @staticmethod
    def draw_corners(image_path, pattern_size, corners, ret, is_show=False, save_path=None):
        """
        绘制并显示/保存角点检测结果

        Args:
            image_path: 原图路径
            pattern_size: 内角点 (cols, rows)
            corners: 角点坐标
            ret: 是否找到角点
            is_show: 是否显示图片
            save_path: 保存路径，None 则不保存
        """
        img = cv2.imread(image_path)
        cv2.drawChessboardCorners(img, pattern_size, corners, ret)

        if is_show:
            cv2.imshow('Chessboard Corners', img)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()

        if save_path:
            cv2.imwrite(save_path, img)
