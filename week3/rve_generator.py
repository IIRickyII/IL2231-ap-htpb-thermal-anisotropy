import numpy as np
import ezdxf
import math
import os

def generate_rve(target_vf, filepath, domain=1000):
    if target_vf == 0.80:
        radii = [40.0, 10.0, 3.0]
        volume_splits = [0.55, 0.25, 0.20] 
        max_attempts = [100000, 300000, 1500000] 
    elif target_vf == 0.70:
        radii = [40.0, 8.0]
        volume_splits = [0.60, 0.40]
        max_attempts = [100000, 300000]
    else:
        radii = [40.0, 10.0]
        volume_splits = [0.70, 0.30]
        max_attempts = [25000, 25000]
        
    area_total = domain**2
    area_target = target_vf * area_total
    particles = []
    
    for r, split, attempts_limit in zip(radii, volume_splits, max_attempts):
        area_phase = area_target * split
        n_particles = int(area_phase / (math.pi * r**2))
        
        for _ in range(n_particles):
            placed = False
            attempts = 0
            while not placed and attempts < attempts_limit:
                x = np.random.uniform(r, domain - r)
                y = np.random.uniform(r, domain - r)
                
                # 0.2um tolerance gap prevents CAD/Mesh overlap errors
                overlap = False
                for px, py, pr in particles:
                    if math.hypot(x - px, y - py) < (r + pr + 0.2): 
                        overlap = True
                        break
                
                if not overlap:
                    particles.append((x, y, r))
                    placed = True
                attempts += 1
                
            if not placed:
                print(f"Jamming limit reached at r={r}um. Increase attempts.")
                break

    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # 1x1mm matrix boundary
    msp.add_lwpolyline([(0,0), (domain,0), (domain,domain), (0,domain), (0,0)])
    
    for x, y, r in particles:
        msp.add_circle((x, y), r)
        
    doc.saveas(filepath)
    actual_vf = sum(math.pi * p[2]**2 for p in particles) / area_total
    print(f"Saved {filepath} | Target VF: {target_vf} | Actual VF: {actual_vf:.3f}")

if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Generate all microstructures
    generate_rve(0.60, os.path.join(output_dir, "rve_60.dxf"))
    generate_rve(0.70, os.path.join(output_dir, "rve_70.dxf"))
    generate_rve(0.80, os.path.join(output_dir, "rve_80.dxf"))
