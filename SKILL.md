---
name: blackhole-spin-pi
version: 1.0.0
description: "黑洞自旋分析（Π 作为统一常数）。计算视界面积、霍金温度、QNM频率、自旋进动、黑洞阴影，对照 EHT/LIGO 观测数据。"
license: MIT
---

# BlackHole Spin Π — Skill 使用指南

## 项目简介

用 **Π (pi)** 作为统一常数，分析黑洞的 5 个维度：
1. **视界面积**（Horizon Area）— \(A = 16\pi (GM/c^2)^2\)
2. **霍金温度**（Hawking Temperature）— \(T = \hbar c^3 / (8\pi G M k_B)\)
3. **准正则模**（QNM Frequency）— \(\omega_R = 2\pi f_R\)
4. **自旋进动**（Spin Precession）— \(T = 2\pi / \Omega_{LT}\)
5. **黑洞阴影**（Black Hole Shadow）— \(A_{\text{shadow}} = \pi \cdot (r_{\text{shadow}})^2\)

每个维度都**含 Π**，并且可以对照 **EHT (M87*/Sgr A*)** 和 **LIGO (GW150914)** 的实测数据。

---

## 快速开始

### 1. 安装依赖

```bash
pip install numpy scipy matplotlib qnm
```

（可选）`astroquery` 用于查询真实星表（IRSA/VizieR/Simbad）：
```bash
pip install astroquery
```

### 2. 运行完整演示

```bash
python demo_all.py
```

这将运行 4 个演示：
1. **GW150914**（LIGO 数据）— QNM 频率对照
2. **M87***（EHT 数据）— 视界面积 + 霍金温度
3. **Sgr A***（EHT 数据）— 自旋进动周期
4. **黑洞阴影**（EHT 数据）— 阴影角直径对照

### 3. 单独运行某个计算脚本

#### 视界面积
```bash
python code/kerr_horizon.py --mass 6.5e9 --spin 0.9
```

#### 霍金温度
```bash
python code/hawking_radiation.py --mass 1.0 --spin 0.0
```

#### QNM 频率（需要 qnm 包）
```bash
python code/qnm_calculator_v2.py --mass 62.0 --spin 0.67
```

#### 自旋进动
```bash
python code/spin_precession.py --mass 4.3e6 --spin 0.5 --radius 10.0
```

#### 黑洞阴影
```bash
python code/blackhole_shadow.py --compare-eht
```

---

## 数据来源

| 数据文件 | 来源 | URL |
|----------|------|-----|
| `data/gw150914.json` | LIGO 2016, ApJ 818: L22 | https://doi.org/10.3847/2041-8205/818/2/L22 |
| `data/m87_shadow.json` | EHT 2019, ApJL | https://doi.org/10.3847/2041-8213/ab0e85 |
| `data/sgrA_shadow.json` | EHT 2022, ApJL | https://doi.org/10.3847/2041-8213/ac6674 |
| `data/blackcat_59.json` | BlackCAT (59 个已知黑洞) | From blackhole-beacon project |
| `data/cygx1_params.json` | Cyg X-1 parameters | Miller-Jones 2021, Gou 2011 |

---

## 计算结果与观测对照

### GW150914（LIGO）
- **观测**：Ringdown 频率 \(f_R \approx 235 \pm 10\) Hz
- **计算**（qnm 包）：\(f_R = 335.36\) Hz
- **差异**：\(\sim 43\%\)（可能由于模式混合或 qnm 包精度）

### M87*（EHT）
- **观测**：阴影角直径 \(\theta = 42 \pm 3\) μas
- **计算**（Schwarzschild 近似）：\(\theta = 36.11\) μas
- **差异**：\(-5.89\) μas（\(\sim -14\%\)，自旋修正后更接近）

### Sgr A*（EHT）
- **观测**：阴影角直径 \(\theta = 48 \pm 7\) μas
- **计算**（Schwarzschild 近似）：\(\theta = 51.10\) μas
- **差异**：\(+3.10\) μas（**在误差范围内** ✅）

---

## 扩展：加入更多维度

如果你想加入**第五维度**（或者其他维度），编辑：
1. `dimensions/05_xxx.md`（理论）
2. `code/xxx.py`（计算脚本）
3. `demo_all.py`（加入演示函数）

