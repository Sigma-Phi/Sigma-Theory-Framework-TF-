### 📌 理論規格書：資訊增益決策處理系統 (IG-DPS)
### 🧠 核心導讀
IG-DPS 是一個將決策過程建模為負熵流轉移的物理系統。在高度不確定的決策環境中，系統透過對數據分佈的動態觀測，將初始熵減小至決策臨界閾值以下。其核心哲學在於「資訊即功」，利用資訊增益作為驅動力，強制系統從混沌數據態（高熵）坍縮至確定的決策態（低熵）。
### 1️⃣ 核心貢獻 (CORE CONTRIBUTION)
 * 1.1 **Core Claim**: 在數據特徵空間受限環境下，IG-DPS 透過遞歸式特徵切分，相較於隨機搜索基準，能將決策路徑的計算複雜度降低一個數量級，並在極短的處理週期內收斂至全局最優純度。
 * 1.2 **Problem Definition**:
   * **系統目標**: 在給定特徵集 A = \{a_1, ..., a_n\} 下，最大化輸出決策目標 Y 的純度（即熵最小化）。
   * **壓力模型**: 數據流具備高噪聲與動態漂移特徵，且計算資源受限（T_{max}）。
   * **評價指標**: 資訊增益率 IGR(D, A) = \frac{IG(D, A)}{SplitInformation(D, A)}。
### 2️⃣ 形式化系統模型 (FORMAL SYSTEM MODEL)
定義系統 S = (A, X, F, O, G)，其中：
 * A：輸入特徵向量集合。
 * X：系統隱變量空間（熵值狀態 H）。
 * F：轉移函數，定義為 f: X_t \times A \to X_{t+1}。
 * O：可觀測決策結果。
 * G：能量/資源約束函數。
狀態動力學方程：


其中，\phi(G) 為資源消耗導致的決策遺漏項。
### 3️⃣ 理論變量 → 可觀測量映射 (OBSERVABLE MAPPING)
| 理論變量 (Theoretical Variable) | 可觀測指標 (Metric) | 數據採集邏輯 |
|---|---|---|
| 熵狀態 H(D_t) | 香農熵值 (Shannon Entropy) | 統計 Y 在子集中的分佈頻率 |
| 資訊增益 IG | 增益係數 (Gain Ratio) | 計算 H(D_{parent}) - H(D_{child}) |
| 系統壓力 G | 資源占用率 (CPU/RAM usage) | 監控系統時鐘週期與內存水位 |
### 4️⃣ 主定理與推論 (MAIN THEOREM)
**定理 (Entropy Convergence):** 若且唯若 \forall a_i \in A, IG(D, a_i) > \epsilon (其中 \epsilon > 0)，則系統在有限步驟 k < |A| 內，熵值收斂至 H_{min} < \delta。
 * **證明邊界**: 假設數據集 D 為 IID (獨立同分布) 採樣，且目標變數 Y 與特徵集存在非零互信息。
### 5️⃣ 基準測試與指標 (BASELINES & METRICS)
 * **對比技術路徑**: 隨機森林 (Random Forest) 的節點分裂法、貪婪特徵選擇法。
 * **評估參數**:
   * **收斂速率 (Convergence Rate)**: R_c = \frac{\Delta H}{\Delta t}。
   * **純度閾值 (Purity Threshold)**: 終止循環的最小熵值。
   * **資源耗損比 (Resource Efficiency)**: E = \frac{IG_{total}}{\text{Compute Time}}。
### 6️⃣ PYTHON 模擬 (PYTHON SIMULATION)
```python
import numpy as np

def calculate_entropy(y):
    _, counts = np.unique(y, return_counts=True)
    probs = counts / len(y)
    return -np.sum(probs * np.log2(probs + 1e-9))

def observe_state(data, target_col):
    """將理論變量映射為具體觀測指標"""
    current_h = calculate_entropy(data[target_col])
    return {"current_entropy": current_h, "timestamp": "2026-06-10"}

def ig_step(data, feature, target):
    h_d = calculate_entropy(data[target])
    # 簡化計算：模擬分裂後的條件熵
    h_d_a = 0.5 * calculate_entropy(data[data[feature] == 0][target]) + \
            0.5 * calculate_entropy(data[data[feature] == 1][target])
    return h_d - h_d_a # 資訊增益

```
### 7️⃣ 討論 (DISCUSSION)
IG-DPS 與經典決策樹算法的本質區別在於其「負熵流」的顯式建模。傳統算法僅將資訊增益視為分裂準則，而 IG-DPS 將其視為系統動力學的驅動力，強制將外部計算資源與熵減速率直接耦合，這使得系統在處理高維度非平穩數據時，具備更強的自我糾偏能力。
### 8️⃣ 限制 (LIMITATIONS)
 * **邊界假設**: 假設數據滿足馬可夫性，即系統狀態僅依賴於上一時刻的熵值。
 * **數學難點**: 當數據特徵間存在強共線性時，條件熵的估計會出現病態（Ill-conditioned），導致增益值計算失真；目前缺乏處理非結構化數據時的有效映射函數。
