import random
import math
import sys

# 修复 Windows 终端中文乱码
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


def median_filter(data, window_size=3):
    """中值滤波：用窗口内的中值替换每个点，窗口边缘用最近值填充"""
    if window_size % 2 == 0:
        raise ValueError("窗口大小必须为奇数")
    half = window_size // 2
    n = len(data)
    result = [0.0] * n

    for i in range(n):
        window = []
        for j in range(i - half, i + half + 1):
            if j < 0:
                window.append(data[0])
            elif j >= n:
                window.append(data[-1])
            else:
                window.append(data[j])
        window.sort()
        result[i] = window[half]

    return result


def main():
    # 生成干净的正弦波信号
    n = 100
    clean = [math.sin(2 * math.pi * i / n) for i in range(n)]

    # 添加椒盐噪声（随机尖峰）
    noisy = clean[:]
    rng = random.Random(42)
    for i in range(n):
        if rng.random() < 0.15:
            noisy[i] = rng.choice([2.0, -2.0])

    # 中值滤波
    filtered_3 = median_filter(noisy, window_size=3)
    filtered_5 = median_filter(noisy, window_size=5)

    print("序号  | 原始信号 | 加噪信号 | 滤波(k=3) | 滤波(k=5)")
    print("-" * 52)
    for i in range(20):
        print(f"{i:4d} | {clean[i]:8.4f} | {noisy[i]:8.4f} | {filtered_3[i]:9.4f} | {filtered_5[i]:9.4f}")

    # 计算均方误差
    mse_noisy = sum((c - nv) ** 2 for c, nv in zip(clean, noisy)) / n
    mse_3 = sum((c - f) ** 2 for c, f in zip(clean, filtered_3)) / n
    mse_5 = sum((c - f) ** 2 for c, f in zip(clean, filtered_5)) / n

    print(f"\n均方误差(MSE):  加噪={mse_noisy:.4f}  滤波(k=3)={mse_3:.4f}  滤波(k=5)={mse_5:.4f}")

    # 尝试画图
    try:
        import matplotlib.pyplot as plt
        import matplotlib.font_manager as fm

        # 设置中文字体
        for font_name in ['Microsoft YaHei', 'SimHei', 'WenQuanYi Zen Hei', 'Noto Sans CJK SC']:
            try:
                fm.findfont(font_name, fallback_to_default=False)
                plt.rcParams['font.sans-serif'] = [font_name, 'DejaVu Sans']
                break
            except Exception:
                continue
        plt.rcParams['axes.unicode_minus'] = False

        fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
        axes[0].plot(clean, 'k-', label='原始信号')
        axes[0].plot(noisy, 'r.', markersize=4, label='加噪信号')
        axes[0].legend()
        axes[0].set_title("原始正弦波 + 椒盐噪声")

        axes[1].plot(clean, 'k-', label='原始信号')
        axes[1].plot(filtered_3, 'b-', label='中值滤波 k=3')
        axes[1].legend()
        axes[1].set_title("窗口大小=3")

        axes[2].plot(clean, 'k-', label='原始信号')
        axes[2].plot(filtered_5, 'g-', label='中值滤波 k=5')
        axes[2].legend()
        axes[2].set_title("窗口大小=5")

        plt.tight_layout()
        plt.savefig("median_filter_result.png", dpi=120)
        print("\n图表已保存到 median_filter_result.png")
    except ImportError:
        print("\n(未安装 matplotlib，跳过绘图)")


if __name__ == "__main__":
    main()
