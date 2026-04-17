from utiles.opencv_utils import OpenCVUtils
import numpy as np
import glob
import os


def GetImagesPath(folder_path):
    """
    获取指定目录下所有常见图片格式的文件路径

    Args:
        folder_path: 图片所在目录路径

    Returns:
        list: 排序后的图片文件路径列表
    """
    # 支持的图片格式
    image_extensions = ["*.jpg", "*.jpeg", "*.png",
                        "*.bmp", "*.tiff", "*.tif", "*.webp"]

    image_paths = []
    for ext in image_extensions:
        pattern = os.path.join(folder_path, ext)
        image_paths.extend(glob.glob(pattern))

    # 去重并排序
    image_paths = sorted(list(set(image_paths)))

    # 提示信息
    if len(image_paths) == 0:
        print(f"警告: 在目录 '{folder_path}' 中未找到任何图片文件")
        print(
            f"支持的图片格式: {', '.join([ext.replace('*.', '') for ext in image_extensions])}")
    else:
        print(f"成功: 在目录 '{folder_path}' 中找到 {len(image_paths)} 个图片文件")

    return image_paths


def generate_object_points(rows, cols, square_size):
    """
    生成3D点

    Args:
        rows: 标定板的行数
        cols: 标定板的列数
        square_size: 标定板一格的长度  单位为米

    Returns:
        np.ndarray: 3D点的坐标矩阵
    """
    obj_points = np.zeros((rows * cols, 3), dtype=np.float32)
    obj_points[:, :2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2)*square_size
    return obj_points


if __name__ == "__main__":
    # 超参数设置
    np.set_printoptions(precision=4, suppress=True)
    cv_utiles = OpenCVUtils()
    rows = 11  # 标定板的中长度对应的角点的个数
    cols = 8  # 标定板的中宽度对应的角点的个数
    square_size = 0.035  # 标定板一格的长度  单位为米

    # 参数
    iamge_folder_path = "collect_data/"  # 手眼标定采集的标定版图片所在路径
    # 采集标定板图片时对应的机械臂末端的位姿 从 第一行到最后一行 需要和采集的标定板的图片顺序进行对应
    arm_pose_file_path = "collect_data/poses.txt"

    # Step 0：预定义
    image_2D_points = []  # 存储2D点
    obj_3D_points = []  # 存储3D点

    # Step 1: 提取2D点
    image_paths = GetImagesPath(iamge_folder_path)
    for image_path in image_paths:
        ret, corners, gray = cv_utiles.find_chessboard_corners(
            image_path, (rows, cols))

        if ret:  # 确保找到角点再处理
            img_refine_points = cv_utiles.refine_corners(gray, corners)
            image_name = os.path.basename(image_path)
            save_path = f"Result/corners/{image_name}"
            cv_utiles.draw_corners(image_path, (rows, cols),
                                   img_refine_points, ret, is_show=False, save_path=save_path)
            image_2D_points.append(img_refine_points)
        else:
            print(f"警告: 未找到角点 - {image_path}")

    # Step 2: 计算单应性矩阵
    # 生成棋盘格角点的世界坐标
    obj_board_3D_points = generate_object_points(rows, cols, square_size)
    # 计算每张图的旋转和平移
    a = calibrateCamera(obj_board_3D_points, image_2D_points)
