# 维度5：黑洞阴影（Black Hole Shadow）

## Π 的角色

黑洞阴影（Shadow）是事件视界附近光子环（Photon Ring）在远处观察者看来投影的暗区。

阴影的**角直径**（angular diameter）公式为：

\[
\theta = \frac{2 \cdot r_{\text{shadow}}}{D}
\]

其中：
- \(r_{\text{shadow}}\)：阴影半径（与 \(M\) 成正比）
- \(D\)：黑洞到观察者的距离

阴影的**面积**公式为：

\[
A_{\text{shadow}} = \pi \cdot \left(\frac{\theta \cdot D}{2}\right)^2
\]

**Π 出现在阴影面积公式中**（π 乘以半径的平方）。

---

## 阴影半径公式（Kerr 黑洞）

对于 Kerr 黑洞（自旋 \(a_*\)），阴影半径 \(r_{\text{shadow}}\) 取决于观测角度 \(\theta_o\)（相对于自旋轴）。

近似公式（来自 EHT 2019 Paper IV）：

\[
r_{\text{shadow}}(a_*, \theta_o) \approx \sqrt{27} \cdot \frac{GM}{c^2} \cdot f(a_*, \theta_o)
\]

其中 \(f(a_*, \theta_o)\) 是自旋和观测角度的修正因子。

对于**（face-on，\(\theta_o = 0\)）：**

\[
r_{\text{shadow}}^{\text{face-on}} \approx \sqrt{27} \cdot \frac{GM}{c^2} \cdot (1 - a_* + \ldots)
\]

对于**（edge-on，\(\theta_o = \pi/2\)）：**

\[
r_{\text{shadow}}^{\text{edge-on}} \approx \sqrt{27} \cdot \frac{GM}{c^2} \cdot \sqrt{1 - a_*^2 + \ldots}
\]

---

## 观测数据（EHT）

### M87*（2019 年首次成像）
- 质量：\(M = 6.5 \times 10^9 \, M_\odot\)
- 距离：\(D = 16.8 \, \text{Mpc}\)
- 阴影角直径：\(\theta = 42 \pm 3 \, \mu\text{as}\)
- 数据来源：EHT Collaboration, *ApJL* 2019, doi:10.3847/2041-8213/ab0e85

### Sgr A*（2022 年成像）
- 质量：\(M = 4.3 \times 10^6 \, M_\odot\)
- 距离：\(D = 8.2 \, \text{kpc}\)
- 阴影角直径：\(\theta = 48 \pm 7 \, \mu\text{as}\)
- 数据来源：EHT Collaboration, *ApJL* 2022, doi:10.3847/2041-8213/ac6674

---

## 计算任务

1. **给定 \(M, a_*, D\)，计算阴影角直径 \(\theta\)**
   - 与 EHT 观测对照
2. **给定 \(\theta, D\)，推断黑洞质量 \(M\)**
   - 与 EHT 给出的质量对照
3. **自旋 \(a_*\) 对阴影形状的影响**
   - 自旋越高，阴影越不圆（EHT 用此估算 \(a_*\)）

---

## Π 的再次出现

| 维度 | Π 的角色 |
|------|----------|
| 1. 视界面积 | \(A = 16\pi (GM/c^2)^2\) |
| 2. 霍金温度 | \(T = \hbar c^3 / (8\pi G M k_B)\) |
| 3. 准正则模 | \(\omega_R = 2\pi f_R\) |
| 4. 自旋进动 | \(T = 2\pi / \Omega_{LT}\) |
| 5. 黑洞阴影 | \(A_{\text{shadow}} = \pi \cdot (r_{\text{shadow}})^2\) |

**Π 始终是黑洞几何与物理的核心常数。**

---

## 下一步

运行 `code/blackhole_shadow.py` 计算 M87* 和 Sgr A* 的阴影角直径，与 EHT 观测对照。
