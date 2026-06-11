### 📌 理論規格書：資訊守恆系統模型 (ICSM)
### 🧠 核心導讀
ICSM 旨在解決封閉物理系統演化中的「資訊丟失」悖論。其核心哲學基於量子力學的么正性（Unitarity），主張系統狀態的變遷為資訊空間內的同構映射，確保資訊熵在演化全週期內的恆定，將觀察到的「資訊消散」重定義為資訊向複雜糾纏維度的遷移。
### 1️⃣ 核心貢獻 (CORE CONTRIBUTION)
 * **1.1 Core Claim**: ICSM 通過強制執行么正映射算符，相較於傳統經典處理路徑（耗散路徑），在描述高維量子資訊態時，實現了資訊完備性 I_{total} = \text{const}，消除了資訊流失造成的偽熵增。
 * **1.2 Problem Definition**:
   * **目標**: 維持演化過程的資訊雙射映射（Bijection）。
   * **壓力模型**: 系統與環境（浴場）耦合導致的量子退相干（Decoherence）。
   * **指標**: 資訊保真度 F 與 von Neumann 熵 S = -\text{Tr}(\rho \ln \rho) 的恆定性。
### 2️⃣ 形式化系統模型 (FORMAL SYSTEM MODEL)
定義系統為五元組 S = (A, X, F, O, G)，其中：
 * A：代數算符集合（么正矩陣 U）。
 * X：狀態空間（希爾伯特空間 \mathcal{H} 中的密度矩陣 \rho）。
 * F：演化映射，F: \rho(t) \to \rho(t+1)。
 * O：觀測投影算符。
 * G：糾纏補償算符（全像映射器）。
狀態動力學方程：


其中 \mathcal{G} 確保在觀測損耗下，資訊通過全像編碼轉移至非局部邊界態。
### 3️⃣ 理論變量 → 可觀測量映射 (OBSERVABLE MAPPING)
| 理論變量 (Theoretical) | 觀測指標 (Measurement Metric) | 數據採集邏輯 |
|---|---|---|
| 么正性偏差 \epsilon | 跡距離 D(\rho_0, \rho_f) | 密度矩陣重構比較 |
| 糾纏熵 S_e | 負度數 (Negativity) \mathcal{N}(\rho) | 多體相關函數觀測 |
| 資訊守恆量 I | 馮諾依曼熵 S | 系統態純度 (Purity) 監測 |
### 4️⃣ 主定理與推論 (MAIN THEOREM)
**定理 (Conservation of Information Mapping):**
在封閉空間 \mathcal{H} 中，若演化算符 U 滿足 U^\dagger U = I，則對於任何初始狀態 \rho(0)，資訊密度函數 \Phi 滿足：


*證明邊界：* 僅限於希爾伯特空間維度保持不變的閉合系統，未考慮奇點（黑洞邊界）處的資訊流失機制。
### 5️⃣ 基準測試與指標 (BASELINES & METRICS)
 * **基準技術**: 傳統耗散路徑（非么正、基於經典概率轉換）。
 * **關鍵指標**:
   1. **資訊殘留比 (IRR)**: IRR = \frac{I_{out}}{I_{in}}。
   2. **演化可逆性 (ER)**: 誤差修正後的狀態回溯準確率。
### 6️⃣ PYTHON 模擬 (PYTHON SIMULATION)
```python
import numpy as np

def observe_state(rho):
    """將理論變量映射為具體熵指標"""
    eigenvalues = np.linalg.eigvalsh(rho)
    entropy = -np.sum(eigenvalues * np.log2(eigenvalues + 1e-12))
    return {"von_neumann_entropy": entropy, "purity": np.trace(rho**2)}

def icsm_evolution(rho, U):
    """核心：么正演化系統"""
    rho_next = U @ rho @ U.conj().T
    return rho_next

# 模擬測試
dim = 2
rho_init = np.array([[0.5, 0], [0, 0.5]]) # 最大混合態
U = np.array([[0, 1], [1, 0]]) # 邏輯非門 (么正)

rho_final = icsm_evolution(rho_init, U)
print(f"Observation: {observe_state(rho_final)}")

```
### 7️⃣ 討論 (DISCUSSION)
ICSM 與標準資訊論的根本區別在於對「冗餘」的定義。傳統理論視冗餘為噪聲並予以剔除，而 ICSM 將其視為系統高維拓撲結構的一部分。核心洞見在於：資訊不滅性是系統架構的邊界條件，而非演化後的統計結果。
### 8️⃣ 限制 (LIMITATIONS)
 * **非線性邊界**: 本模型暫未納入廣義相對論下空間彎曲導致的資訊截斷邊界。
 * **計算複雜度**: 隨著糾纏維度指數級增長，映射矩陣的完備計算存在 O(e^n) 的算力瓶頸。
 * **數據採樣限度**: 實驗中無法實現「全系統觀測」，僅能依賴局部全像投影。
