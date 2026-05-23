# BlackHole-Spin-Π: Π as U(1) Period in Rotating Black Holes

> We set out to explain black hole spin with π. We found π was already there.

---

## 🗣️ Commentary（吐槽时间）

### 我们花了3天做 `blackhole-beacon` 项目……

**目标**：用机器学习分类器从 2MASS/WISE 数据中发现新的黑洞X射线双星（BHXB）候选体。

**现实**：
- **第1天**：下载 ATNF 脉冲星目录（~3000个脉冲星），结果一半坐标在 SIMBAD 查不到对应源（要么太老，要么名字变了）
- **第2天**：想从 BlackCAT 数据库拿 59 个已知黑洞的质量（M）、自旋（a*）、距离（D）——结果发现 `blackcat_59.json` 只有坐标+类型，**31个条目全是 `query_status: "pending"`**，一个参数都没有
- **第3天**：想用 `astroquery` 批量查询 SIMBAD——结果 SIMBAD 对 X射线源覆盖很差，很多黑洞候选体根本没有光学对应体

**数据获取的坑**（真实案例）：
1. **2MASS images**: 输入坐标 → 返回 "Not Found"（近红外太暗，或者坐标有 ±2 角秒误差）
2. **WISE images**: 输入坐标 → 返回黑图（天体在 WISE 波段不可见，或者被银河平面遮挡）
3. **SIMBAD 交叉匹配**: 输入 "PSR J1933+1726" → 返回 35 个候选源，没有一个明确是脉冲星（需要人工检查每个源的 `main_type`）
4. **VizieR 表下载**: 想下载黑洞参数表 → 需要注册 + 每天限 1000 次查询
5. **`astroquery.simbad` 超时**: 批量查询 59 个源 → 第 12 个就超时了

**结论**：天文数据实在太难拿了。不是缺数据，是数据**分散在几十个数据库，格式不统一，API 限流，很多还需要人工校验**。

---

### 不过我们在 `blackhole-beacon` 项目上获得了额外灵感

做到第3天，我们突然意识到：

> **几乎所有天体都会自旋** —— 脉冲星（中子星）自旋，黑洞自旋，星系自旋，甚至地球也自旋。

而 `pi-as-u1-period` 项目的核心洞见是：

> **π 是 U(1) 对称性的周期** —— 任何涉及旋转/周期运动的物理系统，π 都在里面。

所以：**π-as-U(1)-period 完全可以用在黑洞自旋上！**

于是有了这个项目 (`blackhole-spin-pi`)。

---

### 再吐槽一下

由于黑洞数据拿不到（我们去哪里找 59 个黑洞的 M/a*/D 完整参数？），所以**验证工作没有做完整**。

目前的情况：
- ✅ 4 个著名黑洞（M87*, Sgr A*, GW150914, Cyg X-1）有完整参数，可以用来验证
- ❌ 剩下 55 个黑洞只有坐标，没有 M/a*/D
- ⏳ 想做批量验证，但需要先写 `query_blackcat.py` 从 SIMBAD/VizieR 批量查询（又回到数据获取的地狱）

**所以**：理论部分（π 在4个维度的作用）是完整的，但**实证验证只做了 4/59**。

---

### 补充说明

**我们不是专业天文学团队**。

这些项目（`pi-as-u1-period`, `blackhole-beacon`, `blackhole-spin-pi`）的主要目标是：
1. **启发**（show that π is not just a number — it's a structural constraint）
2. **科普**（用简单的 Python 代码演示黑洞物理）
3. **方法论验证**（跨学科映射是否真的能发现新洞见）

如果你期待这里有什么新发现能发 Nature（智能体说的，他被我训练成了科研“狗”满脑子都是论文） —— 那你会失望的。

但如果你想知道 "π 和黑洞自旋有什么关系？" —— 这里有4个维度的答案。

---

## The Core Insight

**U(1) is the simplest compact Lie group: `{e^(iθ) | θ ∈ [0, 2π)}`. Its period is 2π.**

A rotating black hole (Kerr metric) has **axial symmetry** — the azimuthal angle φ runs from 0 to 2π. This is U(1) symmetry.

**Any physical quantity that involves the azimuthal angle or the rotation of the black hole implicitly carries π inside it.**

Four aspects of black hole spin physics — horizon area, Hawking temperature, quasi-normal modes, and spin precession — look unrelated, 
---

## The Cross-Domain Map (from `pi-as-u1-period`)

