"""membrane-muscle v0.1.0 — a sparkainlp-x membrane on a muscle map.

Stdlib-only Python, seeded, reproducible, AGPL-3.0-only.

Lineage, reused exactly
-----------------------
1. membrane-capacity: complex oscillators; patterns stored as an
   outer-product holographic memory; recognition is one-shot
   projection — winner = argmax |overlap|, probs = |m|^2 / sum |m|^2.
2. refusing-membrane: REJECT iff max |overlap| < tau, tau calibrated
   once and frozen — with the midpoint-of-max-J improvement from
   membrane-vs-hopfield.
3. membrane-heart / membrane-brain / membrane-skeleton: a pattern is
   an ENVELOPED phasor wave over a graph, not a pure phase wave.
   Pure phase snapshots differ only by a global phase, which
   |overlap| cannot see (membrane-heart first run: 0.325). The
   envelope — amplitude decays with Dijkstra distance from the
   seed, phase advances with distance — is kept here from the start.

The toy muscle map
------------------
24 muscle-group nodes in a standing 2D layout, connected by
hand-defined edges between adjacent groups. Four stored
"movements" are wave fields started from four seed groups:
push (from pectoralis-left), pull (from latissimus-left),
squat (from quadriceps-left), curl (from biceps-left).
A probe is projected onto them: the membrane names one, or the
frozen gate refuses it. A random field is refused instead of
mislabelled.

What this is NOT — read before any use
---------------------------------------
Not a human muscle system in any clinical sense. No forces,
fibre types, motor units, EMG, or biomechanics. Not a medical
device, not a diagnosis, not a measurement of any real person.
The "25-year-old" label from the holographic muscle images is NOT
carried into this code: a muscle-group graph has no age.
"Holographic" here = outer-product associative memory, the
membrane meaning — not a laser hologram and not a display.
"""

import heapq
import math
import random

__version__ = "0.1.0"


def normalize(v):
    n = math.sqrt(sum(abs(c) ** 2 for c in v))
    if n == 0:
        raise ValueError("cannot normalize a zero vector")
    return [c / n for c in v]


def overlap(field, pattern):
    return sum(p.conjugate() * f for p, f in zip(pattern, field))


def noisy(field, sigma, rng):
    return normalize(
        [c + complex(rng.gauss(0, sigma), rng.gauss(0, sigma))
         for c in field]
    )


