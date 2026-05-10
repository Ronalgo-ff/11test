import math
import random
import os
import sys
import testt

def median_filter(data, window_size=3):
    if window_size % 2 == 0:
        raise ValueError("窗口大小必须为奇数")
    half = window_size // 2
    n = len(data)
    result = [0.0] * n
    for i in range(n):
        window = [data[max(0, min(n - 1, j))] for j in range(i - half, i + half + 1)]
        window.sort()
        result[i] = window[half]
    return result


def run_test():
    n = 200
    rng = random.Random()

    # 随机生成信号：正弦 + 随机游走 + 随机噪声
    t = [i / n for i in range(n)]
    clean = [0.5 * math.sin(10 * math.pi * ti) + rng.gauss(0, 0.05) for ti in t]

    # 添加椒盐噪声
    noisy = [rng.choice([2.0, -2.0]) if rng.random() < 0.12 else c for c in clean]

    filtered = median_filter(noisy, 5)

    # 终端输出
    print("序号  | 原始信号 | 加噪信号 | 滤波结果")
    print("-" * 44)
    for i in range(20):
        print(f"{i:4d} | {clean[i]:8.4f} | {noisy[i]:8.4f} | {filtered[i]:9.4f}")

    mse = lambda d: sum((c - v) ** 2 for c, v in zip(clean, d)) / n
    print(f"\n均方误差: 加噪={mse(noisy):.4f}  滤波后={mse(filtered):.4f}")

    # 绘图
    try:
        import matplotlib.pyplot as plt
        import matplotlib.font_manager as fm
        for f in ['Microsoft YaHei', 'SimHei']:
            try:
                fm.findfont(f, fallback_to_default=False)
                plt.rcParams['font.sans-serif'] = [f, 'DejaVu Sans']
                break
            except Exception:
                continue
        plt.rcParams['axes.unicode_minus'] = False

        fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

        axes[0].plot(clean, 'k-', linewidth=1, label='原始信号')
        axes[0].plot(noisy, 'r.', markersize=3, label='加噪信号')
        axes[0].legend()
        axes[0].set_title("滤波前 — 原始信号 + 椒盐噪声")

        axes[1].plot(clean, 'k-', linewidth=1, label='原始信号')
        axes[1].plot(filtered, 'b-', label='滤波结果 k=5')
        axes[1].legend()
        axes[1].set_title("滤波后 — 中值滤波对比")

        plt.tight_layout()
        out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "median_filter_result.png")
        plt.savefig(out_path, dpi=120)
        print(f"\n图表已保存到 {out_path}")

        # 直接打开图片
        if sys.platform == 'win32':
            os.startfile(out_path)
        elif sys.platform == 'darwin':
            import subprocess
            subprocess.run(['open', out_path])
        else:
            import subprocess
            subprocess.run(['xdg-open', out_path])

    except ImportError:
        print("(未安装 matplotlib，跳过绘图)")


if __name__ == "__main__":
    run_test()
