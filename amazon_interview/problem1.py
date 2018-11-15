from math import sqrt
from amazon_interview.statics import t_table
"""
Black: 30m
Red: 31m
Green: 32m
Yellow: 33m
Blue: 34m
Magenta: 35m
Cyan: 36m
White: 37m
RESET: 0m
"""
CSI = "\x1B["
Black = "90m"
Red = "91m"
Green = "92m"
Yellow = "93m"
Blue = "94m"
Magenta = "95m"
Cyan = "96m"
White = "97m"
RESET = "\033[0m"
precision = 4
r = lambda x: round(x, precision)


def std_dv(lst:list,indent:str,reset:str)->float:
    print(CSI+Blue,end="")
    print("{}# std_dv(lst:lst,indent:str,reset:str)".format(indent))
    d_sum =  sum(lst)
    d_sum_sqrs= sum(d**2 for d in lst)
    print("{}d_sum == {}".format(indent, r(d_sum)))
    print("{}d_sum_sqrs == {}".format(indent, r(d_sum_sqrs)))
    # num = (d_sum_sqrs- ((d_sum**2)/len(lst)))
    # den = (len(lst)-1)
    # ret = (d_sum_sqrs- ((d_sum**2)/len(lst)))/(len(lst)-1)
    # debugg_numerator ="({}-(({}**2)/{})) == {}".format(r(d_sum_sqrs), r(d_sum), r(len(lst)), r(num))
    # debugg_std_dev_expression = RESET+"debugging:\nnumerator == {};\n{}/{} == {}\nsqrt({}) == {}"\
    #     .format( debugg_numerator, r(num), r(den), r(ret), r(ret), r(sqrt(ret)))
    # print(debugg_std_dev_expression)
    print (CSI+reset,end="")
    return sqrt((d_sum_sqrs- ((d_sum**2)/len(lst)))/(len(lst)-1))


def calc_t_val(lst:list, indent:str,reset:str)->float:
    """We assume that meu difference in the null hypothesis is zero, but if we wanted to fact check on a null hyp that
    claims some predicted change, we would use that specified prediction of change for meu_d

    :param lst:
    :return:
    A tuple containing the following items:
        * t-stat:   which denotes an approximation for the possible number of standard deviations from the total
                    pop mean we could be. Used in our error assessment
        * d_bar:    The approximate mean for the element wise difference between our paired sample populations.
        * s:        The standard deviation of
    returns a tuple comprised of the following sample stats for the paired populations:
        (t_stat, paired_pop_diff_mean(aka, d_bar),

    """
    print(CSI+Magenta,end="")
    print("{}# calc_t_val(lst:list,indent:str, reset:str)->float:".format(indent))
    print("{}calculating test statistic for the following values:\n\t\t{}".format(indent, [r(d) for d in lst]))
    meu_d = 0
    d_bar = sum(lst)/len(lst)
    print("{}d_bar is: {}".format(indent, r(d_bar)))
    s = std_dv(lst, indent+"\t",Magenta)
    print("{}std_dev for given values: {}".format(indent, r(s)))
    s_d = s/sqrt(len(lst))
    print("{}std_dev for d_bar is: {}".format(indent, r(s_d)))
    print(CSI+reset,end="")
    return ((d_bar-meu_d)/s_d), d_bar,s,s_d

if __name__ == "__main__":
    # before = [210, 180, 195, 220, 231, 199, 224]
    # after = [193, 186, 186, 223, 220, 183, 233]
    # alpha = .05/2
    before = [5.9,7.5,6.1,6.8,8.1]
    after = [5.4,7.1,6.2,6.3,7.8]
    alpha = 0.05
    alpha_pos = sum(1 for x in t_table["alpha"] if x > alpha)
    print(CSI+Green)
    diff = [(b - a) for b, a in zip(before, after)]
    df = len(diff)-1
    t = t_table[str(df)][alpha_pos]
    t_stat = calc_t_val(diff,"\t",Green)
    print("given:\n\tdf == {}\n\talpha == {}\n\twe see that t == {}".format(df, alpha, t))
    print("values in before: {}".format([r(d) for d in before]))
    print("values in after:  {}".format([r(d) for d in after]))
    print("values in diff:   {}".format([r(d) for d in diff]))
    print("test statistic t for d_bar is: {}".format(r(t_stat)))
    print(RESET)

