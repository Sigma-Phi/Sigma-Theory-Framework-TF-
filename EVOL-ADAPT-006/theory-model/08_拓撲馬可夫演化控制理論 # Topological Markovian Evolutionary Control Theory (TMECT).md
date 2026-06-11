从AI的角度看，这个“拓扑马可夫演化控制理论”（TMECT）本质上是在做一件事：在一堆可能的“树状结构答案”里，用概率方法不断试错，最后逼近最合理的那个。

你可以把它想成一个AI在做“进化树猜测”。它的世界由两部分组成：一部分是树的形状（谁和谁更像亲戚），另一部分是每条分支的“长度”（代表进化差异）。AI每一步都会随机改一点结构，比如交换分支、调整长度，然后用一个评分函数（类似“这个解释数据的概率有多高”）来判断好不好。

如果更好，就更可能被接受；如果更差，也可能偶尔接受，这样避免卡在局部最优。这个过程不断重复，就像AI在黑暗中摸索，但每一步都在向“最能解释数据的树”靠近。

同时，它还有一个“控制器”，会根据当前搜索效果动态调整步子大小：走得太慢就加速，乱跳太多就收敛。

所以从AI视角看，它就是一个：带自适应控制器的概率搜索AI，在树结构空间里做强化版MCMC推理。



# 拓撲馬可夫演化控制理論
## Topological Markovian Evolutionary Control Theory (TMECT)

### 1. 系統定義 (Concrete Formalization)
本系統強制映射至 **機率單體（Probability Simplex）$\Delta^n$** 與 **馬可夫過程空間（Markov Process Space）** 的複合數學結構中。

* **狀態空間 $X$**：定義在拓撲樹空間 $\mathcal{T}_M$ 與邊長（演化時間） $\mathbb{R}_+^{2M-3}$ 的笛卡爾積上，其中 $M$ 為物種（葉節點）數量。$X = \mathcal{T}_M \times \mathbb{R}_+^{2M-3}$。每一個狀態 $X_t = (\tau_t, \mathbf{t}_t)$ 代表第 $t$ 次迭代時的樹拓撲結構 $\tau$ 與分支長度向量 $\mathbf{t}$。
* **觀測空間 $O$**：定義為經多重序列比對校準後的離散特徵矩陣 $D \in \mathcal{S}^{M \times L}$，其中 $L$ 為位點長度，$\mathcal{S}$ 為有限特徵狀態集（如 $\{A, C, G, T\}$）。此空間在系統運行期間為給定之靜態觀測。
* **信號空間 $S$**：定義為當前狀態下各特徵位點的邊際概似度（Marginal Likelihood）向量與自助抽樣（Bootstrap）支援度之組合，屬機率單體空間 $S \in \Delta^{L-1} \times [0,1]^M$。
* **控制空間 $U$**：定義為拓撲搜尋引擎的隨機轉移提議分佈（Proposal Distribution）參數及動態權重調控係數，調整馬可夫鏈蒙地卡羅（MCMC）的步長與接受機率調控比，$U \in \mathbb{R}^k$。

---

### 2. 明確動態系統 (Well-defined Dynamics)
系統的動態演化由以下差分與代數方程組完整刻劃：
$$X_{t+1} = F(X_t, O_t, U_t, \theta)$$
$$U_t = G(S_t, \theta)$$
$$S_t = \phi(X_t, O_t)$$

#### 結構類型標明：
* **狀態轉移函數 $F$（Stochastic / Lipschitz）**：基於 Metropolis-Hastings 抽樣機制。給定控制參數 $U_t$，在樹拓撲空間中透過局部重排（如 NNI, SPR）隨機產生新狀態，其在連續分支長度上的轉移滿足對偏導數的 Lipschitz 連續性。
* **控制策略函數 $G$（Convex / Bounded）**：動態權重調控器。根據當前信號 $S_t$（可信度與收斂速率）調整提議分佈的步長。此函數在有界凸集內運作，確保搜索步長不致發散。
* **信號映射函數 $\phi$（Nonlinear / Stochastic）**：目標函數評估模組（包括過濾、比對分數、概似度計算）。核心為剪接馬可夫轉移矩陣的 Felsenstein 修剪演算法（Pruning Algorithm），對樹狀拓撲具有高度非線性特徵。

---

