# From CNT Orientation to Macroscopic Thermal Anisotropy in AP/HTPB Composite Propellants: A Multiscale Numerical Study

## Project Objective
This repository contains a two-scale numerical framework designed to determine if directional thermal transport introduced by aligned Carbon Nanotubes (CNTs) at the binder scale survives when embedded within a heterogeneous Ammonium Perchlorate (AP) and Hydroxyl-Terminated Polybutadiene (HTPB) composite. 

The primary contribution is the calculation of an **anisotropy-retention factor** ($R_A$). This metric quantifies the fraction of excess anisotropy retained upon moving from the isolated CNT/HTPB binder to the complete AP/HTPB composite scale. The study independently evaluates attenuation mechanisms, specifically AP particle phase interruptions and CNT-HTPB interfacial thermal resistance.

---

## Phase 1: Benchmark Verification (Week 1)
Before generating heterogeneous representative volume elements (RVEs), we established ground-truth validation models. Week 1 isolates the steady-state heat conduction solver, verifying element discretization, material boundary logic, and normal conductive heat flux extraction against absolute analytical limits.

### Material Property Baselines
| Material | Thermal Conductivity ($k$) | Density ($\rho$) | Heat Capacity ($C_p$) | Domain Assignment |
| :--- | :--- | :--- | :--- | :--- |
| **HTPB** | $0.167 \text{ W/(m}\cdot\text{K)}$ | $1190 \text{ kg/m}^3$ | $2100 \text{ J/(kg}\cdot\text{K)}$ | Binder matrix |
| **AP** | $0.450 \text{ W/(m}\cdot\text{K)}$ | $1950 \text{ kg/m}^3$ | $1500 \text{ J/(kg}\cdot\text{K)}$ | Particulate inclusions |

---

## Reproducibility Protocol & Step-by-Step Methodology

### Step 1: Analytical Ground Truth Generation
Before executing numerical simulations, calculate the exact theoretical effective thermal conductivities for a two-layer composite. 

1. Execute the Python baseline script:
   ```bash
   python week1/week1_analytical_baselines.py
   ```
2. **Mathematical Output:**
   * **Series Limit:** $0.2436 \text{ W/(m}\cdot\text{K)}$ (Heat flow perpendicular to material layers).
   * **Parallel Limit:** $0.3085 \text{ W/(m}\cdot\text{K)}$ (Heat flow parallel to material layers).
   * *Validation Standard:* All subsequent COMSOL RVE heat-transfer outputs must match these bounds to a tolerance of $1\times 10^{-4}$.

### Step 2: Homogeneous Isotropic Benchmark (`week1/homogeneous_benchmark.mph`)
This model proves the base $\Delta T$ boundary application evaluates correctly across a uniform domain.

**1. Base Architecture**
* Open **Model Wizard** > **2D**.
* Add **Heat Transfer in Solids (ht)**. Add **Stationary** study. 

**2. Geometry & Material**
* Build a 1x1 mm **Square**. 
* Add a **Blank Material** (Component level, not Global). Assign to Domain 1.
* Set Isotropic Thermal Conductivity to `0.167 W/(m·K)`. Input generic density (`1190`) and heat capacity (`2100`) to satisfy compiler constraints.

**3. Boundary Conditions**
* Add **Temperature** node to Boundary 1 (Left edge). Set to `310 K`.
* Add **Temperature** node to Boundary 4 (Right edge). Set to `290 K`.
* *Note: Top and Bottom boundaries default to Thermal Insulation.*

**4. Execution & Data Extraction**
* Build standard physics-controlled mesh. Compute Study 1.
* Add **Line Integration** under Results > Derived Values. Select the 290 K boundary.
* Evaluate expression `ht.ndflux` (normal conductive heat flux, $Q$).
* **Calculation:** The table outputs $Q = 3.3400 \text{ W/m}$. 
* $$k_{eff} = \frac{Q \cdot L}{A \cdot \Delta T}$$
* Given $L = 0.001\text{ m}$, $A = 0.001\text{ m}$, and $\Delta T = 20\text{ K}$, divide $Q$ by 20. 
* **Finding:** $k_{eff} = 0.167 \text{ W/(m}\cdot\text{K)}$. The solver perfectly reconstructs the inputted isotropic material property.

