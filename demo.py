"""Demo for membrane-muscle v0.1.0. Run: python demo.py"""

import random

from muscle import MembraneMuscle, noisy, rand_field


def main():
    mm = MembraneMuscle()
    geo = mm.geometry
    print(f"membrane-muscle v0.1.0 — {geo.n} muscle groups, "
          f"{len(geo.edges)} edges")

    rng = random.Random(11)
    in_probes = [noisy(mm.patterns[k % 4], 0.15, rng)
                 for k in range(100)]
    ood_probes = [rand_field(24, rng) for _ in range(100)]
    tau, j = mm.calibrate(in_probes, ood_probes)
    print(f"gate calibrated: tau = {tau:.3f}, Youden J = {j:.3f} (frozen)")

    rng2 = random.Random(99)
    ok = sum(
        1 for k in range(40)
        if mm.decide(noisy(mm.patterns[k % 4], 0.15,
                           rng2))[1] == mm.MOVEMENT_NAMES[k % 4])
    print(f"fresh noisy recognition (sigma=0.15): {ok}/40")
    rej = sum(
        1 for _ in range(50)
        if mm.decide(rand_field(24, rng2))[0] == "reject")
    print(f"fresh random fields refused: {rej}/50")
    clean = mm.decide(mm.patterns[2])
    print(f"clean squat probe -> {clean[0]}: {clean[1]}")


if __name__ == "__main__":
    main()