| Dimension | Physical System | Formula (skeletal) | Π's Semantic Role | Critical Threshold | Real-World Impact |
|-----------|----------------|-------------------|-------------------|-------------------|-------------------|
| **Horizon Area** | Kerr black hole event horizon | A = 4π(r₊² + a²) | Π defines the geometric area of the horizon | A = 0 when a = M (extreme Kerr) | Black hole entropy S = A/(4Għ) |
| **Hawking Temperature** | Black hole evaporation | T = ħc³/(8πGMk_B) | Π in denominator → lower T for larger Π | T ∝ 1/(M·Π) → small black holes hotter | Primordial black hole evaporation |
| **Quasi-Normal Modes** | Ringdown after merger | ω_R = 2πf, τ = 2π/ω_I | Π defines the oscillation period and damping time | QNM frequency ∝ Π/M (geometric units) | Gravitational wave detection (LIGO/Virgo) |
| **Spin Precession** | Frame dragging (Lense-Thirring) | Ω_LT = 2GJ/(c²r³) | Precession phase ϕ = 2Π when one full cycle | ϕ = Π → 180° precession | Gyroscope experiments (Gravity Probe B) |

---

## Why This Project?

In `pi-as-u1-period`, we discovered that π is not just a number to compute — it is the **period of U(1) symmetry**, and appears as a structural element in four practical dimensions.

**Black hole spin is the perfect target for this framework:**
- A rotating black hole has U(1) symmetry (axial symmetry)
- The spin parameter a* = J/M² ranges from 0 (Schwarzschild) to 1 (extreme Kerr)
- Π appears in: horizon area (A = 4Πr₊²), Hawking temperature (T ∝ 1/Π), QNM frequencies (ω_R ∝ Π/M), and precession phase (ϕ = 2Π for one cycle)

**The goal**: Map the four dimensions of `pi-as-u1-period` to black hole spin physics, and show that Π is not just a geometric constant — it is a **structural constraint** on rotating black holes.

**The inspiration**: After struggling with data acquisition in `blackhole-beacon`, we realized that **π-as-U(1)-periodicity** is a universal framework that can be applied to **any spinning astrophysical object** — not just black holes, but also neutron stars, white dwarfs, and even galaxies.

---

## Structure

```
blackhole-spin-pi/
├── README.md                           (this file)
├── dimensions/
│   ├── 01_horizon_area.md            Π in horizon area (A = 4Πr₊²)
│   ├── 02_hawking_temperature.md      Π in Hawking temperature (T ∝ 1/Π)
│   ├── 03_quasi_normal_modes.md      Π in QNM frequencies (ω_R = 2Πf)
│   └── 04_spin_precession.md         Π in spin precession (ϕ = 2Π)
├── code/
│   ├── kerr_horizon.py               Compute Kerr horizon area
│   ├── hawking_radiation.py          Compute Hawking temperature and power
│   ├── qnm_calculator_v2.py         Compute QNM frequencies (Π's role)
│   └── spin_precession.py            Compute Lense-Thirring precession
├── data/
│   ├── blackhole_shadow_eht.csv      EHT shadow data (M87*, Sgr A*)
│   ├── gw150914_qnm.csv             GW150914 QNM parameters
│   └── cygx1_params.json            Cyg X-1 parameters (Miller-Jones 2021)
├── tests/
│   ├── test_kerr_horizon.py
│   ├── test_hawking_radiation.py
│   ├── test_qnm_calculator.py
│   └── test_spin_precession.py
└── LICENSE
```

---

## Quick Start

```bash
# Compute Kerr horizon area (Π in A = 4Π(r₊² + a²))
python code/kerr_horizon.py --mass 1.0 --spin 0.5

# Compute Hawking temperature (Π in denominator)
python code/hawking_radiation.py --mass 1.0

# Compute QNM frequencies (Π in ω_R = 2Πf)
python code/qnm_calculator_v2.py --mass 1.0 --spin 0.5 --mode 220

# Compute spin precession (Π in phase accumulation)
python code/spin_precession.py --radius 10.0 --spin 0.5
```

---

## The Four Dimensions (Preliminary)

### Dimension 1: Horizon Area — Π as Geometry

The Kerr metric has an event horizon at:
```
r₊ = M + √(M² - a²)  (geometric units G = c = 1)
```

The horizon area is:
```
A = 4Π(r₊² + a²) = 8ΠMr₊
```

**Π's role**: Π defines the geometric area. Without Π, the area formula would be just `4(r₊² + a²)` — which is wrong by a factor of Π.

**Critical threshold**: When a = M (extreme Kerr), r₊ = M, 
**Real-world impact**: Black hole entropy S = A/(4Għ) ∝ Π. The Bekenstein-Hawking entropy formula has Π in it.

---

### Dimension 2: Hawking Temperature — Π as Suppression

The Hawking temperature for a Kerr black hole is:
```
T = ħc³(r₊ - r_-) / (4Πk_B G M (r₊² + a²))
```
where r_- = M - √(M² - a²) (inner horizon).