### Step 3: Two-Layer Composite Limits (`week1/twolayer_benchmark.mph`)
This model slices the geometry into two discrete material phases to verify interface heat transfer computation.

**1. Geometry Slicing**
* Delete the 1x1 mm square. 
* Build Rectangle 1 (HTPB): Width `0.5 mm`, Height `1 mm`, Position `x=0`.
* Build Rectangle 2 (AP): Width `0.5 mm`, Height `1 mm`, Position `x=0.5 mm`.

**2. Phased Material Assignment**
* Material 1 (HTPB, $k=0.167$): Assign exclusively to Domain 1 (Left).
* Material 2 (AP, $k=0.450$): Assign exclusively to Domain 2 (Right).

**3. Series Limit Validation (Heat Flow Perpendicular to Interface)**
* Apply `310 K` to the far-left boundary. Apply `290 K` to the far-right boundary. Top/bottom remain insulated.
* Compute study. Extract `ht.ndflux` via Line Integration on the 290 K boundary.
* **Calculation:** The table outputs $Q = 4.8720 \text{ W/m}$. Dividing by 20 yields $k_{eff} = 0.2436 \text{ W/(m}\cdot\text{K)}$. 
* **Finding:** Numerical output perfectly matches the theoretical series limit.

**4. Parallel Limit Validation (`week1/twolayer_parallel_benchmark.mph`)**
* Shift boundaries 90 degrees: Apply `310 K` to the top edges of both domains. Apply `290 K` to the bottom edges. Left/right boundaries remain insulated.
* Compute study. Extract `ht.ndflux` via Line Integration on the bottom boundaries.
* **Calculation:** The table outputs $Q = 6.1700 \text{ W/m}$. Dividing by 20 yields $k_{eff} = 0.3085 \text{ W/(m}\cdot\text{K)}$.
* **Finding:** Numerical output perfectly matches the theoretical parallel limit.

## Week 1 Findings Summary
| Configuration | Analytical Target | COMSOL Output | Error Margin | Validation Status |
| :--- | :--- | :--- | :--- | :--- |
| **Isotropic (HTPB)** | $0.1670 \text{ W/(m}\cdot\text{K)}$ | $0.1670 \text{ W/(m}\cdot\text{K)}$ | $0.00\%$ | PASSED |
| **Two-Layer Series** | $0.2436 \text{ W/(m}\cdot\text{K)}$ | $0.2436 \text{ W/(m}\cdot\text{K)}$ | $0.00\%$ | PASSED |
| **Two-Layer Parallel** | $0.3085 \text{ W/(m}\cdot\text{K)}$ | $0.3085 \text{ W/(m}\cdot\text{K)}$ | $0.00\%$ | PASSED |

---

## Phase 2: Multiscale Tensor Injection (Week 2)
Week 2 bridges the nanoscale CNT parameters to the macroscale composite by applying **Nan's Effective Medium Theory (EMT)** coupled with the **Hermans Orientation Factor ($S$)**. The isotropic HTPB binder was converted into a dynamic, anisotropic $2 \times 2$ diagonal tensor.

### CNT Parameters & Kapitza Resistance
We introduced specific nanoscale variables into the COMSOL Global Parameters to calculate the intrinsic interfacial dampening caused by the Kapitza thermal resistance ($R_k$):
* **$V_f$ (CNT Volume Fraction):** $0.05$ (5%)
* **$k_c$ (Intrinsic CNT Conductivity):** $3000 \text{ W/(m}\cdot\text{K)}$
* **$d_{cnt}$ / $L_{cnt}$ (CNT Dimensions):** $10 \text{ nm}$ / $10 \ \mu\text{m}$
* **$R_k$ (Kapitza Resistance):** $1 \times 10^{-8} \text{ m}^2\cdot\text{K/W}$

