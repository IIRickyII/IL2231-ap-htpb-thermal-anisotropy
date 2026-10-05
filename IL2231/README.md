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
   python week1_analytical_baselines.py
   ```
2. **Mathematical Output:**
   * **Series Limit:** $0.2436 \text{ W/(m}\cdot\text{K)}$ (Heat flow perpendicular to material layers).
   * **Parallel Limit:** $0.3085 \text{ W/(m}\cdot\text{K)}$ (Heat flow parallel to material layers).
   * *Validation Standard:* All subsequent COMSOL RVE heat-transfer outputs must match these bounds to a tolerance of $1\times 10^{-4}$.

### Step 2: Homogeneous Isotropic Benchmark (`homogeneous_benchmark.mph`)
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

### Step 3: Two-Layer Composite Limits (`twolayer_benchmark.mph`)
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

**4. Parallel Limit Validation (`twolayer_parallel_benchmark.mph`)**
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

## Upcoming Workflow (Week 2-4)
* **Week 2:** Implementation of the Hermans orientation factor ($S$). Mapping of $S$ (0 to 1.0) to an effective anisotropic conductivity tensor for the CNT/HTPB binder.
* **Week 3:** Generation of 2D non-overlapping heterogeneous AP particle RVEs across 60%, 70%, and 80% volume fractions. Introduction of Kapitza interfacial thermal resistance parameters.
* **Week 4:** Extraction of parallel ($k_{||}$) and perpendicular ($k_{\perp}$) effective thermal conductivities. Calculation of the anisotropy-retention factor ($R_A$).