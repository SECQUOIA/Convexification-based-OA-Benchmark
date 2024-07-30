
python3 ../src/paver/paver.py \
  ./MindtPy-convexification-gurobi11/trace_file/convex/*/mindtpy-OA-single*/*.trc \
  ../solu/minlplib_new.solu \
  --failtime 900 \
  --mintime 0.1 \
  --ccopttol inf \
  --ccreltol 1e03 \
  --ccabstol 1e-7 \
  --gaptol  0.001 \
  --writehtml MindtPy-convexification-gurobi11/paver_results/convex/singletree \
  --extendedprofiles \
  --nocheckinstanceattr \
  --extendedprofiles


python3 ../src/paver/paver.py \
  ./MindtPy-convexification-gurobi11/trace_file/convex/*/mindtpy-OA-2024*/*.trc \
  ../solu/minlplib_new.solu \
  --failtime 900 \
  --mintime 0.1 \
  --ccopttol inf \
  --ccreltol 1e03 \
  --ccabstol 1e-7 \
  --gaptol  0.001 \
  --writehtml MindtPy-convexification-gurobi11/paver_results/convex/multitree \
  --extendedprofiles \
  --nocheckinstanceattr \
  --extendedprofiles

python3 ../src/paver/paver.py \
  ./MindtPy-convexification-gurobi11/trace_file/nonconvex/*/mindtpy-GOA-single*/*.trc \
  ../solu/minlplib_new.solu \
  --failtime 900 \
  --mintime 0.1 \
  --ccopttol inf \
  --ccreltol 1e03 \
  --ccabstol 1e-7 \
  --gaptol  0.001 \
  --writehtml MindtPy-convexification-gurobi11/paver_results/nonconvex/singletree \
  --extendedprofiles \
  --nocheckinstanceattr \
  --extendedprofiles

  # --numpts 10000 \

python3 ../src/paver/paver.py \
  ./MindtPy-convexification-gurobi11/trace_file/nonconvex/*/mindtpy-GOA-2024*/*.trc \
  ../solu/minlplib_new.solu \
  --failtime 900 \
  --mintime 0.1 \
  --ccopttol inf \
  --ccreltol 1e03 \
  --ccabstol 1e-7 \
  --gaptol  0.001 \
  --writehtml MindtPy-convexification-gurobi11/paver_results/nonconvex/multitree \
  --extendedprofiles \
  --nocheckinstanceattr \
  --extendedprofiles