These parameters allow the derivation of the fully aligned theoretical limits for the CNT/HTPB matrix:
* **$k_{para}$ (Ideal Longitudinal Limit):** $21.587 \text{ W/(m}\cdot\text{K)}$
* **$k_{perp}$ (Ideal Transverse Limit):** $0.175 \text{ W/(m}\cdot\text{K)}$

### The Hermans Tensor Mapping
To orient the conductivity dynamically in COMSOL, the HTPB material was assigned a **Diagonal** tensor. The spatial conductivities $k_{xx}$ and $k_{yy}$ are defined by the Hermans Orientation Factor ($S$), which spans from $-0.5$ (perpendicular alignment) to $1.0$ (perfect parallel alignment):

$$k_{yy}(S) = k_{perp} + (k_{para} - k_{perp}) \frac{2S + 1}{3}$$

$$k_{xx}(S) = k_{perp} + (k_{para} - k_{perp}) \frac{1 - S}{3}$$

### Week 2 Validations
We tested the tensor logic on the 50/50 AP/HTPB parallel boundary configuration. Both extremes were analytically calculated and numerically validated.

**1. Perfect Alignment ($S = 1.0$) -> `twolayer_parallel_benchmark.mph`**
* **Physical state:** CNTs are perfectly bridging the top-to-bottom thermal gradient within the binder phase.
* **Analytical $k_{eff}$:** $11.018 \text{ W/(m}\cdot\text{K)}$
* **COMSOL Heat Flux ($Q$):** $220.37 \text{ W/m}$ (Exactly matches theoretical limit).

**2. Random Orientation ($S = 0.0$) -> `twolayer_parallel_random.mph`**
* **Physical state:** CNTs are randomly distributed in 3D space. The tensor collapses into an isotropic state.
* **Analytical $k_{eff}$:** $3.881 \text{ W/(m}\cdot\text{K)}$
* **COMSOL Heat Flux ($Q$):** $77.628 \text{ W/m}$ (Exactly matches theoretical limit).

---

## Reproducibility Protocol

### COMSOL Execution & Verification
To verify the numerical outputs of any `.mph` file in this repository:
1. Open the file in **COMSOL Multiphysics**.
2. Navigate to **Model Builder** > **Study 1**. Click **Compute**.
3. Navigate to **Results** > **Derived Values** > **Line Integration 1**.
4. Click **Evaluate**.
5. The `Table` tab will output the **normal conductive heat flux** ($Q$) in $\text{W/m}$.
6. Calculate the effective thermal conductivity:

   $$k_{eff} = \frac{Q \cdot L}{A \cdot \Delta T}$$

   **Note:** For all current benchmarks, $L = 0.001\text{ m}$, $A = 0.001\text{ m}$, and $\Delta T = 20\text{ K}$. Divide the total heat flux by 20.

To test different CNT orientations, navigate to **Global Definitions** > **Parameters 1**, alter the value of `S_factor`, and recompute the study.

---

## Phase 3: Heterogeneous Microstructure Generation (Week 3)
To transition from simple geometric layers to accurate composite microstructures, we generated 2D non-overlapping Representative Volume Elements (RVEs) of the AP/HTPB mixture across 60%, 70%, and 80% volume fractions.

### The Unified Geometry Engine (`rve_generator.py`)
To prevent thermodynamic jamming at high volume fractions, we implemented a stabilized Random Sequential Adsorption (RSA) algorithm. The Python script dynamically shifts from a bimodal to a trimodal particle distribution and tightens mesh collision tolerances to $0.2 \ \mu\text{m}$.

