"""Tests for membrane-muscle v0.1.0. Run: python tests.py"""

import math
import random
import unittest

from muscle import (
    MembraneMuscle,
    MuscleGeometry,
    noisy,
    rand_field,
)


class TestMembraneMuscle(unittest.TestCase):
    def test_geometry_connected_no_isolated(self):
        geo = MuscleGeometry()
        self.assertEqual(geo.n, 24)
        for m in geo.muscles:
            self.assertGreaterEqual(len(geo.neighbours(m.id)), 1)
        delays = geo.delays_from(geo.by_name["pectoralis-left"])
        self.assertTrue(all(math.isfinite(d) for d in delays))

    def test_patterns_unit_and_distinct(self):
        mm = MembraneMuscle()
        self.assertEqual(len(mm.patterns), 4)
        for p in mm.patterns:
            self.assertAlmostEqual(
                math.sqrt(sum(abs(c) ** 2 for c in p)), 1.0, places=9)
        for i in range(4):
            for j in range(i + 1, 4):
                ov = abs(sum(a.conjugate() * b for a, b
                             in zip(mm.patterns[i],
                                    mm.patterns[j])))
                self.assertLess(ov, 0.95)

    def test_clean_movement_recognition(self):
        mm = MembraneMuscle()
        mm.tau = None
        for i, p in enumerate(mm.patterns):
            verdict, name, _ = mm.decide(p)
            self.assertEqual(verdict, "accept")
            self.assertEqual(name, mm.MOVEMENT_NAMES[i])

    def test_noisy_recognition(self):
        mm = MembraneMuscle()
        mm.tau = None
        rng = random.Random(7)
        ok, trials = 0, 40
        for k in range(trials):
            probe = noisy(mm.patterns[k % 4], 0.15, rng)
            _, name, _ = mm.decide(probe)
            ok += name == mm.MOVEMENT_NAMES[k % 4]
        self.assertGreaterEqual(ok / trials, 0.90)

    def test_gate_refuses_random(self):
        mm = MembraneMuscle()
        rng = random.Random(11)
        in_probes = [noisy(mm.patterns[k % 4], 0.15, rng)
                     for k in range(100)]
        ood_probes = [rand_field(24, rng) for _ in range(100)]
        tau, j = mm.calibrate(in_probes, ood_probes)
        self.assertGreater(j, 0.90)
        self.assertGreater(tau, 0.2)
        self.assertLess(tau, 0.95)
        rng2 = random.Random(99)
        accepted = sum(
            1 for k in range(50)
            if mm.decide(noisy(mm.patterns[k % 4], 0.15,
                               rng2))[0] == "accept")
        rejected = sum(
            1 for _ in range(50)
            if mm.decide(rand_field(24, rng2))[0] == "reject")
        self.assertGreaterEqual(accepted / 50, 0.90)
        self.assertGreaterEqual(rejected / 50, 0.90)

    def test_determinism(self):
        a = MembraneMuscle()
        b = MembraneMuscle()
        self.assertEqual(a.patterns, b.patterns)
        self.assertEqual(a.geometry.edges, b.geometry.edges)


if __name__ == "__main__":
    unittest.main(verbosity=2)
