這個「演化收斂理論」其實可以用很直白的方式理解：

在一個AI視角裡，我把一群解想成一群正在亂試答案的智能體，每一代都有一批候選解在空間裡探索。我會先評分（適應度函數），好的留下，差的被淘汰，這是「選擇」。接著讓部分解互相混合特徵（交配），再加上一點隨機干擾（突變），避免整群人卡死在同一個局部答案。

關鍵是這個系統不是完全隨機，而是有一個「動態控制器」：如果大家太相似（多樣性下降），我就提高突變率，強迫探索；如果已經很分散，就降低突變，專心收斂。再加上一條鐵律：每一代最好的解一定被保留，不會被破壞。

從AI的角度看，這其實是在做一件事：在「探索未知」和「加速收斂」之間自動調平衡。長期下來，因為永遠保留最優解、又保證偶爾能跳出局部最優，系統會像一個帶噪聲但有記憶的優化器，逐步逼近全域最佳解。


# 演化收斂理論 (Evolutionary Convergence Theory)

## 1. 系統定義 (Concrete Formalization)

本系統強制映射至 **機率單體空間** \(\Delta^{N-1}\) 與 **歐幾里得空間** \(\mathbb{R}^d\) 的笛卡爾積。

- 群體大小：\(N\)  
- 個體基因長度：\(d\)  
- 解空間：\(\mathcal{X} \subset \mathbb{R}^d\)  
- 當前 \(t\) 世代的群體：
\[
X_t = [x_{t,1}, x_{t,2}, \dots, x_{t,N}]^T \in \mathcal{X}^N
\]  
- 經驗機率分布：
\[
\mu_t \in \Delta^{N-1}
\]

### 狀態空間 (State Space) \(X\)

整個群體中所有 \(N\) 個個體的基因組狀態。

### 觀測空間 (Observation Space) \(O\)

群體中每個個體經由適應度函數映射後得到的適應度向量：
\[
O_t = [f(x_{t,1}), f(x_{t,2}), \dots, f(x_{t,N})]^T
\]

### 信號空間 (Signal Space) \(S\)

- 選擇機率分布：\(p_t \in \Delta^{N-1}\)  
- 群體多樣性指數：\(div_t \in \mathbb{R}^+\)

### 控制空間 (Control Space) \(U\)

控制參數：
\[
U_t = [p_c(t), p_m(t)]^T
\]  
- \(p_c(t)\)：交配機率  
- \(p_m(t)\)：突變機率（動態調整）

---

## 2. 系統動態 (Well-defined Dynamics)

系統由隨機轉移算子構成，其非線性離散時間狀態方程式：

\[
X_{t+1} = F(X_t, U_t) = M \circ C \circ S_{sel} (X_t)
\]

- **選擇算子 \(S_{sel}\)**：基於 \(O_t\) 隨機抽樣  
- **交配算子 \(C\)**：非線性片段重組  
- **突變算子 \(M\)**：隨機擾動

控制策略：
\[
p_m(t) = \min\left(p_{\max}, \frac{\theta_m}{div_t + \epsilon}\right)
\]

信號映射：
\[
p_{t,i} = \frac{O_{t,i}}{\sum_j O_{t,j}}, \quad
div_t = \frac{1}{N} \sum_{i=1}^N \| x_{t,i} - \bar{x}_t \|_2
\]

---

## 3. 假設集合 (Explicit Assumptions)

| 編號 | 假設內容 |
|------|---------|
| **A1** | 狀態空間 \(\mathcal{X} \subset \mathbb{R}^d\) 有界緊緻: \(\|x\|_2 \le M_x\) |
| **A2** | 突變算子隨機擾動有界，確保個體不逸出 \(\mathcal{X}\) |
| **A3** | 適應度函數 \(f\) 利普希茨連續：\(|f(x)-f(y)| \le L_f \|x-y\|_2\) |
| **A4** | 控制參數有界：<br> \(p_c(t) \in [p_{c,min}, p_{c,max}]\) <br> \(p_m(t) \in [p_{m,min}, p_{m,max}]\), \(p_{m,min} > 0\) |
| **A5** | 精英保留策略：每代保留當前最佳個體 \(x_t^* = \arg\max_{x\in X_t} f(x)\) |

---

## 4. 可驗證命題 (Testable Propositions)

### 命題 1：分布收斂性與全域最優收斂

在 **精英保留**與 **持續突變 (p_{m,min} > 0)** 條件下，當 \(t \to \infty\)：
\[
x_t^{best} \xrightarrow{a.s.} \mathcal{X}^*
\]

---

## 5. 穩定性分析 (Lyapunov / Contractive Check)

定義隨機 Lyapunov 函數：
\[
V(X_t) = \| x_t^{best} - x^* \|_2 \ge 0
\]

- 精英保留策略 (A5)：  
  \(f(x_{t+1}^{best}) \ge f(x_t^{best}) \implies V(X_{t+1}) - V(X_t) \le 0\)
- 持續突變 (A4)：  
  從任意 \(X_t\) 出發，轉移到包含更優解的狀態概率 \(\delta > 0\)

依據 **超鞅收斂定理 (Supermartingale Convergence Theorem)**，系統隨機穩定。

---

## 6. 可驗證性要求 (Experimental Validity)

1. **模擬方法**  
   - 選擇基準函數：Rastrigin、Rosenbrock  
   - 群體大小 \(N\)、基因長度 \(d\) 固定  
   - 蒙地卡羅模擬 \(M=1000\) 次
2. **收斂測量**  
\[
\frac{1}{M}\sum_{m=1}^M f(x_{t,m}^{best})
\]  
   - 繪製歷代最優適應度曲線
3. **穩定性驗證**  
   - 確認 Lyapunov 軌跡 \(V(X_t)\) 單調下降
4. **誤差估計**  
   - 計算最終解與全域最優解殘差：
\[
\| x_T^{best} - x^* \|_2
\]  
   - 提供 95% 置信區間

---

## 7. 系統分類

- Optimization System  
- Stochastic Dynamical System  
- Hybrid Feedback System

---

## 8. 最終理論輸出 (Theorem Form)

### 定理 1 (演化收斂定理)

> 若假設 A1–A5 成立，則系統的最佳狀態序列 \(x_t^{best}\) 將展現**隨機漸近穩定性 (Stochastic Asymptotic Stability)**，歷史最佳個體序列以機率 1 收斂至全域最優解集合 \(\mathcal{X}^*\)：
\[
x_t^{best} \xrightarrow{a.s.} \mathcal{X}^*
\]

---

## 9. 理論本質一句話

> 本系統是一個**透過非線性隨機擾動維持全域遍歷性，並藉由耗散型精英選擇與動態反饋反壓，確保狀態分佈向全域最優解單調收斂的馬可夫決策與優化系統。**
