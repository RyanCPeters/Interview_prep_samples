# Problem
# You have a special set of N six-sided dice, each of which has six different positive integers on
# its faces. Different dice may have different numberings.
#
# You want to arrange some or all of the dice in a row such that the faces on top form a straight
# (that is, they show consecutive integers). For each die, you can choose which face is on top.
#
# How long is the longest straight that can be formed in this way?
#
# Input
# The first line of the input gives the number of test cases, T. T test cases follow. Each test
# case begins with one line with N, the number of dice. Then, N more lines follow; each of them has
# six positive integers Dij. The j-th number on the i-th of these lines gives the number on the
# j-th face of the i-th die.
#
# Output
# For each test case, output one line containing Case #x: y, where x is the test case number
# (starting from 1) and y is the length of the longest straight that can be formed.
#
# Limits
# 1 ≤ T ≤ 100.
# 1 ≤ Dij ≤ 106 for all i, j.
#
# Small dataset
# 1 ≤ N ≤ 100.
#
# Large dataset
# 1 ≤ N ≤ 50000.
#
# The sum of N across all test cases ≤ 200000.
#
# Sample
#
# Input
#
# Output
#
# 3
# 4
# 4 8 15 16 23 42
# 8 6 7 5 30 9
# 1 2 3 4 55 6
# 2 10 18 36 54 86
# 2
# 1 2 3 4 5 6
# 60 50 40 30 20 10
# 3
# 1 2 3 4 5 6
# 1 2 3 4 5 6
# 1 4 2 6 5 3
#
# Case #1: 4
# Case #2: 1
# Case #3: 3
#
# In sample case #1, a straight of length 4 can be formed by taking the 2 from the fourth die, the
# 3 from the third die, the 4 from the first die, and the 5 from the second die.
#
# In sample case #2, there is no way to form a straight larger than the trivial straight of
# length 1.
#
# In sample case #3, you can take a 1 from one die, a 2 from another, and a 3 from the remaining
# unused die. Notice that this case demonstrates that there can be multiple dice with the same set
# of values on their faces.

import concurrent.futures as cf
import os
from functools import reduce

class dice_tree:
    class dtnode:
        """
        This class will represent a branching tree structure that tracks all of the possible
        """
        
        def __init__(self, my_face: int, associated_dice: tuple) -> None:
            # list of index values for where to find all dice that have a face equal to my_face
            self.associated_dice = associated_dice
            self.face = my_face
    
    def __init__(self, face_dice_dict: dict, dice_face_dict: dict) -> None:
        self.root = None
        self.face_dice_dict = face_dice_dict    # {face_value: (dice_id, possessing, this, face, value)}
        self.dice_face_dict = dice_face_dict    # {dice_id:    (face, values, on, this, dice_id)
        
    
    def add_from_face_range(self, least_face:int, greatest_face:int)->int:
        """Depth-first search for the longest viable dice-chain that represents a continuous
        sequence-set of dice that would allow us to represent as many of the face values on the
        range of least_face <= x <= greatest_face as possible.
        
        Given face values on the range of least_face < x < greatest_face, we build out a depth first
        search of dice-chains which could be used to as a continuous sequence of dice, with each
        discrete dice element being used only once in a sequence, that would allow us to represent
        as many face values between least_face and greatest_face, inclusively, as possible.
        
        ASSUMPTIONS:
        
        ::
            
            Note that it is assumed that the caller has already verified that there is a continuous
            range of face values, in the current test case, between least_face and greatest_face.
        
        :param least_face:
        an int representing the smallest face value in the straight being checked
        
        :param greatest_face:
        an int representing the largest face value in the straight being checked
        
        :return:
            an int representing the longest dice_chain sequence possible
        """
        unique_sequence_list = list()
        
        


