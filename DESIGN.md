# DESIGN.md — membrane-muscle v0.1.0

## Decisions

- **Hand-defined muscle graph, not k-NN.** Proximity is not
  adjacency: a calf near a hamstring is a leg chain, a biceps near
  a pectoralis is not a functional link. Hand edges follow the
  layout the toy intends, and connectivity is tested.
- **24 groups, not every muscle.** Hundreds of named muscles exist;
  modelling them would be anatomy theatre. 24 major groups carry
  the four waves, and no more is claimed.
- **Wave movements, not forces.** No torque, no load, no EMG.
  A wave from a seed group is a clean, checkable pattern whose
  recognition and refusal can be measured exactly.
- **Envelope from the start.** membrane-heart's pure-phase failure
  is not repeated: amplitude decays with distance, phase advances
  with distance, pattern normalised.
- **Midpoint tau.** Same improvement as the heart/brain/skeleton
  toys: midpoint of the maximal-J taus.
- **No age in the code.** The images were labelled 25; a graph
  cannot have an age, so the code drops it rather than pretending.

## Falsified / rejected designs

- **EMG-like output.** Rejected: synthesising a clinical-looking
  trace from a toy would be misleading.
- **Strength or fitness scores.** Rejected: overlaps are not
  strength, and no summary fitness number is invented from them.
- **Full anatomical muscle list.** Rejected: more nodes, same four
  waves, false impression of completeness.

## Limits, restated

Synthetic only. Flat 2D layout, width 25, period 40, delays in
layout distance units — none of these are biological parameters.
The refusal rate is a property of this toy's random fields, not a
sensitivity or specificity for anything real.
