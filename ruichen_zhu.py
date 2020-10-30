from scipy import stats
from scipy.stats import t as t_dist
from scipy.stats import chi2
import math
from abtesting_test import *

def slice_2D(list_2D, start_row, end_row, start_col, end_col):
    '''
    Splices a the 2D list via start_row:end_row and start_col:end_col
    :param list: list of list of numbers
    :param nums: start_row, end_row, start_col, end_col
    :return: the spliced 2D list (ending indices are exclsive)
    '''
    to_append = []
    for l in range(start_row, end_row):
        to_append.append(list_2D[l][start_col:end_col])

    return to_append

def get_avg(nums):
    '''
    Helper function for calculating the average of a sample.
    :param nums: list of numbers
    :return: average of list
    '''
    #TODO: fill me in!
    num = 0
    for l in nums:
        num += l
    num = num/len(nums)
    return num

def get_stdev(nums):
    '''
    Helper function for calculating the standard deviation of a sample.
    :param nums: list of numbers
    :return: standard deviation of list
    '''
    #TODO: fill me in!
    avg = get_avg(nums)
    num = 0
    for l in nums:
        num+=(l-avg)*(l-avg)
    num = math.sqrt(num/(len(nums)-1))
    return num
    

def get_standard_error(a, b):
    '''
    Helper function for calculating the standard error, given two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: standard error of a and b (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    x = math.pow(get_stdev(a),2)/len(a)
    y = math.pow(get_stdev(b),2)/len(b) 
    num = math.sqrt(x+y)
    return num

def get_2_sample_df(a, b):
    '''
    Calculates the combined degrees of freedom between two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: integer representing the degrees of freedom between a and b (see studio 6 guide for this equation!)
    HINT: you can use Math.round() to help you round!
    '''
    #TODO: fill me in!
    x = math.pow(get_stdev(a),2)/len(a)
    y = math.pow(get_stdev(b),2)/len(b) 
    x = math.pow(x,2)/(len(a)-1)
    y = math.pow(y,2)/(len(b)-1)
    num = round(math.pow(get_standard_error(a,b),4)/(x+y))
    return num

def get_t_score(a, b):
    '''
    Calculates the t-score, given two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: number representing the t-score given lists a and b (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    t = (get_avg(a)-get_avg(b))/get_standard_error(a,b)
    if t>0:
        t = -t
    return t

def perform_2_sample_t_test(a, b):
    '''
    ** DO NOT CHANGE THE NAME OF THIS FUNCTION!! ** (this will mess with our autograder)
    Calculates a p-value by performing a 2-sample t-test, given two lists of numbers.
    :param a: list of numbers
    :param b: list of numbers
    :return: calculated p-value
    HINT: the t_dist.cdf() function might come in handy!
    '''
    #TODO: fill me in!
    x = get_2_sample_df(a,b)
    y = get_t_score(a,b)
    return t_dist.cdf(y,x)


# [OPTIONAL] Some helper functions that might be helpful in get_expected_grid().
# def row_sum(observed_grid, ele_row):
# def col_sum(observed_grid, ele_col):
# def total_sum(observed_grid):
# def calculate_expected(row_sum, col_sum, tot_sum):
def row_sum(observed_grid, ele_row):
    num = 0
    for l in observed_grid[ele_row]:
        num += l
    return num

def col_sum(observed_grid, ele_col):
    num = 0
    for row in range(len(observed_grid)):
        num+= observed_grid[row][ele_col]
    return num


def total_sum(observed_grid):
    num = 0
    for l in range(len(observed_grid)):
        num+= row_sum(observed_grid, l)
    return num

def calculate_expected(row_sum, col_sum, tot_sum):
    num = row_sum*col_sum/tot_sum
    return num

def get_expected_grid(observed_grid):
    '''
    Calculates the expected counts, given the observed counts.
    ** DO NOT modify the parameter, observed_grid. **
    :param observed_grid: 2D list of observed counts
    :return: 2D list of expected counts
    HINT: To clean up this calculation, consider filling in the optional helper functions below!
    '''
    #TODO: fill me in!
    expected = []
    for i in range(len(observed_grid)):
        row = []
        for j in range(len(observed_grid[0])):
            temp = calculate_expected(row_sum(observed_grid,i),col_sum(observed_grid,j), total_sum(observed_grid))
            row.append(temp)
        expected.append(row)
    return expected        
            
    

def df_chi2(observed_grid):
    '''
    Calculates the degrees of freedom of the expected counts.
    :param observed_grid: 2D list of observed counts
    :return: degrees of freedom of expected counts (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    num = (len(observed_grid)-1)*(len(observed_grid[0])-1)
    return num

def chi2_value(observed_grid):
    '''
    Calculates the chi^2 value of the expected counts.
    :param observed_grid: 2D list of observed counts
    :return: associated chi^2 value of expected counts (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    expected = get_expected_grid(observed_grid)
    num = 0
    for i in range(len(observed_grid)):
        for j in range(len(observed_grid[0])):
            num += pow(observed_grid[i][j]-expected[i][j],2)/expected[i][j]
    return num

def perform_chi2_homogeneity_test(observed_grid):
    '''
    ** DO NOT CHANGE THE NAME OF THIS FUNCTION!! ** (this will mess with our autograder)
    Calculates the p-value by performing a chi^2 test, given a list of observed counts
    :param observed_grid: 2D list of observed counts
    :return: calculated p-value
    HINT: the chi2.cdf() function might come in handy!
    '''
    #TODO: fill me in!
    x = chi2_value(observed_grid)
    df = df_chi2(observed_grid)
    return 1-chi2.cdf(x,df)
    

# These commented out lines are for testing your main functions. 
# Please uncomment them when finished with your implementation and confirm you get the same values :)
def data_to_num_list(s):
  '''
    Takes a copy and pasted row/col from a spreadsheet and produces a usable list of nums. 
    This will be useful when you need to run your tests on your cleaned log data!
    :param str: string holding data
    :return: the spliced list of numbers
    '''
  return list(map(float, s.split()))

time_a = """9575
37834
12671
17479
32277
6241
12619
30594
32132
4343
8840
5811
24236"""


time_b = """14029
8125
407299
21152
19030
59214
11573
29058
12927
12696
9593
69807
5979"""

return_a = """10 3"""
return_b = """8 5""" 

timea_tlist = data_to_num_list(time_a) 
timeb_tlist = data_to_num_list(time_b)
print(get_t_score(timea_tlist, timeb_tlist))
print(perform_2_sample_t_test(timea_tlist, timeb_tlist))

returna_clist = data_to_num_list(return_a) 
returnb_clist = data_to_num_list(return_b)
c_observed_grid = [returna_clist, returnb_clist]
print(chi2_value(c_observed_grid))
print(perform_chi2_homogeneity_test(c_observed_grid))





