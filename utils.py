import cv2
import numpy as np

# import matplotlib.pyplot as plt
# from pathlib import Path


# def imshow(img: np.ndarray) -> None:
#     plt.imshow(img[:, :, [2, 1, 0]])
#     plt.xticks([])
#     plt.yticks([])
#     plt.title(img.shape)
#     # plt.axis('off')
#     plt.show()


def crop_to_square(img: np.ndarray) -> np.ndarray:
    """
    将图片裁剪成最大的内切正方形，并缩放为68x68像素
    参数:
        img: 输入图片
    返回:
        68x68像素的正方形图片
    """
    height, width = img.shape[:2]
    size = min(height, width)

    # 计算裁剪的起始位置，确保正方形在中心
    start_x = (width - size) // 2
    start_y = (height - size) // 2

    # 裁剪图片
    cropped = img[start_y : start_y + size, start_x : start_x + size]

    # 将裁剪后的图片缩放为68x68
    resized = cv2.resize(cropped, (68, 68), interpolation=cv2.INTER_AREA)
    return resized


def getImg(i, j, area_type='normal'):
    start_h = 156 + i * imgHeight
    start_w = 175 + j * imgWidth
    if area_type == 'normal':
        return main[
            start_h : start_h + imgHeight,
            start_w : start_w + imgWidth,
        ]
    elif area_type == 'larger':
        return main[
            start_h - 10 : start_h + imgHeight + 10,
            start_w - 10 : start_w + imgWidth + 10,
        ]
    elif area_type == 'x-larger':
        return main[
            start_h - 100 : start_h + imgHeight + 100,
            start_w - 100 : start_w + imgWidth + 100,
        ]


def find_avatar_template_matching(main_img, avatar_img):
    # 使用OpenCV的模板匹配
    result = cv2.matchTemplate(main_img, avatar_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 获取最佳匹配位置
    top_left = max_loc
    h, w = avatar_img.shape[:2]
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # 在原图上画出匹配位置
    result_img = main_img.copy()
    cv2.rectangle(result_img, top_left, bottom_right, (0, 255, 0), 2)

    return result_img, max_val


def find_avatar(avatar_stem: str):
    # 使用示例
    avatar = cv2.imread(f'input/{avatar_stem}.jpg')
    template = crop_to_square(avatar)[10:-10, 10:-10]
    confidences = np.zeros((50 * 134))
    for i in range(50):
        for j in range(134):
            matched_img, confidence = find_avatar_template_matching(
                getImg(i, j, area_type='larger'), template
            )
            confidences[i * 134 + j] = confidence

    rank = np.argsort(-confidences)
    # plt.plot(confidences[rank], 'o')

    # fig = plt.figure(figsize=(30, 10))
    # for i in range(3):
    #     ax = fig.add_subplot(1, 3, i + 1)
    #     ax.set_title(f'No.{i + 1} confidence: {confidences[rank[i]]}')
    #     row, col = int(rank[i] // 134), int(rank[i] % 134)
    #     matched_img, _ = find_avatar_template_matching(
    #         getImg(row, col, area_type='larger'), template
    #     )
    #     ax.imshow(matched_img[:, :, [2, 1, 0]])
    #     ax.set_xticks([])
    #     ax.set_yticks([])
    # plt.show()

    # choose_i = int(input('choose a number:')) - 1
    choose_i = 0
    row, col = int(rank[choose_i] // 134), int(rank[choose_i] % 134)

    # 计算目标点的坐标
    target_y = 156 + row * imgHeight + imgHeight // 2
    target_x = 175 + col * imgWidth + imgWidth // 2

    # 画箭头
    if target_x > 1000:
        if target_y > 1000:
            arrow_start = (target_x - 1000, target_y - 1000)  # 箭头起点
            arrow_end = (target_x - 100, target_y - 100)  # 箭头终点
        else:
            arrow_start = (target_x - 1000, target_y + 1000)  # 箭头起点
            arrow_end = (target_x - 100, target_y + 100)  # 箭头终点
    else:
        if target_y > 1000:
            arrow_start = (target_x + 1000, target_y - 1000)  # 箭头起点
            arrow_end = (target_x + 100, target_y - 100)  # 箭头终点
        else:
            arrow_start = (target_x + 1000, target_y + 1000)  # 箭头起点
            arrow_end = (target_x + 100, target_y + 100)  # 箭头终点

    arrow_color = (0, 0, 255)  # 红色
    arrow_thickness = 100

    # 画箭头
    img_res = cv2.arrowedLine(
        main.copy(),
        arrow_start,
        arrow_end,
        arrow_color,
        arrow_thickness,
        tipLength=0.3,
    )
    # imshow(img_res)
    cv2.imwrite(
        f'./output/{avatar_stem}.jpg',
        cv2.resize(
            img_res,
            (img_res.shape[1] // 10, img_res.shape[0] // 10),
        ),
    )


main = cv2.imread('./main.jpg')
imgHeight, imgWidth = 68, 68


# imshow(getImg(0, 130, area_type='larger'))
# imshow(getImg(35, 133, area_type='larger'))  # 最右边
# imshow(getImg(49, 0, area_type='larger'))  # 最下边

# imshow(getImg(44, 73, area_type='larger'))
# imshow(crop_to_square(avatar))