### 3. 假設集合 (Explicit Assumptions)
* **A1（Compactness）**：最大演化時間與分支長度有界，即樹空間的連續部分限制於一個緊緻集（Compact set） $\mathbf{t} \in [0, t_{max}]^{2M-3}$。
* **A2（Noise Definition）**：觀測數據中的噪點與定序誤差分佈符合有界獨立同分佈（i.i.d. Bounded Noise），且突變速率轉移矩陣（如 Jukes-Cantor 或 GTR）的隨機擾動服從亞高斯（sub-Gaussian）分佈。
* **A3（Lipschitz Continuity）**：對數概似函數 $\ln P(D|\tau, \mathbf{t})$ 關於分支長度 $\mathbf{t}$ 是 Lipschitz 連續的，其 Lipschitz 常數為 $L_{\phi}$。
* **A4（Bounded Measure）**：拓撲搜尋引擎與交叉驗證器的動態權重調控策略 $G$ 是有界且勒貝格可測的（Bounded and Measurable）。
* **A5（Diminishing Step）**：模擬退火或隨機搜索的步長（冷卻係數）與動態調整權重隨時間步 $\eta_t$ 滿足遞減條件：$\sum_{t=1}^{\infty} \eta_t = \infty$ 且 $\sum_{t=1}^{\infty} \eta_t^2 < \infty$。

---

### 4. 可驗證命題 (Testable Propositions)
#### 分佈收斂與平穩性命題（Distributional Convergence Statement）：
在隨機動態搜索下，狀態 $X_t = (\tau_t, \mathbf{t}_t)$ 的機率分佈會以全變差變數（Total Variation Distance）收斂至目標後驗機率分佈（Posterior Distribution） $P(X|D)$。
$$\lim_{t \rightarrow \infty} \|\mathbb{P}(X_t \in \cdot) - P(X|D)\|_{TV} = 0$$
且其目標概似函數期待值滿足收斂性：
$$\mathbb{E}[\phi(X_t, O)] \rightarrow \phi^*(D)$$

---

### 5. 穩定性分析 (Lyapunov / Contractive Check)
構造李亞普諾夫能量函數 $V(X)$ 為當前狀態與最優拓撲結構（或目標後驗分佈）之間的 Kullback-Leibler 散度（KL Divergence）：
$$V(X_t) = D_{KL}(\delta_{X_t} \| P(X|D)) = -\ln P(D|X_t) - \ln P(X_t) + \ln P(D)$$
檢查差分期望值：
$$\mathbb{E}[V(X_{t+1}) | X_t] - V(X_t) = -\sum_{X_{t+1}} T(X_{t+1}|X_t, U_t) \ln \left( \frac{P(D|X_{t+1})P(X_{t+1})}{P(D|X_t)P(X_t)} \right) \le 0$$
由於轉移機率矩陣 $T$ 滿足細緻平衡條件（Detailed Balance），該差分在平均意義下嚴格小於等於 0，證明該隨機動力系統在平衡狀態（後驗分佈）上具有**隨機穩定性（Stochastic Stability）**。

---

### 6. 可驗證性要求 (Experimental Validity)
* **如何模擬系統**：使用馬可夫鏈蒙地卡羅（MCMC）演算法或動態粒子濾波器（Particle Filter），在給定的離散序列矩陣 $D$ 下模擬 $X_t$ 的轉移軌跡。
* **如何測量收斂**：計算潛在尺度縮減因子（Potential Scale Reduction Factor, PSRF, 即 $\hat{R}$ 值）。當 $\hat{R} < 1.05$ 時，視為馬可夫鏈已進入平穩分佈，完成收斂。
* **如何驗證穩定性**：透過交叉驗證器進行 Bootstrap 抽樣，統計重複運行 1000 次後，特定分支拓撲（Split）的出現頻率（應高於 95% 閾值）。
* **如何估計誤差**：利用有效樣本量（Effective Sample Size, ESS）評估隨機抽樣的自相關誤差，並計算分支長度的 95% 最高後驗密度區間（HPD Index）。

---

### 7. 系統分類
* **Estimation System**（估計祖先狀態與分支長度）
* **Optimization System**（極大似然法與最大簡約法的拓撲搜尋）
* **Stochastic Dynamical System**（基於 MCMC 空間轉移的隨機演化動力學）

---

### 8. 最終理論輸出 (Theorem Form)
#### 定理（拓撲馬可夫演化控制系統之收斂與穩健性定理）
If assumptions A1–A5 hold, then:
在觀測矩陣 $O$ 固定且滿足有界噪聲條件下，系統控制策略 $G$ 能確保狀態序列 $X_t$ 構成一個幾何遍歷（Geometrically Ergodic）的馬可夫鏈，其**分佈收斂性（Distributional Convergence）**成立；且最終輸出的最優拓撲分支圖在 Bootstrap 自助重採樣下具有**統計穩定性（Statistical Stability）**。

---

### 9. 一句話理論本質
> 本系統本質上是一個在非連續拓撲結構與連續時間參數之流形空間中，以 Kullback-Leibler 散度為李亞普諾夫能量函數，進行隨機逼近與後驗概率測度收斂的隨機反饋控制系統。
