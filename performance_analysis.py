import glob
import pandas as pd
import numpy as np
from scipy.stats import gmean
import itertools

pd.set_option('display.max_columns', None)

# performance_index = 'SolverTime'
# performance_index = 'NumberOfIterations'
performance_index = "Number of infeasible nlp subproblems"
threshold = 10

trace_file_column_names = [
    'InputFileName',
    'ModelType',
    'SolverName',
    'NLP',
    'MIP',
    'JulianDate',
    'Direction',
    'NumberOfEquations',
    'NumberOfVariables',
    'NumberOfDiscreteVariables',
    'NumberOfNonZeros',
    'NumberOfNonlinearNonZeros',
    'OptionFile',
    'ModelStatus',
    'SolverStatus',
    'ObjectiveValue',
    'ObjectiveValueEstimate',
    'SolverTime',
    'NumberOfIterations',
    'NumberOfDomainViolations',
    'NumberOfNodes',
    # The following are user defined data in MindtPy
    "Best solution found time",
    "fixed nlp time",
    "mip time",
    "initialization time",
    "OA cut time",
    "Affine cut generation time",
    "Nogood cut generation time",
    "ECP cut generation time",
    "Regularization master time",
    "fp master time",
    "fp master time",
    "PyomoNLP time",
    "Number of infeasible nlp subproblems",
]

MODEL_STATUS_CODE = {
    1: "Optimal",
    2: "Locally Optimal",
    3: "Unbounded",
    4: "Infeasible",
    5: "Locally Infeasible",
    6: "Intermediate Infeasible",
    7: "Intermediate Nonoptimal",
    8: "Integer Solution",
    9: "Intermediate Non-Integer",
    10: "Integer Infeasible",
    11: "Licensing Problems - No Solution",
    12: "Error Unknown",
    13: "Error No Solution",
    14: "No Solution Returned",
    15: "Solved Unique",
    16: "Solved",
    17: "Solved Singular",
    18: "Unbounded - No Solution",
    19: "Infeasible - No Solution",
}

SOLVER_STATUS_CODE = {
    1: "Normal Completion",
    2: "Iteration Interrupt",
    3: "Resource Interrupt",
    4: "Terminated by Solver",
    5: "Evaluation Error Limit",
    6: "Capability Problems",
    7: "Licensing Problems",
    8: "User Interrupt",
    9: "Error Setup Failure",
    10: "Error Solver Failure",
    11: "Error Internal Solver Error",
    12: "Solve Processing Skipped",
    13: "Error System Failure",
}

file_paths = glob.glob('trace_file/*/*/*/*.trc')


OA_method_list = [
    "C-OA-Baron(c)",
    "C-OA-Baron(r)",
    "C-OA-Coramin(r)",
    "C-OA-FBBT-Coramin(r)",
    "OA",
    "OA-FBBT",
]
LPNLP_method_list = [
    "C-LP/NLP-B&B-Baron(c)",
    "C-LP/NLP-B&B-Baron(r)",
    "C-LP/NLP-B&B-Coramin(r)",
    "C-LP/NLP-B&B-FBBT-Coramin(r)",
    "LP/NLP-B&B",
    "LP/NLP-B&B-FBBT",
]

GOA_method_list = [
    "C-GOA-Baron(c)",
    "C-GOA-Baron(r)",
    "C-GOA-Coramin(r)",
    "C-GOA-FBBT-Coramin(r)",
    "GOA",
    "GOA-FBBT",
]

GLPNLP_method_list = [
    "C-GLP/NLP-B&B-Baron(c)",
    "C-GLP/NLP-B&B-Baron(r)",
    "C-GLP/NLP-B&B-Coramin(r)",
    "C-GLP/NLP-B&B-FBBT-Coramin(r)",
    "GLP/NLP-B&B",
    "GLP/NLP-B&B-FBBT",
]

# Read the trace files and extract the data
data = []

for filepath in file_paths:
    with open(filepath, 'r') as file:
        line = file.readline().strip()
        # Split the line into two parts
        parts = line.split('# ')
        first_part = parts[0].split(', ')
        second_part = parts[1].split('. ')
        row = first_part[:-1]

        # Extract key-value pairs from the second part
        for item in second_part:
            if 'at ' in item:
                best_solution_time = item.split('at ', 1)[1].split(' ')[0]
                row.append(best_solution_time)
            if ': ' in item:
                key, value = item.split(': ', 1)
                row.append(value)
        data.append(row)

df = pd.DataFrame(data, columns=trace_file_column_names)
df[performance_index] = df[performance_index].astype(float)
df['SolverTime'] = df['SolverTime'].astype(float)