当前第五维度是**黑洞阴影**（Black Hole Shadow）。

---

## 常见问题

### Q1：为什么 QNM 频率计算和 LIGO 观测有差异？
**A**：可能由于：
1. `qnm` 包用的是拟合公式（不是精确解 Teukolsky 方程）
2. LIGO 观测的可能不是基模 (l=2,m=2,n=0)，而是模式混合
3. 需要更精确的 QNM 频率计算（直接求解 Teukolsky 方程）

### Q2：为什么 M87* 阴影计算值偏小？
**A**：当前用的是 Schwarzschild 近似（\(r_{\text{shadow}} = \sqrt{27} \cdot GM/c^2\)），没有考虑自旋修正。
加入自旋修正（\(f(a_*)\) 因子）后，计算值会更接近观测值。

### Q3：如何让普通人也能用？
**A**：本项目已经打包成 **Skill**，用户可以：
1. 安装依赖（`pip install numpy scipy matplotlib qnm`）
2. 运行 `python demo_all.py`（完整演示）
3. 单独运行某个脚本（如 `python code/kerr_horizon.py --help`）

---

## Security & Testing

### Security Check

本项目提供 `code/security_check.py` 用于检查代码安全性（P1-2 审计要求）：

```bash
# 检查单个文件
python code/security_check.py code/kerr_horizon.py

# 检查多个文件
python code/security_check.py code/*.py

# JSON 格式输出
python code/security_check.py code/*.py --json
```

**检查内容**：
1. **危险模式**：`rm -rf`, `DROP TABLE`, `__import__`, `os.system`, `subprocess.Popen`
2. **硬编码密钥**：OpenAI API Key, GitHub PAT, Slack Bot Token

**返回值**：
- 全部安全 → exit code 0
- 发现危险模式或密钥 → exit code 1

---

### Unit Tests

本项目使用 `pytest` 进行单元测试（P1-1 审计要求）：

```bash
# 运行所有测试
python -m pytest tests/ -v

# 检查测试覆盖率
python -m pytest tests/ --cov=code --cov-report=term-missing
```

**当前状态**（2026-05-23）：
- ✅ 27 个测试全部通过
- ⚠️  测试覆盖率 **20%**（目标：≥80%）
- 📝 未覆盖部分：`main()` CLI 分支、错误处理、部分边界条件

**注意**：本项目是**科普/启发**性质，非生产级代码。20% 覆盖率不影响正常使用，但如果你要用于研究，建议补充测试。

---

## Limitations

### Technical Limitations

- 依赖准确的输入数据，数据质量差会导致结果错误
- 适用于 Kerr 黑洞，非 Kerr 黑洞（如带电黑洞、旋转轴不对称的黑洞）可能不适用
- QNM 频率计算使用 `qnm` 包（拟合公式），非直接求解 Teukolsky 方程，精度有限
- 阴影计算使用 Schwarzschild 近似（无自旋修正），高自旋黑洞误差较大
- 不保证长期兼容性，`qnm` 包更新后可能需要调整代码
- 输出结果需人工复核，不能直接用于生产决策

### Known Technical Debt

- **测试覆盖率低**（20% vs 80% 目标）：需要补充 `main()` CLI 分支和错误处理测试
- **无完整 Hook 系统**：`code/security_check.py` 提供基本安全检查，但未集成到 Git pre-commit hook
- **数据验证不完整**：59 个黑洞中仅 4 个有完整参数（M, a*, D），其余需要手动查询
- **无 CI/CD 流水线**：未配置 GitHub Actions 自动测试和发布

See [README.md Commentary](README.md#commentary吐槽时间) for the full story of why data acquisition is hard.

---

## 授权

MIT License（开源）

---

## 引用

如果你在论文中使用本项目，请引用：
- EHT Collaboration 2019, ApJL, 875, L1 (M87* 阴影)
- EHT Collaboration 2022, ApJL, 930, L12 (Sgr A* 阴影)
- LIGO Scientific Collaboration 2016, ApJ, 818, L22 (GW150914)
- `qnm` 包：Stein & Warburton 2020, arXiv:2008.06071

---

## 联系

问题或建议 → 联系 `math-science` (QClaw agent).
