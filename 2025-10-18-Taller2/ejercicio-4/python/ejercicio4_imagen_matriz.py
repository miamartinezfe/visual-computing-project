import os
import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DATOS = os.path.join(ROOT, "datos")
RESULTADOS = os.path.join(ROOT, "resultados")
os.makedirs(RESULTADOS, exist_ok=True)
INPUT_IMG = os.path.join(DATOS, "input.jpg")

def ensure_region(y1, y2, x1, x2, h, w):
    if y1 is None or y2 is None or x1 is None or x2 is None:
        cy, cx = h // 2, w // 2
        half_h = max(1, h // 4)
        half_w = max(1, w // 4)
        return max(0, cy - half_h), min(h, cy + half_h), max(0, cx - half_w), min(w, cx + half_w)
    y1 = int(max(0, min(y1, h - 2)))
    y2 = int(max(y1 + 1, min(y2, h)))
    x1 = int(max(0, min(x1, w - 2)))
    x2 = int(max(x1 + 1, min(x2, w)))
    return y1, y2, x1, x2

def save_rgb(path, arr_rgb):
    arr_bgr = cv2.cvtColor(arr_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, arr_bgr)

def plot_and_save_histograms(orig_rgb, mod_rgb, out_prefix):
    fig, axes = plt.subplots(2, 3, figsize=(12, 6))
    for i, ch in enumerate(cv2.split(orig_rgb)):
        axes[0, i].hist(ch.ravel(), bins=256, range=(0, 255))
        axes[0, i].set_title(f'Orig channel {i}')
    for i, ch in enumerate(cv2.split(mod_rgb)):
        axes[1, i].hist(ch.ravel(), bins=256, range=(0, 255))
        axes[1, i].set_title(f'Mod channel {i}')
    plt.tight_layout()
    out_path = f"{out_prefix}_histograms.png"
    fig.savefig(out_path)
    plt.close(fig)
    return out_path

def save_grayscale_histogram(orig_rgb, mod_rgb, out_path):
    gray_orig = cv2.cvtColor(orig_rgb, cv2.COLOR_RGB2GRAY)
    gray_mod = cv2.cvtColor(mod_rgb, cv2.COLOR_RGB2GRAY)
    fig, ax = plt.subplots(1, 2, figsize=(8, 4))
    ax[0].hist(gray_orig.ravel(), bins=256, range=(0, 255))
    ax[0].set_title("Gray orig")
    ax[1].hist(gray_mod.ravel(), bins=256, range=(0, 255))
    ax[1].set_title("Gray mod")
    plt.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    return out_path

def main():
    if not os.path.exists(INPUT_IMG):
        print("Error: input image not found at:", INPUT_IMG)
        sys.exit(1)
    img_bgr = cv2.imread(INPUT_IMG)
    if img_bgr is None:
        print("Error: failed to read image (corrupt or unsupported):", INPUT_IMG)
        sys.exit(1)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    h, w = img_rgb.shape[:2]
    y1, y2, x1, x2 = ensure_region(50, 200, 100, 350, h, w)
    save_rgb(os.path.join(RESULTADOS, "original_rgb.png"), img_rgb)
    r, g, b = cv2.split(img_rgb)
    ch_r = np.stack([r, np.zeros_like(r), np.zeros_like(r)], axis=2)
    ch_g = np.stack([np.zeros_like(g), g, np.zeros_like(g)], axis=2)
    ch_b = np.stack([np.zeros_like(b), np.zeros_like(b), b], axis=2)
    save_rgb(os.path.join(RESULTADOS, "channel_r.png"), ch_r)
    save_rgb(os.path.join(RESULTADOS, "channel_g.png"), ch_g)
    save_rgb(os.path.join(RESULTADOS, "channel_b.png"), ch_b)
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    h_ch, s_ch, v_ch = cv2.split(img_hsv)
    ch_h = np.stack([h_ch, h_ch, h_ch], axis=2).astype(np.uint8)
    ch_s = np.stack([s_ch, s_ch, s_ch], axis=2).astype(np.uint8)
    ch_v = np.stack([v_ch, v_ch, v_ch], axis=2).astype(np.uint8)
    save_rgb(os.path.join(RESULTADOS, "channel_h.png"), cv2.cvtColor(ch_h, cv2.COLOR_RGB2RGB))
    save_rgb(os.path.join(RESULTADOS, "channel_s.png"), cv2.cvtColor(ch_s, cv2.COLOR_RGB2RGB))
    save_rgb(os.path.join(RESULTADOS, "channel_v.png"), cv2.cvtColor(ch_v, cv2.COLOR_RGB2RGB))
    region = img_rgb[y1:y2, x1:x2].copy()
    alpha = 1.2
    beta = 20
    region_adj = cv2.convertScaleAbs(region, alpha=alpha, beta=beta)
    img_mod = img_rgb.copy()
    img_mod[y1:y2, x1:x2] = region_adj
    save_rgb(os.path.join(RESULTADOS, "modified_region.png"), img_mod)
    hist_path = plot_and_save_histograms(img_rgb, img_mod, os.path.join(RESULTADOS, "region_comparison"))
    gray_hist_path = save_grayscale_histogram(img_rgb, img_mod, os.path.join(RESULTADOS, "gray_comparison_hist.png"))
    print("Saved files:")
    print(os.path.join(RESULTADOS, "original_rgb.png"))
    print(os.path.join(RESULTADOS, "channel_r.png"))
    print(os.path.join(RESULTADOS, "channel_g.png"))
    print(os.path.join(RESULTADOS, "channel_b.png"))
    print(os.path.join(RESULTADOS, "channel_h.png"))
    print(os.path.join(RESULTADOS, "channel_s.png"))
    print(os.path.join(RESULTADOS, "channel_v.png"))
    print(os.path.join(RESULTADOS, "modified_region.png"))
    print(hist_path)
    print(gray_hist_path)

if __name__ == "__main__":
    main()