def find_straight_end(starting_index: int, left_bound: int, check_point: int, right_bound: int,
                      face_dIdx_pairs: tuple, dice_list: list) -> tuple:
    """Binary search for the end of the current straight, which starts at left_bound.

    It is assumed that key_list is already sorted in ascending order, so that we may use the
    value saved at face_dIdx_pairs[left_bound][0] as an offset value for doing a binary search for
    the last index in the face_dIdx_pairs where

    ::

        face_dIdx_pairs[check_point][0]-face_dIdx_pairs[left_bound][0] == check_point-left_bound

    :param starting_index: an int representing the index position for the first element in the
    current straight as it resides within the face_dIdx_pairs.

    :param left_bound: an int representing the index position of a valid member element of the
    current straight that's less than check_point, and greater than or equal to starting_index.

    :param check_point: an int pointing to the next index of key_list that needs to be checked for
    satisfying the ongoing straight

    :param right_bound: an int representing a known maximum limit for where this straight may end.

    :param face_dIdx_pairs: an ordered tuple of int/list pairings. Where the int values represent
    a set of discrete face values that can be found across all dice. Associated with each face
    value
    is a list of all the dice which have a face that matches that value.

    :param dice_list: a list of lists where each individual sub-list represents the face values of
    a discrete dice belonging to the current test case.

    :return:
        returns the index positions of the first and last elements in the current straight
    """
    while -1<left_bound<check_point<right_bound<len(face_dIdx_pairs):
        if face_dIdx_pairs[check_point][0]-face_dIdx_pairs[left_bound][0]==check_point-left_bound\
                and:
            # check_point indexes to a valid member of the current straight, so the end must be to
            # the right still
            left_bound = check_point
        else:
            # check_point indexes to an invalid member for the current straight, so we need to look
            # to the left of check_point
            right_bound = check_point
        check_point = (left_bound+right_bound)//2
    
    return starting_index, right_bound
    pass

def single_case_solution(dice_list: list, case_num: int) -> tuple:
    """

    :param dice_list: a list of lists, where each sublist represents the faces of each descrete dice
    used in this test case.
    :param case_num: an int identifying which test case resulting return values belong to. Needed
    for us to parallel this functionality but not lose track of what the results mean.
    :return:
    """
    dice_face_dict = {k:tuple(v) for k,v in enumerate(dice_list)}
    longest_straight = 1
    dice_to_face_map = dict()
    # building the set of unique dice faces for creating a straight, while also retaining the
    # mapping of which dice have a each face.
    for dice_idx, dice_face_tuple in dice_face_dict.items():
        for face_key in dice_face_tuple:
            if face_key not in dice_to_face_map:
                dice_to_face_map[face_key] = []
            dice_to_face_map[face_key].append(dice_idx)
    
    
    return case_num, longest_straight

def main():
    with open("dice_straight_sample.txt", "r+") as f:
        input_seq = [line.strip("\n") for line in f.readlines()]
    input_seq.reverse()
    output_string_template = "Case #{}: {}"
    results_list = []
    test_num = int(input_seq.pop())  # initial simple testing
    # the first line of input file should be number of test cases
    # test_num = int(input())
    max_workers = os.cpu_count()
    max_workers = int(max_workers*.9)
    with cf.ProcessPoolExecutor(max_workers=max_workers) as ppe:
        ftrs = []
        for case in range(1, test_num+1):
            dice_count = int(input_seq.pop())  # initial simple testing
            # getting the number of dice in the current test case
            dice_count = int(input())
            dice_list = [[int(s) for s in input_seq.pop().split(" ")].sort()
                         # initial simple testing
                         for d_count in range(dice_count)]  # initial simple testing
            
            # dice_list = [[int(s) for s in input().split(" ")].sort() for d_count in range(
            # dice_count)]
            ftrs.append(ppe.submit(single_case_solution, dice_list, case))
        for ftr in cf.as_completed(ftrs):
            # print(output_string_template.format(ftr.result()))
            print(ftr.result())

if __name__=="__main__":
    main()
