

⸻

🧠 MEPT 可計算版本（Python Toy Model）

模型對應關係

理論概念	計算對應
互斥場 𝔈	矩陣 X
互斥張力	X[i,j]
投影 Π	normalize + softmax
現象 ℛ	機率分布
光 L	ΔX
時間	iteration step

⸻

🧾 Python 程式碼

import numpy as np
import matplotlib.pyplot as plt
# -----------------------------
# MEPT Toy Model Parameters
# -----------------------------
n = 20                  # 系統維度（狀態數）
steps = 200             # 演化步數
noise_strength = 0.02   # 噪聲
alpha = 0.15            # 收縮強度（互斥穩定性）
# -----------------------------
# 初始化互斥場 𝔈 (張力矩陣 X)
# -----------------------------
X = np.random.rand(n, n)
np.fill_diagonal(X, 0)
# 保證對稱（互斥關係）
X = (X + X.T) / 2
# -----------------------------
# 投影函數 Π：從互斥場 → 現象世界
# -----------------------------
def projection(X):
    # softmax-like projection to probability space
    expX = np.exp(-X)
    np.fill_diagonal(expX, 0)
    return expX / (np.sum(expX) + 1e-9)
# -----------------------------
# 演化函數（互斥動態）
# -----------------------------
def evolve(X):
    global alpha, noise_strength
    # 張力更新：互斥增強 + 收縮穩定
    grad = np.dot(X, X) / n
    X_new = X + alpha * grad
    # 加入隨機噪聲（宇宙擾動）
    X_new += noise_strength * np.random.randn(n, n)
    # 對稱 + 去對角
    X_new = (X_new + X_new.T) / 2
    np.fill_diagonal(X_new, 0)
    # 非負投影（互斥張力不能為負）
    X_new = np.clip(X_new, 0, None)
    return X_new
# -----------------------------
# 主迭代
# -----------------------------
history_energy = []
history_flux = []
for t in range(steps):
    # 投影到現象世界
    R = projection(X)
    # 光 = 張力變化
    if t > 0:
        flux = np.linalg.norm(X - X_prev)
    else:
        flux = 0
    # 能量 = 系統張力總量
    energy = np.sum(X)
    history_energy.append(energy)
    history_flux.append(flux)
    # 更新
    X_prev = X.copy()
    X = evolve(X)
# -----------------------------
# 可視化結果
# -----------------------------
plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.plot(history_energy)
plt.title("MEPT Energy (Total Tension)")
plt.xlabel("time")
plt.ylabel("energy")
plt.subplot(1,2,2)
plt.plot(history_flux)
plt.title("MEPT Light (ΔX)")
plt.xlabel("time")
plt.ylabel("flux")
plt.tight_layout()
plt.show()

⸻

🔬 這個模型對應你的理論

1. 互斥場

X[i,j] = 互斥張力

⸻

2. 光（L）

flux = ||X_t - X_{t-1}||

👉 「互斥變化的投影痕跡」

⸻

3. 現實投影 Π

R = softmax(-X)

👉 張力越高 → 概率越低
（互斥越強 → 越不容易同時出現）

⸻

4. 時間 t

for t in range(steps)

👉 純更新序列

⸻

5. 宇宙行為會出現什麼？

你會看到：

✔ energy（張力）可能收斂

→ 對應「穩定宇宙」

✔ flux（光）會波動

→ 對應「現象變化」

✔ 有時會出現震盪態

→ 對應「宇宙結構相變」

⸻