def rand_field(n, rng):
    return normalize(
        [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
    )


NODE_DEFS = [
    ("trapezius", 0, 78),
    ("deltoid-left", -13, 70),
    ("deltoid-right", 13, 70),
    ("pectoralis-left", -6, 66),
    ("pectoralis-right", 6, 66),
    ("latissimus-left", -11, 58),
    ("latissimus-right", 11, 58),
    ("biceps-left", -16, 56),
    ("biceps-right", 16, 56),
    ("triceps-left", -17, 48),
    ("triceps-right", 17, 48),
    ("forearm-left", -17, 36),
    ("forearm-right", 17, 36),
    ("abdominals", 0, 52),
    ("oblique-left", -7, 52),
    ("oblique-right", 7, 52),
    ("gluteus-left", -6, 36),
    ("gluteus-right", 6, 36),
    ("quadriceps-left", -6, 26),
    ("quadriceps-right", 6, 26),
    ("hamstring-left", -7, 20),
    ("hamstring-right", 7, 20),
    ("calf-left", -6, 10),
    ("calf-right", 6, 10),
]

EDGE_DEFS = [
    (0, 1), (0, 2), (0, 3), (0, 4),
    (1, 7), (2, 8), (1, 9), (2, 10),
    (7, 11), (8, 12), (9, 11), (10, 12),
    (3, 5), (4, 6), (3, 13), (4, 13),
    (5, 14), (6, 15), (13, 14), (13, 15),
    (14, 16), (15, 17),
    (16, 18), (17, 19), (16, 20), (17, 21),
    (18, 22), (19, 23), (20, 22), (21, 23),
]


class Muscle:
    def __init__(self, nid, name, x, y):
        self.id = nid
        self.name = name
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return f"Muscle({self.id}, {self.name!r})"


class MuscleGeometry:
    def __init__(self):
        self.muscles = [
            Muscle(i, name, x, y)
            for i, (name, x, y) in enumerate(NODE_DEFS)
        ]
        self.n = len(self.muscles)
        self.edges = sorted(
            (min(a, b), max(a, b)) for a, b in EDGE_DEFS
        )
        self.by_name = {m.name: m.id for m in self.muscles}

    def neighbours(self, nid):
        out = []
        for a, b in self.edges:
            if a == nid:
                out.append(b)
            elif b == nid:
                out.append(a)
        return sorted(out)

    def delays_from(self, source):
        by_id = {m.id: m for m in self.muscles}
        times = {m.id: math.inf for m in self.muscles}
        times[source] = 0.0
        heap = [(0.0, source)]
        while heap:
            t, nid = heapq.heappop(heap)
            if t > times[nid]:
                continue
            a = by_id[nid]
            for mid in self.neighbours(nid):
                b = by_id[mid]
                w = math.hypot(a.x - b.x, a.y - b.y)
                if t + w < times[mid]:
                    times[mid] = t + w
                    heapq.heappush(heap, (times[mid], mid))
        return [times[m.id] for m in self.muscles]


class MembraneMuscle:
    """Muscle membrane: store, project, refuse."""

    MOVEMENT_NAMES = ("push", "pull", "squat", "curl")
    SEED_MUSCLES = ("pectoralis-left", "latissimus-left",
                     "quadriceps-left", "biceps-left")

    def __init__(self, width=25.0, period=40.0):
        if width <= 0 or period <= 0:
            raise ValueError("width and period must be positive")
        self.geometry = MuscleGeometry()
        self.n = self.geometry.n
        self.width = width
        self.period = period
        self.seed_ids = [
            self.geometry.by_name[name] for name in self.SEED_MUSCLES
        ]
        self.patterns = [self.wave(sid) for sid in self.seed_ids]
        self.tau = None

    def wave(self, source):
        delays = self.geometry.delays_from(source)
        out = []
        for d in delays:
            if math.isinf(d):
                out.append(0j)
                continue
            amp = math.exp(-(d * d) / (2.0 * self.width * self.width))
            phase = 2.0 * math.pi * d / self.period
            out.append(amp * complex(math.cos(phase),
                                     math.sin(phase)))
        return normalize(out)

    def overlaps(self, field):
        return [overlap(field, p) for p in self.patterns]

    def project(self, field):
        ms = self.overlaps(field)
        tot = sum(abs(m) ** 2 for m in ms)
        if tot == 0:
            return None, [0.0] * len(ms)
        probs = [abs(m) ** 2 / tot for m in ms]
        return max(range(len(ms)), key=lambda i: abs(ms[i])), probs

    def max_overlap(self, field):
        return max(abs(m) for m in self.overlaps(field))

    def calibrate(self, in_probes, ood_probes, grid=101):
        in_max = [self.max_overlap(f) for f in in_probes]
        ood_max = [self.max_overlap(f) for f in ood_probes]
        best_j, best_taus = -2.0, []
        for step in range(grid + 1):
            tau = step / grid
            tpr = sum(1 for v in in_max if v >= tau) / len(in_max)
            fpr = sum(1 for v in ood_max if v >= tau) / len(ood_max)
            j = tpr - fpr
            if j > best_j + 1e-12:
                best_j, best_taus = j, [tau]
            elif abs(j - best_j) <= 1e-12:
                best_taus.append(tau)
        self.tau = (best_taus[0] + best_taus[-1]) / 2.0
        return self.tau, best_j

    def decide(self, field):
        winner, probs = self.project(field)
        if winner is None:
            return "reject", None, probs
        if self.tau is not None and self.max_overlap(field) < self.tau:
            return "reject", None, probs
        return "accept", self.MOVEMENT_NAMES[winner], probs
