# membrane-muscle v0.1.0

**A sparkainlp-x membrane on a muscle map — a toy graph, not a body.**

Stdlib-only Python, seeded, reproducible, AGPL-3.0-only.

## Lineage reused

- **membrane-capacity**: complex oscillators, outer-product
  holographic memory, one-shot projection (argmax |overlap|).
- **refusing-membrane**: REJECT iff max |overlap| < tau, tau
  calibrated once via Youden's J and frozen, with the
  midpoint-of-best-taus improvement from membrane-vs-hopfield.
- **membrane-heart / membrane-brain / membrane-skeleton**:
  patterns as ENVELOPED phasor waves over a graph.

## Run

```bash
python demo.py    # numbers + gate + recognition
python tests.py   # 6 tests
```

## The toy, in one paragraph

24 muscle-group nodes in a standing 2D layout, connected by
hand-defined edges between adjacent groups. Four stored
"movements" are wave fields started from four seed groups:
push (pectoralis-left), pull (latissimus-left), squat
(quadriceps-left), curl (biceps-left). A probe is projected onto
them: the membrane names one, or the frozen gate refuses it.

## Measured (demo)

- 24 muscle groups, 30 edges
- Gate calibrated: tau = 0.460, Youden J = 1.000 (frozen)
- Fresh noisy recognition (sigma = 0.15): 40/40
- Fresh random fields refused: 50/50
- Clean squat probe: accept, squat

## Honest limits — read before any use

- **Not a human muscle system.** No forces, fibre types, motor
  units, EMG, or biomechanics.
- **No age.** The holographic muscle images were labelled 25 years
  old; this graph has no age, and nothing here is a measurement
  of any real person.
- **Not a medical device, not a diagnosis.** Movement names are
  labels for wave snapshots, not observed movements.
- "Holographic" here = outer-product associative memory, the
  membrane meaning — not a laser hologram and not a display.

## Files

- `muscle.py` — muscle graph, wave, membrane, gate
- `demo.py` — measured demo
- `tests.py` — 6 tests
- `DESIGN.md` — decisions, falsified designs, limits
- `LICENSE` — AGPL-3.0-only

## Credits

Authors: Jean-François Brisson and Mun Seok Lee.
Lee, author of the Digital to Wave paradigm (Zenodo 21947036,
21947108), is the inspiration friend behind this wave and
membrane work. This package's code was built by Brisson with
AI assistance, except where a file already credits Lee as
author; the joint credit here is for the shared programme,
not a claim that Lee wrote every line of this package.
