#!/bin/python3
import os
import sys

from typing import Dict, Optional, Tuple
import re


valid_operators = ['+', '-', '*', '/']


def max_result_expression(expression: str,
                          variables: Dict[str, Tuple[int, int]]) -> Optional[
    int]:
    """
    Evaluates the prefix expression and calculates the maximum result for the given variable ranges.

    Arguments:
        expression: the prefix expression to evaluate.
        variables: Keys of this dictionary may appear as variables in the expression.
            Values are tuples of `(min, max)` that specify the range of values of the variable.
            The upper bound `max` is NOT included in the range, so (2, 5) expands to [2, 3, 4].

    Returns:
        int:  the maximum result of the expression for any combination of the supplied variables.
        None: in the case there is no valid result for any combination of the supplied variables.
    """
    valid_expression = check_validity(expression)
    if not valid_expression:
        return
    elif isinstance(valid_expression, int):
        return valid_expression
    else:
        final_result = evaluate_expression(valid_expression, variables)
        return final_result


def evaluate_expression(expression, variables):
    while len(expression) > 1:
        for item in range(len(expression)-2):
            if expression[item] in valid_operators:
                if not expression[item+1] in valid_operators \
                        and not expression[item+2] in valid_operators:
                    left, right = expression[item+1], expression[item+2]
                    if left in variables:
                        left = variables[-2]
                    if right in variables:
                        right = variables[-2]
                    # print(left, expression[item], right)
                    result = eval(left + expression[item] + right)
                    expression = \
                        expression[:item] + [str(result)] + expression[item+3:]
                    # print(expression)
                    break
    return expression[-1]


def check_validity(expression):
    ops = expression.split()
    count = len(ops)
    if count == 0:
        return
    elif count == 1:
        if re.match('[0-9]+', ops[0]):
            return int(ops[0])
        else:
            return
    else:
        operator_count = 0
        operand_count = 0
        for op in ops:
            if op in valid_operators:
                operator_count += 1
            else:
                operand_count += 1
        if operator_count + 1 != operand_count:
            return
    return ops


# print(check_validity("+ 12 a"))
print(max_result_expression("+ 6 * - 4 + 2 3 8", {}))
