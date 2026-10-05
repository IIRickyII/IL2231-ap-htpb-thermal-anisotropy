def series_conductivity(L1, k1, L2, k2):
    L_total = L1 + L2
    return L_total / ((L1 / k1) + (L2 / k2))

def parallel_conductivity(A1, k1, A2, k2):
    A_total = A1 + A2
    return (k1 * A1 + k2 * A2) / A_total

k_HTPB = 0.167
k_AP = 0.450

k_series = series_conductivity(0.5, k_HTPB, 0.5, k_AP)
k_parallel = parallel_conductivity(0.5, k_HTPB, 0.5, k_AP)

print(f"TARGET SERIES: {k_series:.4f}")
print(f"TARGET PARALLEL: {k_parallel:.4f}")