* **60% & 70% $V_f$:** Bimodal distribution ($40 \ \mu\text{m}$ and $8-10 \ \mu\text{m}$ radii).
* **80% $V_f$:** Trimodal distribution ($40 \ \mu\text{m}$, $10 \ \mu\text{m}$, and $3 \ \mu\text{m}$ radii) targeting up to 1.5 million brute-force collision iterations to shatter the topological jamming limit.

### COMSOL Implementation
The exported DXF coordinates are imported into COMSOL with **Form solids** activated to map native 2D boundaries. 
* **Matrix Phase:** Continuous HTPB is assigned the anisotropic diagonal tensor (evaluated at the $S = 1.0$ limit).
* **Inclusion Phase:** Dispersed AP particles are assigned isotropic properties ($0.45 \text{ W/(m}\cdot\text{K)}$).
* **Interfacial Boundaries:** To physically replicate the macroscale Kapitza thermal contact resistance ($R_s = 1 \times 10^{-4} \text{ m}^2\cdot\text{K/W}$), all internal AP-HTPB boundaries are selected and modeled as a **Nonlayered shell** using the Thin Layer node.

### Week 3 Macro-Scale Convergence Data
Data is extracted via normal conductive heat flux ($Q$) along the $290\text{ K}$ boundary ($\Delta T = 20\text{ K}$).

| Volume Fraction ($V_f$) | Algorithm | Heat Flux ($Q$) | Effective Conductivity ($k_{eff}$) |
| :--- | :--- | :--- | :--- |
| **0.60** | Bimodal | $31.587 \text{ W/m}$ | $1.579 \text{ W/(m}\cdot\text{K)}$ |
| **0.70** | Bimodal | $23.330 \text{ W/m}$ | $1.166 \text{ W/(m}\cdot\text{K)}$ |
| **0.80** | Trimodal | $18.557 \text{ W/m}$ | $0.928 \text{ W/(m}\cdot\text{K)}$ |

**Physics Validation:** The thermal degradation scales perfectly with the microstructural geometry. At 80% volume fraction, the thousands of $3 \ \mu\text{m}$ inclusions exponentially inflate the internal interface surface area. Kapitza resistance entirely dominates the phonon transport networks, stripping the macroscopic conductivity below $1.0\text{ W/(m}\cdot\text{K)}$ despite the perfectly aligned CNT-reinforced binder.

---

## Reproducibility Protocol

### 1. Generating RVE Geometries
Execute the Python solver to generate the bimodal and trimodal DXF CAD coordinates:
```bash
python week3/rve_generator.py
```

### 2. Analytical Ground Truth Calculation (Week 1/2)
Execute the Python baseline script to calculate the theoretical effective thermal conductivities for the simple two-layer composite limits. 
```bash
python week1/week1_analytical_baselines.py
```

### 3. COMSOL Execution & Verification
To verify the numerical outputs of any `.mph` file in this repository:

1. Open the file in **COMSOL Multiphysics**.
2. Navigate to **Model Builder** > **Study 1**. Click **Compute**.
3. Navigate to **Results** > **Derived Values** > **Line Integration 1**.
4. Click **Evaluate**.
5. The `Table` tab will output the **normal conductive heat flux** ($Q$) in $\text{W/m}$.
6. Calculate the effective thermal conductivity:

**Note:** For all current benchmarks, $L = 0.001\text{ m}$, $A = 0.001\text{ m}$, and $\Delta T = 20\text{ K}$. Divide the total heat flux by 20.

$$k_{eff} = \frac{Q \cdot L}{A \cdot \Delta T}$$

To test different CNT orientations, navigate to **Global Definitions** > **Parameters 1**, alter the value of `S_factor`, and recompute the study.

---

## Upcoming Workflow (Week 4)
* **Week 4:** Extraction of perpendicular ($k_{\perp}$) effective thermal conductivities on the full RVEs by rotating the thermal gradient or tensor parameters. Calculation of the anisotropy-retention factor ($R_A$) to conclude the multiscale study.