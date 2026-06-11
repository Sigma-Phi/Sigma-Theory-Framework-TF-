這個理論其實就是在研究「利他行為怎麼在群體中進化起來」的數學模型。核心想法是：如果你幫助親戚，雖然自己會付出成本，但因為親戚也帶有你的基因，這種利他行為有機會被選擇留下。數學上，我們用一個 0~1 的數字 x 代表群體中利他策略的比例，然後根據「Hamilton 條件」（幫助收益 × 親緣係數 > 成本）來決定策略強弱。系統會隨時間自動更新，利他基因多的時候更容易被保留下來，不利的就慢慢消失。

從 AI 的角度看，它就像一個帶有「回饋控制」和「策略學習」的強化學習系統：環境（B、C、親緣係數）是輸入，控制器決定行為強度 u，然後狀態 x 根據效果更新。整個過程是一個正回饋迴路，AI 模型可以模擬這種演化，學習在不同環境下利他行為的最佳策略。也可以用蒙地卡羅或深度 RL 做大量模擬，觀察利他策略在群體中的收斂與穩定性。

總之，這理論不只是生物學，也可以用 AI 視角理解成「策略控制 + 環境回饋 + 演化優化」的動態系統。


# 理論名稱：廣義適應度親緣選擇動力學理論  
*(Inclusive Fitness Kin Selection Dynamics)*

---

## 1. 系統定義 (Concrete Formalization)

本系統強制映射至 **機率簡形空間（Probability Simplex）Δ¹**，用以描述群體中「利他表現型基因型」的出現頻率。

### 狀態空間 (State Space X)
\[
X = [0,1], \quad x \in X
\]
其中 \(x\) 表示群體中利他等位基因（或利他策略）的出現頻率。

---

### 觀測空間 (Observation Space O)
\[
O = r \in [0,1]
\]
代表系統對環境中親緣個體遺傳特徵識別後的平均親緣係數。

---

### 信號空間 (Signal Space S)
\[
S = (B, C)
\]
其中：
- \(B\)：利他行為帶來的群體收益  
- \(C\)：個體執行行為的能量成本  

---

### 控制空間 (Control Space U)
\[
U = u \in [0,1]
\]
代表利他行為釋放機率或行為強度輸出。

---

## 2. 明確動態系統 (Well-defined Dynamics)

系統狀態轉移為：

\[
x_{t+1} = F(x_t, u_t, B_t, C_t)
\]

控制策略為：

\[
u_t = G(o_t, B_t, C_t)
\]

信號映射：

\[
(B_t, C_t) = \phi(\text{environment}_t)
\]

其中：
- \(\theta > 0\)：基因庫更新選擇係數（學習率/演化速率）  
- \(\beta > 0\)：決策平滑因子  

---

### 函數性質

- **狀態轉移函數 F**
  - 非線性 (Nonlinear)
  - Lipschitz 連續
  - 擴展 replicator dynamics

- **控制函數 G**
  - 有界非線性
  - Sigmoid/Hamiltonian 判別逼近
  - Lipschitz 連續

- **信號映射 φ**
  - 凸函數或固定邊際映射

---

## 3. 假設集合 (Explicit Assumptions)

- **A1**：\(X=[0,1]\) 為緊緻且有界空間  
- **A2**：\(B_t \in [0,B_{max}], C_t \in [0,C_{max}]\)  
- **A3**：F 在 X 上 Lipschitz 連續，常數 \(L_F\)  
- **A4**：G 有界且可測，\(u_t \in [0,1]\)  
- **A5**：  
\[
0 < \theta < \frac{2}{B_{max} + C_{max}}
\]

---

## 4. 可驗證命題 (Testable Propositions)

### 命題 1：收斂性

若滿足：

\[
\bar{o} \cdot B > C
\]

則：

\[
x_t \rightarrow 1
\]

反之：

\[
\bar{o} \cdot B < C \Rightarrow x_t \rightarrow 0
\]

---

## 5. 穩定性分析 (Lyapunov / Contractive Check)

構造 Lyapunov 函數：

\[
V(x) = 1 - x
\]

性質：

- \(V(x) \ge 0\) 對 \(x \in (0,1]\)
- \(V(1)=0\)

差分變化：

\[
\Delta V = V(x_{t+1}) - V(x_t)
\]

代入動態系統 \(F\)：

當 Hamilton 條件成立：

\[
o_t B_t > C_t,\quad u_t > 0
\]

則：

\[
\Delta V < 0
\]

因此系統滿足收斂性與穩定性條件。

---

## 6. 可驗證性要求 (Experimental Validity)

### 模擬方法
- Euler Forward Method 離散化
- 初始值 \(x_0 \in (0,1)\)
- Monte Carlo 擾動 \(r, B, C\)

### 收斂判定
\[
|x_{t+N} - x_t| < \epsilon, \quad \epsilon = 10^{-6}
\]

### 穩定性測試
- 在 \(x^*=0,1\) 加入脈衝 \(\delta x\)
- 檢查回復能力（local asymptotic stability）

### 誤差估計
\[
MSE = \mathbb{E}[(x^{det}_t - x^{noise}_t)^2]
\]

---

## 7. 系統分類

- Control System（回饋控制）
- Stochastic Dynamical System（隨機環境擾動）
- Optimization System（廣義適應度最大化）

---

## 8. 最終理論輸出 (Theorem Form)

**Theorem 1**

若滿足 A1–A5，且存在：

\[
\inf_t (o_t B_t - C_t) > \delta > 0
\]

則：

\[
x_t \rightarrow 1
\]

且：

\[
x^* = 1
\]

在內部空間 \( \Delta^1 \setminus \{0\} \) 上全域漸近穩定。

---

## 9. 一句話理論本質

本系統是一個**以親緣係數作為動態增益、以 Hamilton 不等式作為閾值開關的正回饋基因頻率控制優化系統**。