status_result = (
    df.groupby(['ModelStatus', 'SolverStatus'])
    .agg({'SolverTime': ['mean', 'count']})
    .reset_index()
)
status_result['ModelStatus'] = (
    status_result['ModelStatus'].astype(int).replace(MODEL_STATUS_CODE)
)
status_result['SolverStatus'] = (
    status_result['SolverStatus'].astype(int).replace(SOLVER_STATUS_CODE)
)
print(status_result)

#       ModelStatus          SolverStatus  SolverTime
#                                                mean count
# Error No Solution  Error Solver Failure   91.080747    31
#        Infeasible  Terminated by Solver   11.113592     9
#  Integer Solution  Error Solver Failure  233.766983    22
#  Integer Solution  Terminated by Solver  681.507524    65

# For number of iterations
# 2     Error No Solution  Terminated by Solver  902.623097    43
# 3  No Solution Returned    Resource Interrupt  900.839473   233
# 7      Integer Solution    Resource Interrupt  903.812880   566

failed_status = [['13', '10'], ['4', '4'], ['8', '10'], ['8', '4']]
failed_mask = df.apply(
    lambda row: [row['ModelStatus'], row['SolverStatus']] in failed_status, axis=1
)
failed_instances_names = df[failed_mask]['InputFileName'].to_list()
print('Failed instances:', failed_instances_names)

# Read the convex and nonconvex instance lists
with open('minlp_instances/convex_instances.txt', 'r') as file:
    convex_instance_list = [line.strip() for line in file]
with open('minlp_instances/nonconvex_instances.txt', 'r') as file:
    nonconvex_instance_list = [line.strip() for line in file]

convex_instance_list = list(set(convex_instance_list) - set(failed_instances_names))
nonconvex_instance_list = list(
    set(nonconvex_instance_list) - set(failed_instances_names)
)

# Filter out the simple instances solved within 10 seconds

print('Filter out the simple instances solved within {} seconds'.format(threshold))

filtered_list = []
for baseline_method, method_list, instance_list in [
    ['OA', OA_method_list, convex_instance_list],
    ['LP/NLP-B&B', LPNLP_method_list, convex_instance_list],
    ['GOA', GOA_method_list, nonconvex_instance_list],
    ['GLP/NLP-B&B', GLPNLP_method_list, nonconvex_instance_list],
]:
    filtered_instance_list = set(instance_list) - set(
        df[(df['SolverName'] == baseline_method) & (df['SolverTime'] < threshold)][
            'InputFileName'
        ].to_list()
    )
    filtered_list += list(itertools.product(filtered_instance_list, method_list))

filtered_df = pd.DataFrame(filtered_list, columns=['InputFileName', 'SolverName'])
df = pd.merge(df, filtered_df, on=['InputFileName', 'SolverName'], how='right')
df[performance_index] = df[performance_index].fillna(900)

group_sizes = df.groupby('SolverName').size().reset_index(name='count')
print('group_sizes', group_sizes)


# Calculate the shifted geometric mean
def shifted_geometric_mean(group, shift_value):
    # Shift the values within the group
    shifted_values = group + shift_value

    # Calculate the geometric mean
    if len(shifted_values) == 0:
        return np.nan
    return gmean(shifted_values) - shift_value


result = (
    df.groupby('SolverName')[performance_index]
    .apply(lambda x: shifted_geometric_mean(x, shift_value=10))
    .reset_index()
)
result.columns = ['method', 'shifted_geometric_mean']

for method_list, baseline_method in zip(
    [OA_method_list, GOA_method_list, LPNLP_method_list, GLPNLP_method_list],
    ['OA', 'GOA', 'LP/NLP-B&B', 'GLP/NLP-B&B'],
):
    method_result = result[result['method'].isin(method_list)].reset_index(drop=True)
    baseline_sgm = method_result.loc[
        method_result['method'] == baseline_method, 'shifted_geometric_mean'
    ].iloc[0]
    method_result['normalized_shifted_geometric_mean'] = (
        method_result['shifted_geometric_mean'] / baseline_sgm
    )
    method_result['improvement'] = method_result[
        'normalized_shifted_geometric_mean'
    ].apply(lambda x: f"{(1-x):.2%}")
    method_result = method_result.iloc[::-1].reset_index(drop=True)

    print(method_result[['method', 'improvement']], '\n')
    method_result[['method', 'improvement']].to_csv(
        'performance_analysis_' + performance_index + '.csv',
        mode='a',
        header=True,
        index=False,
    )