For Schwarzschild (a = 0):
```
T = ħc³ / (8ΠGMk_B)
```

**Π's role**: Π is in the **denominator**. Larger Π → lower temperature → slower evaporation.

**Critical threshold**: T ∝ 1/(M·Π). Small black holes (M ~ 10¹² kg) have T ~ 10⁸ K (very hot!), large black holes (M ~ M☉) have T ~ 10⁻⁸ K (very cold).

**Real-world impact**: Primordial black holes (M ~ 10¹² kg) evaporate in 13.8 billion years. Π determines their lifetime.

---

### Dimension 3: Quasi-Normal Modes — Π as Oscillation Period

After a black hole merger, the final black hole "rings down" — it oscillates and settles to a stationary state. These are **quasi-normal modes (QNMs)**.

The QNM frequencies are complex:
```
ω = ω_R + iω_I
```
where ω_R is the oscillation frequency, and ω_I is the damping rate.

In geometric units (G = c = 1):
```
ω_R ∝ Π/M,   τ = 2Π/ω_I ∝ M/Π
```

**Π's role**: Π defines the oscillation period (T = 2Π/ω_R) and damping time (τ = 2Π/|ω_I|).

**Critical threshold**: The fundamental mode (n=0, l=m=2) has ω_R ≈ (1.525 - 1.1566i)·(c³/GM) for a* = 0. The real part is ∝ Π/M.

**Real-world impact**: LIGO/Virgo detect QNMs in gravitational wave signals. Π is in the waveform model.

---

### Dimension 4: Spin Precession — Π as Phase Cycle

A gyroscope near a rotating black hole precesses due to **frame dragging** (Lense-Thirring effect).

The precession frequency is:
```
Ω_LT = 2GJ/(c²r³)  (for a gyroscope at distance r)
```

The precession phase accumulates as:
```
ϕ(t) = Ω_LT · t
```

When ϕ = 2Π, the gyroscope has completed **one full precession cycle**.

**Π's role**: Π defines the phase for one full cycle. ϕ = Π corresponds to 180° precession.

**Critical threshold**: Gravity Probe B measured frame dragging with ϕ ~ 10⁻² arcsec/yr. Π converts this to a phase accumulation rate.

**Real-world impact**: Gyroscope experiments test general relativity. Π is in the phase accumulation formula.

---

## Philosophy

**Inward**: Computing Π to 100 trillion digits — measuring Π itself.  
**Outward**: Using Π as a *structural constraint* on black hole spin physics — letting Π reveal order in the universe.

> U(1) symmetry = useful information.  
> Π is the tick mark on that axis.

---

## Connection to `pi-as-u1-period`

This project is a **direct mapping** of the `pi-as-u1-period` framework to black hole spin physics:

| `pi-as-u1-period` | `blackhole-spin-pi` |
|---------------------|---------------------|
| Flux quantization (Φ = Φ₀·n) | Horizon area (A = 4Πr₊²) |
| Chern topology (C = (1/2Π)∫F d²k) | Hawking temperature (T ∝ 1/Π) |
| Kuramoto synchronization (Π/2 boundary) | QNMs (ω_R = 2Πf) |
| Antenna grating (d = Λ/2 = Π/k) | Spin precession (ϕ = 2Π) |

The mathematical skeleton is the same: **Π as U(1) period**.

---

## Verification Status

| Black Hole | M (M☉) | a* | D (kpc) | Verified? | Source |
|------------|---------|-----|-----------|----------|--------|
| **M87*** | 6.5×10⁹ | 0.9 | 16.8 Mpc | ✅ | EHT 2019 |
| **Sgr A*** | 4.3×10⁶ | 0.5 | 8.2 kpc | ✅ | EHT 2022 |
| **GW150914** | 62.0 | 0.67 | ~400 Mpc | ✅ | LIGO 2015 |
| **Cyg X-1** | 14.8 | 0.95 | 1.86 kpc | ✅ | Miller-Jones 2021 |
| **Remaining 55** | ? | ? | ? | ❌ | Need `query_blackcat.py` |

**Note**: Verification for the remaining 55 black holes is blocked by data availability. See [Commentary](#commentary吐槽时间) for details.

---

## Limitations

1. **Not a professional astronomy project** — The main goal is inspiration and outreach, not new discoveries.
2. **Incomplete verification** — Only 4/59 black holes have complete parameters for verification.
3. **Simplified physics** — The code uses approximate formulas (e.g., Kerr horizon area ignores higher-order corrections).
4. **No real data pipeline** — The project does not include a full data reduction pipeline for 2MASS/WISE images.

---

*Generated by math-science workspace, 2026-05-23*  
*Inspired by `pi-as-u1-period` (May 2026)*  
*Dedicated to everyone who ever struggled with astronomical data acquisition*
