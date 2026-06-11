⸻
性選擇動力學可以理解為自然界的「演化智能系統」。每個個體都是一個「智能代理」，它有自己的狀態——基因與表型特徵，能觀察環境和其他個體的信號，並基於這些訊號做出配偶選擇策略。整個種群的目標是最大化繁殖適應度，就像 AI 系統裡的 reward function。

系統包含正反饋和負反饋。正反饋相當於獎勵放大：受歡迎的特徵被更多個體選擇，下一代表型分布會向這些特徵傾斜；負反饋就像約束或懲罰，防止過度特徵降低生存率。突變和隨機因素則提供探索噪聲，使系統避免陷入局部最優。

通過世代模擬，我們可以追蹤種群表型分布收斂到穩定平衡，檢查平均適應度是否提升，驗證系統是否達到穩定策略。簡單說，性選擇是一個帶正負反饋、隨機探索的自然演化算法，不斷「學習」如何在繁殖成功與生存壓力間取得最優平衡，最終形成穩定的性狀



# Sexual Selection Dynamics / 性選擇動力學

---

## 1. 系統定義（Concrete Formalization）

**選擇結構類型**：measurable space  
（系統涉及個體變異、遺傳分布與隨機選擇過程）

---

### State space \(X\)：種群表型分布與基因頻率

\[
X_t \in \Delta^n, \quad n = \text{表型基因組數量}
\]

（使用概率單形 \(\Delta^n\) 表示基因 / 表型比例）

---

### Observation space \(O\)：個體可觀察表型 + 環境參數

\[
O_t = \{ \text{phenotypes}, \text{environmental factors} \} \in \mathbb{R}^m
\]

---

### Signal space \(S\)：個體求偶信號

\[
S_t \in \mathbb{R}^k, \quad k = \text{信號特徵數量}
\]

---

### Control space \(U\)：配偶選擇策略 / 生殖決策

\[
U_t \in \Delta^p, \quad p = \text{候選配偶數量}
\]

---

## 2. 動態系統（Well-defined Dynamics）

\[
\begin{aligned}
X_{t+1} &= F(X_t, O_t, U_t, \theta) && \text{(stochastic, nonlinear)} \\
S_t &= \phi(X_t, O_t) && \text{(nonlinear, measurable)} \\
U_t &= G(S_t, \theta) && \text{(convex, bounded)}
\end{aligned}
\]

---

### 2.1 具體建模

#### (1) 種群演化動態

\[
X_{t+1} = X_t \odot \frac{W(X_t, U_t)}{\langle W(X_t, U_t), \mathbf{1} \rangle} + \epsilon_t
\]

- \(\odot\)：元素乘法  
- \(W(X_t, U_t)\)：適應度加權矩陣（含正 / 負反饋）  
- \(\epsilon_t \sim \text{small stochastic noise}\)

---

#### (2) 信號生成

\[
S_t = \phi(X_t, O_t)
\]

\[
\phi(X_t, O_t) = \text{observable phenotype features weighted by energy allocation}
\]

---

#### (3) 配偶選擇策略

\[
U_t = \text{softmax}(\alpha \cdot S_t \cdot \text{fitness weight})
\]

- \(\alpha\)：選擇強度參數  
- 結構保持 convex / bounded  

---

## 3. 假設集合（Explicit Assumptions）

- **A1**：\(X\) 為概率單形（有界且緊緻）  
- **A2**：\(\epsilon_t\) 服從 sub-Gaussian 分布  
- **A3**：\(F\) 為 Lipschitz 連續（常數 \(L < \infty\)）  
- **A4**：\(G\) 有界且可測  
- **A5**：時間步長 \(\eta_t = 1\)（離散世代）或可逐漸縮小  

---

## 4. 可驗證命題（Testable Propositions）

- **收斂性**  
\[
X_t \rightarrow X^*
\]

- **適應度單調性（期望）**  
\[
\mathbb{E}[\langle W(X_t, U_t), \mathbf{1} \rangle] \ \text{non-decreasing}
\]

- **邊界穩定性**  
\[
X_t \in [0,1], \quad \sum_i X_t^{(i)} = 1
\]

---

## 5. 穩定性分析（Lyapunov / Contractive Check）

### Lyapunov 函數

\[
V(X) = D_{\text{KL}}(X \,\|\, X^*)
\]

\[
V(X) = \sum_i X^*_i \log \frac{X^*_i}{X_i}
\]

---

### 收斂條件

\[
V(X_{t+1}) - V(X_t) \le 0
\quad \text{若 } F \text{ 對 } X^* \text{ contractive}
\]

---

### 或適應度條件

\[
\mathbb{E}[W(X_{t+1}, U_{t+1})]
\ge
\mathbb{E}[W(X_t, U_t)]
\]

---

## 6. 可驗證性（Experimental Validity）

- 離散世代模擬（population + selection matrix）
- 收斂檢測：
  - KL divergence
  - Total variation distance \(\|X_{t+1} - X_t\|_1\)
- Lyapunov 單調性檢查
- Monte Carlo 重複模擬估計穩定分布

---

## 7. 系統分類（System Classification）

- Stochastic Dynamical System  
- Evolutionary Optimization System  
- Hybrid Feedback System  

---

## 8. 最終理論輸出（Theorem Form）

**Theorem (Sexual Selection Stability Theorem)**

If assumptions A1–A5 hold, then:

\[
X_t \rightarrow X^*
\quad \text{and} \quad
\mathbb{E}[\langle W(X_t, U_t), \mathbf{1} \rangle] \ \text{converges}
\]

with bounded phenotypic proportions and stable feedback dynamics.

---

## 9. 一句話理論本質

性選擇動力學是一個作用於概率單形上的隨機非線性反饋系統，其透過信號驅動的選擇機制，使種群收斂至適應度平衡態。
