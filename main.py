from typing import List

import cvxpy


def Nash_budget(total: float, subjects: List[str], preferences: List[List[str]]):
    donations = []
    n = len(preferences)
    for _ in range(n):
        donations.append(total / n)
    allocations = cvxpy.Variable(len(subjects))
    utilities = []
    for i in range(len(preferences)):
        sum1 = 0
        for j in range(len(preferences[i])):
            index = subjects.index(preferences[i][j])
            sum1 += allocations[index]
        utilities.append(sum1)

    sum_of_logs = cvxpy.sum([cvxpy.log(u) for u in utilities])
    positivity_constraints = [v >= 0 for v in allocations]
    sum_constraint = [cvxpy.sum(allocations) == sum(donations)]
    problem = cvxpy.Problem(
        cvxpy.Maximize(sum_of_logs),
        constraints=positivity_constraints + sum_constraint)
    problem.solve()

    # print the result
    print("budget: ", end="")
    for i in range(len(list(allocations))):
        print(subjects[i], "=", allocations[i].value, end=" ")

    for i in range(len(preferences)):
        print("\ncitizen {} : gives ".format(i), end=" ")
        for j in range(len(preferences[i])):
            index = subjects.index(preferences[i][j])
            val = allocations[index].value * donations[i] / utilities[i].value
            if j != 0:
                print("and {} to {}".format(val, subjects[index]), end=" ")
            else:
                print("{} to {}".format(val, subjects[index]), end=" ")
    print("\n")


if __name__ == '__main__':
    total1 = 500
    subjects1 = ['a', 'b', 'c', 'd']
    preferences1 = [['a', 'b'], ['a', 'c'], ['a', 'd'], ['b', 'c'], ['a']]
    Nash_budget(total1, subjects1, preferences1)

    total1 = 1000
    subjects1 = ['a', 'b', 'c', 'd']
    preferences1 = [['a', 'b'], ['a', 'c'], ['a', 'd'], ['b', 'c']]
    Nash_budget(total1, subjects1, preferences1)

    total1 = 5000
    subjects1 = ['a', 'b', 'c']
    preferences1 = [['a', 'b'], ['a', 'c'], ['a', 'b'], ['b', 'c'], ['c']]
    Nash_budget(total1, subjects1, preferences1)
