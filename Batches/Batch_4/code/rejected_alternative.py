
import sys


def sort_and_sweep(points):
    pts = sorted(set(points))            
    out, best = [], float("inf")
    for p in pts:
        if p[1] < best:                  
            out.append(p)
            best = p[1]
    return out


def sort_and_sweep_3d_naive(points):
  
    pts = sorted(set(points), key=lambda p: (p[0], p[1], -p[2]))
    out, best = [], float("inf")
    for p in pts:
        if p[1] < best:
            out.append(p)
            best = p[1]
    return sorted(out)


if __name__ == "__main__":
    if "--input" in sys.argv:
        from main_solution import read_csv
        pts = [p[:2] for p in read_csv(sys.argv[sys.argv.index("--input") + 1])]
        s = sort_and_sweep(pts)
        print("n=%d  skyline size=%d" % (len(pts), len(s)))
    else:
        from main_solution import INSTANCE, brute_force_3d
        print(sorted(sort_and_sweep(list(INSTANCE.values()))))
        
        A, B = (1000, 3.0, 4.5), (2000, 5.0, 4.9)
        print("3-D naive sweep keeps :", sort_and_sweep_3d_naive([A, B]))
        print("true 3-D skyline      :", brute_force_3d([A, B]))
