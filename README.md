# A Convexification-based Outer-Approximation Method for Convex and Nonconvex MINLP

This repository contains the benchmark results of the paper **"A Convexification-based Outer-Approximation Method for Convex and Nonconvex MINLP"** by Z. Peng, K. Cao, K.C. Furman, C. Li, I.E. Grossmann, and D.E. Bernal. You can view the detailed results on the [web page](https://secquoia.github.io/Convexification-based-OA-Benchmark/).

The implementation of the proposed methods is based on **MindtPy**, the Mixed-Integer Nonlinear Decomposition Toolbox in Pyomo. For more information about MindtPy, please refer to the [Pyomo MindtPy documentation](https://pyomo.readthedocs.io/en/stable/contributed_packages/mindtpy.html).

The benchmark results for each instance are stored as trace files. For more information about trace files, please refer to the [GAMS trace file documentation](https://www.gams.com/latest/docs/UG_SolverUsage.html#UG_SolverUsage_TraceFile).

The software [Paver 2](https://github.com/coin-or/Paver) is used to process the trace files and analyze the performance of the proposed methods in this work.

## MINLP Instances

All the MINLP instances benchmarked here are from [MINLPLib](http://minlplib.org), including

1. 435 [convex MINLP instances](https://github.com/SECQUOIA/Convexification-based-OA-Benchmark/minlp_instances/convex_instances.txt)
2. 182 [nonconvex MINLP instances](https://github.com/SECQUOIA/Convexification-based-OA-Benchmark/minlp_instances/nonconvex_instances.txt)

## Project Structure

```plaintext
.
├── LICENSE
├── README.md           # Project overview and structure
├── _config.yml         # Configuration file for GitHub Pages
├── index.md            # Main page of the website
├── minlp_instances     # Folder containing the list of convex and nonconvex MINLP instances
├── paver_results       # Folder containing Paver results
└── trace_file          # Folder containing trace files
```
