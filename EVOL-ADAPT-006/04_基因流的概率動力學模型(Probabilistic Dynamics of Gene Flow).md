這篇論文其實是在說「不同族群的基因是怎麼互相影響、慢慢變化的」。你可以把每個種群想像成一鍋果汁，每種水果的比例就是不同的基因。每一代，果汁都會有三件事發生：一部分保持原本味道（原有基因）、一部分混入外面的果汁（遷移的基因）、還有一點小變化（就像不小心撒進去的新材料）。

作者設計了一個「攪拌公式」，每次更新時，果汁的新味道 = 原本味道 × (1–攪拌力) + 外來果汁 × 攪拌力 + 一點隨機波動。系統裡還有一個小機制：如果內部和外部味道差很大，就加大攪拌；差不多了就減少，保證不會亂掉。

結果很直觀：如果外面果汁一直保持一樣，鍋裡的果汁最後也會慢慢變得跟外面差不多，整體味道趨於穩定。換句話說，基因流就像一種把種群慢慢拉向外界平均狀態的力量，而且這個過程可以用數學精確模擬和驗證。



# 《基因流的概率動力學模型》  
**English Title:** *Probabilistic Dynamics of Gene Flow*

---

## 1. 系統定義（Concrete Formalization）

**選擇數學結構：** probability simplex Δⁿ  
> 基因流本質是「等位基因頻率在種群間演化」。

### State Space
\[
X_t \in \Delta^n
\]  
表示時間 \(t\) 的種群基因頻率向量：
\[
X_t = (x_t^1, x_t^2, ..., x_t^n), \quad \sum_i x_t^i = 1
\]

### Observation Space
\[
O_t \in \mathbb{R}^n
\]  
表示外部種群輸入的觀測基因頻率（migrant allele distribution）。

### Signal Space
\[
S_t \in \mathbb{R}^n
\]  
表示「環境適應性加權後的基因信號」。

### Control Space
\[
U_t \in [0,1]^n
\]  
表示基因流強度（migration / mixing rate vector）。

---

## 2. 明確動態系統（Well-defined Dynamics）

### 系統演化方程
\[
X_{t+1} = F(X_t, O_t, U_t, \theta)
\]  

定義：
\[
X_{t+1} = (1 - U_t) \odot X_t + U_t \odot O_t + \epsilon_t
\]  
- **F**：stochastic convex combination system  
- \(\epsilon_t\)：噪聲（mutation drift）

### Control Function
\[
U_t = G(S_t, \theta)
\]  

定義：
\[
U_t = \sigma(W S_t)
\]  
- **G**：neural / Lipschitz bounded mapping  
- \(\sigma\)：sigmoid 保證 boundedness

### Signal Function
\[
S_t = \phi(X_t, O_t)
\]  

定義：
\[
S_t = O_t - X_t
\]  
- **φ**：linear difference operator

---

## 3. 假設集合（Explicit Assumptions）

- **A1.** state space bounded  
  \(X_t \in \Delta^n\)  
- **A2.** noise bounded sub-Gaussian  
  \(\epsilon_t \sim \text{sub-Gaussian}(0, \sigma^2)\)  
- **A3.** F Lipschitz continuous  
  \(\|F(x)-F(y)\| \le L \|x-y\|\)  
- **A4.** G bounded measurable  
  \(U_t \in [0,1]^n\)  
- **A5.** step stability  
  \(\mathbb{E}[U_t] \le 1\)  

---

## 4. 可驗證命題（Testable Propositions）

- **命題 1（收斂）**  
  若外部分布穩定 \(O_t \to O^*\)，則：
  \[
  X_t \rightarrow O^*
  \]

- **命題 2（平衡態）**  
  存在固定點 \(X^*\) 使：
  \[
  X^* = (1 - U^*)X^* + U^* O^*
  \]  
  解得：
  \[
  X^* = O^*
  \]

- **命題 3（期望收斂）**  
  \[
  \mathbb{E}[X_t] \to O^*
  \]

---

## 5. 穩定性分析（Lyapunov / Contractive Check）

定義 Lyapunov 函數：
\[
V(X_t) = \|X_t - O^*\|^2
\]

差分：
\[
V(X_{t+1}) - V(X_t) = \|(1-U_t)(X_t - O^*) + \epsilon_t\|^2 - \|X_t - O^*\|^2
\]

收縮條件：
\[
0 < U_t \le 1 \implies \mathbb{E}[V(X_{t+1})] \le (1 - \alpha) V(X_t) + \sigma^2
\]  
其中 \(\alpha = \min(U_t)\)

**結論：** 系統為 **stochastic contractive system**

---

## 6. 可驗證性要求（Experimental Validity）

### 模擬方法
1. 初始化 \(X_0\)（初始種群）  
2. 給定外部分布 \(O_t\)  
3. 迭代：
   - 更新 \(S_t = O_t - X_t\)  
   - 計算 \(U_t = \sigma(W S_t)\)  
   - 更新 \(X_{t+1}\)  

### 收斂測量
\[
\|X_t - O^*\| \to 0
\]  
或使用 KL divergence：
\[
D_{KL}(X_t \| O^*)
\]

### 穩定性驗證
- variance 是否收斂  
- drift 是否下降  
- spectral radius of update Jacobian < 1

### 誤差估計
\[
\mathbb{E}[\|X_t - X^*\|] \le O(\sigma)
\]

---

## 7. 系統分類

- ✔ Stochastic Dynamical System  
- ✔ Control System  
- ✔ Estimation System  
- ✔ Hybrid Feedback System  

---

## 8. 最終定理（Theorem Form）

**Theorem (Gene Flow Convergence Theorem)**  

If assumptions A1–A5 hold, and external allele distribution \(O_t \to O^*\), then:

\[
X_t \rightarrow O^*
\]  
in probability, and the system is stochastically stable under bounded migration noise.

---

## 9. 一句話理論本質

> 基因流系統是一個在隨機控制下，將種群分布逐步拉向外部遺傳分布的收縮型概率動力系統。
