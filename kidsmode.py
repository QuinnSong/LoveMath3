# -*- coding: cp936 -*-
import random
import re

# Regex patterns to check if exp is valid
MD_PATTERN = r'(\d+(\*|/)\d+)'  ## * AND /
AM_PATTERN = r'(\d+(\+|-)\d+)'  ## + AND -
BRACKETS_PATTERN = r'.*?(\([^)(]+\))'  ## ( AND )
BAD_PATTERN_1 = r'^\([\d\-+]+\)[\d\-\+]+$'


def replace_ops(exp, pattern, num_limit, student_special_mode, check_every_step):
    """
    1) for * and /, make sure all ops result is in range limit
    2) for /, make sure there is no reminder
    3) finally replace * and / with actual result values
    If student special mode is on, then num_limit = 10 for * and / ops
    :param exp: math expression
    :param pattern: regex pattern to parse expression like a[+-*/]b
    :param num_limit: max value allowed
    :param student_special_mode: True for student special mode; False otherwise
    :return: math expression with the parsed exp calculated; None if invalid
    """
    while re.search(pattern, exp):
        md = re.search(pattern, exp)

        if student_special_mode:
            if md.groups()[1] in  ['+', '-'] and (eval(md.groups()[0]) not in range(0, 101)):
                exp = None
                break
            if md.groups()[1] in ['*','/'] and len(md.groups()[0]) > 3 or eval(md.groups()[0]) >= 10:
                exp = None
                break
        # no reminder allowed
        if md.groups()[1] == '/':
            i, j = md.groups()[0].split('/')
            if int(i) % int(j) != 0:
                exp = None
                break

        if (check_every_step and eval(md.groups()[0]) not in range(0, num_limit + 1)):
            exp = None
            break

        if exp:
            exp = exp.replace(md.groups()[0], str(eval(md.groups()[0])))
    return exp


def replace_brackets(exp, num_limit, student_special_mode, check_every_step):
    """
    1) for (), make sure all exps in brackets result is in range limit
    2) finally replace () with actual result values

    :param exp: math expression
    :param num_limit: max value allowed
    :param student_special_mode: True for student special mode; False otherwise
    :return: math expression without (); None if invalid
    """
    while re.search(BRACKETS_PATTERN, exp):
        brackets = re.findall(BRACKETS_PATTERN, exp)
        if any(eval(a) not in range(0, num_limit + 1) for a in brackets):
            exp = None
            break
        for b in brackets:
            tmp = check_in_brackets(b.strip(')('), num_limit, student_special_mode, check_every_step)
            if not tmp:
                exp = None
                break
            else:
                exp = exp.replace(b, str(eval(b)))
        if not exp: break
    return exp


def check_in_brackets(exp, num_limit, student_special_mode, check_every_step):
    """
    Check if the exp inside () is valid
    :param exp: math expression
    :param num_limit: max value allowed
    :param student_special_mode: True for student special mode; False otherwise
    :return: True if the exp inside () is valid; False otherwise
    """
    exp = replace_ops(exp, MD_PATTERN, num_limit, student_special_mode, check_every_step)
    if exp is None:
        return False
    exp = replace_ops(exp, AM_PATTERN, num_limit, student_special_mode, check_every_step)
    return True if exp else False


def isExpValid(exp, num_limit, student_special_mode, carry_or_borrow, check_every_step):
    """
    Main function to validate a expression
    :param exp: math expression
    :param num_limit: max value allowed
    :param student_special_mode: True for student special mode; False otherwise
    :return: True if valid; False otherwise
    """
    # ensure result is within range specified
    if eval(exp) not in range(0, num_limit + 1):
        return False

    # carry/borrow checkup
    if not (carry_or_borrow == hasCarryOrBorrow(exp)):
        return False

    if re.match(BAD_PATTERN_1, exp):
        return False

    # calculate exp in brackets
    exp = replace_brackets(exp, num_limit, student_special_mode, check_every_step)
    if exp is None:
        return False
    else:
        return check_in_brackets(exp, num_limit, student_special_mode, check_every_step)


def convertToDecimal(exp, seed, num_decimal=2):
    """
    Convert an integer expression to decimal expression
    :param exp: math expression
    :param seed: decimal list
    :param num_decimal: decimal digits
    :return:
    """
    nums = re.findall(r'\d+', exp)
    ops = re.findall(r'[^\d]+', exp)

    mask = lambda x: round(int(x) * random.choice(seed), num_decimal)
    nums_mask = [str(mask(i)) for i in nums]
    if len(nums) <= len(ops):
        k = ''.join([j for i in zip(ops, nums_mask) for j in i if j])
    else:
        k = ''.join([j for i in zip(nums_mask, ops) for j in i if j])
    return k


def hasCarryOrBorrow(exp):
    """
    Check expression to see if carry or borrow is required
    :param exp: math expression
    :return: True if carry/borrow is required; False otherwise
    """
    sign = re.findall(r'(\d+)([+*/-])(\d+)', exp)
    if sign[0][1] == '/':
        return False
    elif sign[0][1] == '*':
        return any([int(x) * int(y) >= 10 for x in list(sign[0][0]) for y in list(sign[0][2])])
    else:
        if eval(exp) < 0:
            return True
        else:
            grp = re.findall(r'(\d+)(.)(\d+)', exp)
            qty = min(len(grp[0][0]), len(grp[0][2]))
            pair = zip(list(grp[0][0][len(grp[0][0]) - qty:]), list(grp[0][2][len(grp[0][2]) - qty:]))
            # print pair
            return any([eval(x + grp[0][1] + y) >= 10 or eval(x + grp[0][1] + y) < 0 for x, y in pair])


def meetDigitLength(exp, totalDigits):
    """
    Check expression to see if it meets requirement for total digits
    :param exp: math expression
    :param lenRequired:
    :return: True if requirement is met; False otherwise
    """
    total_digits_list = re.findall(r'\d+', exp)
    return all([len(i)==totalDigits for i in total_digits_list])


if __name__ == '__main__':
    s1 = '23+18'
    s2 = '51-27'
    s3 = '60-26-19'
    s4 = '66-27+45'
    s0 = '31-99'
    s11 = '333-9'
    a = '(212+2)-(821-702)'
    # print(isExpValid('((5+2)*1+3-10)+2*3', 5))
    # print(isExpValid('6+(3-2)+5', 6))
    # print(isExpValid('(6-3)*6', 10))
    # print(calCarryOrBorrow (s3))
    # print(convertToDecimal(a, [0.1,0.2, 0.3, 0.4]))
    # print(replace_mul_div('44-30*5', MD_PATTERN, 100, True))
    # print(isExpValid('93+45-97', 100, True))
    # print(hasCarryOrBorrow('82*1113'))
    # print(calCarryOrBorrow('8-8+9', 10))
    # print(isExpValid('8*18/9', 20, False, False, True))
    print(isExpValid('18-(5+48)/16*3', 2000, False, True, True))
    # print(isExpValid('7/(1+7)*6', 100, True))
