---
layout: default
title: Benchmark Results
---

## Description

The PAVER reports used in the paper: **"A Convexification-based Outer-Approximation Method for Convex and Nonconvex MINLP"** by Z. Peng, K. Cao, K.C. Furman, C. Li, I.E. Grossmann, D.E. Bernal are available here.

## Implementation
The implementation of the Outer-Approximation method is based on [MindtPy](https://pyomo.readthedocs.io/en/stable/contributed_packages/mindtpy.html), the Mixed-Integer Nonlinear Decomposition Toolbox in Pyomo. Furthermore, we integrate two implementations of the bound tightening and the convexification techniques for MINLP problems in MindtPy. 
1. The first implementation is based on a special version of [BARON](https://www.minlp.com/baron-solver) 19.4.4, the state-of-the-art commercial MINLP solver.
2. The second implementation uses [Coramin](https://github.com/Coramin/Coramin) and the FBBT (C++) code in [Pyomo](https://github.com/Pyomo/pyomo), both of which are open-source and offer more flexibility.

## MINLP Instances

All the MINLP instances benchmarked here are from [MINLPLib](http://minlplib.org), including

1. 435 [convex MINLP instances](https://github.com/SECQUOIA/Convexification-based-OA-Benchmark/blob/main/minlp_instances/convex_instances.txt)
2. 182 [nonconvex MINLP instances](https://github.com/SECQUOIA/Convexification-based-OA-Benchmark/blob/main/minlp_instances/nonconvex_instances.txt)

## Paver Reports

1. [C-OA method for convex instances](https://SECQUOIA.github.io/Convexification-based-OA-Benchmark/paver_results/convex/multitree)

2. [C-LP/NLP-based B&B method for convex instances](https://SECQUOIA.github.io/Convexification-based-OA-Benchmark/paver_results/convex/singletree)

3. [C-GOA method for nonconvex instances](https://SECQUOIA.github.io/Convexification-based-OA-Benchmark/paver_results/nonconvex/multitree)

4. [C-GLP/NLP-based B&B method for nonconvex instances](https://SECQUOIA.github.io/Convexification-based-OA-Benchmark/paver_results/nonconvex/singletree)
