ISCS（資訊安全完整性系統）可以用白話理解成：它是一個會「邊加密、邊自我調整」的系統。每次資料被加密時，不只是單純用固定公式轉換，而是會把隨機亂數、動態金鑰和內部狀態一起混合進去，讓輸出的密文變得更難被分析。系統還會持續監測密文的統計特性，例如是否太有規律，然後再自動調整加密方式與熵來源，避免被攻擊者找出模式。從數學角度看，它是在一個隨機動態系統中運作，目標是讓密文的分布越來越接近完全隨機，同時確保資訊沒有被破壞或洩漏。簡單說，就是一個會不斷「提高混亂程度並自我修正」的智慧型加密系統，讓資料在不可信環境中依然保持安全與完整。



# 📌 ISCS（Information Security & Integrity Control System）  
## 📌 完整可驗證理論形式化版本（Verification Closure Model）

---

# 1️⃣ 系統定義（Concrete Formalization）

## 📐 選擇數學結構

\[
\textbf{metric space } (X, d) + \textbf{stochastic extension}
\]

---

## 🧩 State / Observation / Signal / Control

### 🟦 state space

\[
X = \{0,1\}^n \times K \times E
\]

其中：

- \(x_t \in \{0,1\}^n\)：密文狀態  
- \(k_t \in K\)：動態金鑰  
- \(e_t \in E \subset \mathbb{R}^m\)：熵源狀態  

---

### 👁 observation space

\[
O = \mathbb{R}^p
\]

（NIST test / KL divergence / correlation metrics）

---

### 📡 signal space

\[
S = \mathbb{R}^m
\]

（熵強度、攻擊指標、噪聲觀測）

---

### 🎛 control space

\[
U = K \times \mathbb{R}^m
\]

（key update + entropy injection control）

---

## 📏 metric 定義

\[
d(x_i, x_j) = \lambda_1 d_H(x_i, x_j) + \lambda_2 D_{KL}(P_i \,\|\, P_j)
\]

---

# 2️⃣ 動態系統（Well-defined Dynamics）

## 🔁 state dynamics

\[
X_{t+1} = F(X_t, O_t, U_t, \theta)
\]

---

## 🔬 展開形式

\[
x_{t+1} = \sigma(x_t \oplus k_t \oplus \eta_t)
\]

\[
k_{t+1} = G_k(k_t, O_t)
\]

\[
e_{t+1} = \phi(e_t, \xi_t)
\]

---

## ⚙ function structure

- \(F\)：nonlinear + stochastic + Lipschitz (piecewise)
- \(G\)：bounded update / neural operator
- \(\phi\)：stochastic contraction process

---

## 🎛 control law

\[
U_t = G(S_t, \theta)
\]

\[
S_t = \phi(X_t, O_t)
\]

---

## 🌪 entropy injection

\[
\eta_t \sim \text{sub-Gaussian}(0, \sigma^2)
\]

---

# 3️⃣ 假設集合（Axioms）

## 📌 A1 — 有界狀態空間

\[
X \subseteq \{0,1\}^n \times K \times E,\quad \text{compact}
\]

---

## 📌 A2 — 噪聲模型

\[
\eta_t \sim \text{sub-Gaussian}, \quad \xi_t \sim \text{bounded noise}
\]

---

## 📌 A3 — Lipschitz continuity

\[
\|F(x)-F(y)\| \le L \|x-y\|
\]

---

## 📌 A4 — 控制有界性

\[
\|G(S_t)\| \le C
\]

---

## 📌 A5 — 時間穩定性

\[
\eta_t \to 0 \quad \text{or annealing bounded schedule}
\]

---

# 4️⃣ 可驗證命題（Testable Propositions）

---

## 📉 Proposition 1 — 熵收斂

\[
D_{KL}(P_{cipher,t} \,\|\, P_{random}) \rightarrow 0
\]

---

## 📉 Proposition 2 — 穩定性

\[
\mathbb{E}[d(X_{t+1}, X_t)] \le \rho \mathbb{E}[d(X_t, X_{t-1})], \quad \rho < 1
\]

---

## 🔐 Proposition 3 — 資訊泄漏上界

\[
I(M; C_t) \le \epsilon
\]

---

# 5️⃣ 穩定性分析（Lyapunov Framework）

---

## 📌 Lyapunov function

\[
V(X_t) =
D_{KL}(P_{cipher,t} \,\|\, P_{uniform})
+ \alpha \|k_t - k^*\|^2
\]

---

## 📉 drift condition

\[
V(X_{t+1}) - V(X_t)
\le -\gamma \|X_t\|^2 + \epsilon
\]

---

## 📌 contraction condition

若：

\[
\|\sigma(x) - \sigma(y)\| \le \rho \|x-y\|,\quad \rho < 1
\]

則：

> stochastic contractive system

---

# 6️⃣ 可驗證性（Experimental Validity）

---

## 🧪 simulation pipeline

- Markov chain cipher simulator  
- RNG entropy injection model  
- adversarial reconstruction testing  

---

## 📊 收斂檢測

- KL divergence → 0  
- entropy → max  
- correlation → 0  

---

## 🧯 stability testing

- perturb \(k_t\)  
- measure output divergence  
- compute Jacobian spectral radius  

---

## 📏 error metric

\[
\epsilon_t = \|P_{empirical} - P_{ideal}\|
\]

---

# 7️⃣ 系統分類（System Class）

✔ Stochastic Dynamical System  
✔ Control System  
✔ Cryptographic Transformation System  
✔ Hybrid Feedback System  
✔ Estimation System  

---

# 8️⃣ 主定理（Main Theorem）

---

## 📌 ISCS Stability & Security Convergence Theorem

若滿足 A1–A5，則：

### (1) 穩定性

\[
X_t \xrightarrow{a.s.} X^*
\]

---

### (2) 安全收斂

\[
D_{KL}(P_{cipher,t} \,\|\, P_{random}) \rightarrow 0
\]

---

### (3) 泄漏有界

\[
I(M;C_t) \le \epsilon
\]

---

# 9️⃣ 一句話理論本質

> ISCS 是一個在隨機控制作用下，使密文分布透過動態熵注入機制收斂至最大熵不動點的收縮型加密動力系統。

---

# 🔟 核心本質總結

👉 本系統本質不是加密算法，而是：

> **在 metric space 上運行的 stochastic contraction dynamics，將資訊流推動至統計均勻不動點。**
