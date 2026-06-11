我們研究自然界中某些行為模式長期穩定、不易被新策略取代的現象，並用「演化穩定策略（ESS）」建立數學模型。假設群體中個體可選擇攻擊、妥協或躲避等策略，每種策略有不同收益與成本，群體策略比例會依適應度自我調整，並考慮隨機突變，觀察穩定性。透過模擬，我們可追蹤哪些策略最終成為 ESS，哪些被淘汰，並量化收斂、穩定性及群體多樣性。本研究將自然界的策略競爭抽象為可分析、可計算的系統，幫助理解行為模式長期存在的原因。從人工智慧角度看，此模型為多智能體強化學習（MARL）提供理論支持，特別在策略魯棒性與抗突變性上。未來 AI 智能體可模仿自然的適應度調節，演化出即使面對未知挑戰者也能自我防禦、維持系統穩定的「演化魯棒策略」，不再僅追求單一最優解。


# 《隨機複製動態下的演化穩定策略分析》  
**English:** Evolutionarily Stable Strategies under Stochastic Replicator Dynamics

---

## 1. 系統定義（Concrete Formalization）

**系統空間選擇：**  
`probability simplex` \(\Delta^n \subset \mathbb{R}^n\)  
代表 \(n\) 種策略在群體中的分佈。

**State Space**  
\[
X := x_t \in \Delta^n,\quad x_t^i \ge 0,\ \sum_{i=1}^n x_t^i = 1
\]

**Observation Space**  
\[
O_t := (A_t, V_t, C_t)
\]  
- \(A_t \in \mathbb{R}^{n \times n}\)：博弈報酬矩陣（payoff matrix）  
- \(V_t \in \mathbb{R}_+\)：資源價值  
- \(C_t \in \mathbb{R}_+\)：衝突成本  

**Signal Space**  
\[
S_t := f(X_t, O_t) \in \mathbb{R}^n
\]  
各策略適應度向量（fitness signal）

**Control Space**  
\[
U_t := (\eta_t, \mu_t)
\]  
- \(\eta_t\)：學習/更新步長  
- \(\mu_t\)：突變率（mutation rate）

---

## 2. 明確動態系統（Well-defined Dynamics）

**Fitness Function**（linear / Lipschitz）
\[
f_i(X_t,O_t) = (A_t X_t)_i + V_t - C_t \cdot \sum_{j \ne i} x_t^j
\]

**Strategy Update (stochastic nonlinear replicator-mutator dynamics)**
\[
X_{t+1} = F(X_t,O_t,U_t,\theta)
\]

\[
x_{t+1}^i =
(1-\mu_t)x_t^i \cdot \frac{f_i(X_t,O_t)}{\bar f(X_t,O_t)}
+ \mu_t \cdot \frac{1}{n}
\]

其中  
\(\bar f(X_t,O_t) = \sum_i x_t^i f_i(X_t,O_t)\)

**Signal Mapping**
\[
S_t = \phi(X_t,O_t) = f(X_t,O_t)
\]

**Control Policy (linear-bounded policy)**
\[
U_t = G(S_t,\theta)
\]

\[
\eta_t = \sigma(\|S_t\|), \quad \mu_t = \min(\mu_{max}, \|\nabla S_t\|)
\]

G 為 **Lipschitz + bounded neural policy**

---

## 3. 假設集合（Explicit Assumptions）

- **A1.** \(\Delta^n\) 是緊緻且凸的  
- **A2.** 報酬矩陣 \(A_t\) 有界: \(\|A_t\|_\infty \le M\)  
- **A3.** \(F\) Lipschitz: \(\|F(x)-F(y)\| \le L\|x-y\|\)  
- **A4.** \(G\) 可測且有界: \(\eta_t \in (0,1], \mu_t \in [0,\mu_{max}]\)  
- **A5.** 步長穩定: \(\sum_t \eta_t = \infty, \sum_t \eta_t^2 < \infty\)  
- **A6.** 噪聲（mutation）為有界 sub-Gaussian

---

## 4. 可驗證命題（Testable Propositions）

**Proposition 1 (Mean Payoff Convergence)**  
\[
\mathbb{E}[\bar f(X_t)] \rightarrow \bar f^*
\]  
收斂至 Nash / ESS 鄰域。

**Proposition 2 (State Convergence)**  
\[
X_t \rightarrow X^* \in \Delta^n
\]  
其中 \(X^*\) 為 ESS 或混合 Nash equilibrium。

**Proposition 3 (Boundedness)**  
\[
\|X_t\|_2 \le 1,\ \forall t
\]

---

## 5. 穩定性分析（Lyapunov / Contractive Check）

**Lyapunov 函數**
\[
V(X_t) = - \bar f(X_t) = -X_t^T A_t X_t
\]

**Stability Condition**  
在對稱博弈下：
\[
V(X_{t+1}) - V(X_t) \le 0
\]  
因 replicator dynamics 保證 \(\bar f(X_t)\) non-decreasing，所以 \(V\) non-increasing。

**Contraction Condition (Local)**  
若 ESS 存在 \(X^*\)，則：
\[
\rho(J_F(X^*)) < 1
\]  
(Jacobian spectral radius < 1)

---

## 6. 可驗證性要求（Experimental Validity）

**模擬方法**  
- Monte Carlo population simulation  
- replicator-mutator iteration  
- random payoff perturbation \(A_t + \epsilon\)

**收斂測量**  
- \(\|X_{t+1}-X_t\|\)  
- entropy reduction: \(H(X_t) = -\sum x_i \log x_i\)

**穩定性驗證**  
- inject mutant strategy \(e_i\)  
- measure invasion fitness: \(f(e_i, X^*) - f(X^*, X^*)\)

**誤差估計**  
\(\epsilon_t = \|X_t - X^*\|\)

---

## 7. 系統分類

- ✔ Evolutionary Game System  
- ✔ Stochastic Dynamical System  
- ✔ Optimization System  
- ✔ Hybrid Feedback System  

---

## 8. 最終定理（Theorem Form）

**Theorem (ESS Convergence under Replicator–Mutator Dynamics)**

If assumptions A1–A6 hold, then:

- \(X_t \in \Delta^n\) for all \(t\)  
- expected mean payoff is non-decreasing  
- \(X_t\) converges in probability to a neighborhood of an ESS \(X^*\)  

\[
X_t \xrightarrow{p} X^*
\]

and \(X^*\) is locally asymptotically stable under mutation perturbations.

---

## 9. 一句話理論本質

**ESS 是在隨機擾動與策略複製動態下，使群體分佈進入不可被入侵的穩態概率吸引子。**
