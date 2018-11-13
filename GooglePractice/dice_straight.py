"""
    Problem
    You have a special set of N six-sided dice, each of which has six different positive integers on
    its faces. Different dice may have different numberings.

    You want to arrange some or all of the dice in a row such that the faces on top form a straight
    (that is, they show consecutive integers). For each die, you can choose which face is on top.

    How long is the longest straight that can be formed in this way?

    Input
    The first line of the input gives the number of test cases, T. T test cases follow. Each test
    case begins with one line with N, the number of dice. Then, N more lines follow; each of them
    has
    six positive integers Dij. The j-th number on the i-th of these lines gives the number on the
    j-th face of the i-th die.

    Output
    For each test case, output one line containing Case #x: y, where x is the test case number
    (starting from 1) and y is the length of the longest straight that can be formed.

    Limits
    1 ≤ T ≤ 100.
    1 ≤ Dij ≤ 106 for all i, j.

    Small dataset
    1 ≤ N ≤ 100.

    Large dataset
    1 ≤ N ≤ 50000.

    The sum of N across all test cases ≤ 200000.

    Sample

    Input

    Output

    3
    4
    4 8 15 16 23 42
    8 6 7 5 30 9
    1 2 3 4 55 6
    2 10 18 36 54 86
    2
    1 2 3 4 5 6
    60 50 40 30 20 10
    3
    1 2 3 4 5 6
    1 2 3 4 5 6
    1 4 2 6 5 3

    Case #1: 4
    Case #2: 1
    Case #3: 3

    In sample case #1, a straight of length 4 can be formed by taking the 2 from the fourth die, the
    3 from the third die, the 4 from the first die, and the 5 from the second die.

    In sample case #2, there is no way to form a straight larger than the trivial straight of
    length 1.

    In sample case #3, you can take a 1 from one die, a 2 from another, and a 3 from the remaining
    unused die. Notice that this case demonstrates that there can be multiple dice with the same set
    of values on their faces.
"""

import concurrent.futures as cf
import itertools
import os
import time
import json

class sequence_builder:
    def __init__(self, d2f: dict, f2d: dict) -> None:
        """an object that handles the task of searching for the longest sequence of discrete dice
        that
        can fit on a given interval.

        :param d2f: a dict mapping unique dice id numbers to their associated face values
        :param f2d: a dict mapping each face value in the union of all face values to the dice which
        posses a face of that value.
        """
        
        # the key structure for this dict should be a tuple: (face_val, dice_id)
        self.d2f = d2f
        self.f2d = f2d
        self.longest = 0
    
    def new_sequence(self, start_face: int, end_face: int):
        """

        :param start_face: An int representing the face value to start at (not an index position)
        :param end_face: An in representing the face value to end at (not an index position)
        :return:
        The longest sequence of dice that could be found.
        """
        
        if start_face+1<end_face:
            # initializing the first element-tier of the sequence dict
            self.longest = max(self._alt_build_sequence(start_face, end_face),
                               # self._build_sequence(set(), 0, start_face, end_face),
                               self.longest)
        return self.longest
    
    def face_gen(self, start:int, end:int):
        for face in range(start,end):
            yield face, self.f2d[face], len(self.f2d[face])
        
    def single_faces(self, sorted_face_dice_list:list):
        for face,dice,d_len in sorted_face_dice_list:
            if d_len==1:
                yield face,dice[0]
            else:
                break
    def other_faces(self, head:int, sorted_face_dice_list:list):
        for face,dice,d_len in sorted_face_dice_list[head:]:
            yield face,dice[0]
        
        
    def _alt_build_sequence(self, start: int, end: int) -> int:
        """
        Steps for placement order:
          First: Fill all face positions that have only 1 dice that can satisfy them.

          Second: Of the remaining dice, place all those that appear only 1 time within
          the range of start<=x<=end
          
                Note: The dice sets for the first and second steps are disjoint

          Third: Fill all remaining positions in the range from a priority que of remaining dice.
              This priority que shall be ordered according to the following, in order of importance:
                  1. ascending order for # of occurrences within the range.
                  2. ascending order for greatest face on the dice
          
          Fourth: starting at the beginning of the sequence, we attempt to fill the gaps in the

        :param start:
        :param end:
        :return:
        """
        if end <= start+1:
            return 1
        # faces_by_options will be a list of 3-tuples in the form of:
        #   (face_value, list_of_dice_ids, len(list_of_dice_ids))
        faces_by_options = sorted(((face, dice,d_len) for face, dice, d_len in self.face_gen(start,end)),
                                  key=lambda face, dice,d_len: d_len)
        # first_faces is a list of tuples representing all face values that only have a single dice
        # to represent them.
        # These tuples will be in the form of (face_value, dice_id)
        first_faces = tuple((face,dice) for face,dice in self.single_faces(faces_by_options))
        if len(first_faces) > 0:
            other_faces = self.other_faces(len(first_faces),faces_by_options)
        else:
            other_faces = faces_by_options
            first_faces = None
        
        # dice_set is a set of tuples in the form of: (dice_id,,count_of_usable_faces)
        dice_set = set(d for faces,d_ids in faces_by_options for d in d_ids)
        reset_tuple = tuple(dice_set)
        # we'll use this value later to see if we have our optimal sequence yet
        max_seq_len = len(dice_set)
        len_based_dice_map = dict()
        for d in reset_tuple:
            l = sorted([f for f in self.d2f[d] if start<=f<=end], reverse=True)
            if len(l) not in len_based_dice_map:
                len_based_dice_map[len(l)] = dict()
            len_based_dice_map[len(l)][d] = l
        
        final_sequence = [None]*(end-start)
        
        # now we finally start building the sequence
        # first by adding those face values that only appear on a single dice
        if first_faces:
            for face,dice_id in first_faces:
                assert(face >= start), "Failed assert when assigning dice_ids for first_face\n\tface < start"
                assert(final_sequence[face-start] is None),"Failed assert when assigning dice_ids for first_face\n\tfinal_sequence[face-start] wasn't None"
                if dice_id in dice_set:
                    final_sequence[face-start] = dice_id
                    dice_set.remove(dice_id)
        
        # now we place all of the dice that appear only one time into the sequence.
        for length in len_based_dice_map:
            for dice_id in len_based_dice_map[length]:
                face = len_based_dice_map[length][dice_id].pop()
                while final_sequence[face-start] is not None:
                    face = len_based_dice_map[length][dice_id].pop()
                    
                assert(face >= start), "Failed assert when assigning dice_ids for len_based_dice_map\n\tv[0] < start"
                assert(final_sequence[face-start] is None),"Failed assert when assigning dice_ids for len_based_dice_map\n\tfinal_sequence[v[0]-start] wasn't None"
                
                if dice_id in dice_set:
                    final_sequence[face-start] = dice_id
                    dice_set.remove(dice_id)
        
        
        
        nons = [pos for pos in range(len(final_sequence)) if final_sequence[pos] is None]
        return max((nons[i+1]-nons[i] for i in range(len(nons)-1)))
    
    def _build_sequence(self, d_sequence: set, depth: int, target_face: int, end: int) -> int:
        """This function will perform a depth-first-search for a dice sequence that can span the
        entire range from start to end, stopping should such a sequence be found, else it returns
        the longest sequence encountered during the search.

        :param d_sequence: A set of dice id's that represents the current sequence being explored
        :param depth: an int that tracks how deep we are able to get in this sequence before running
                      out of dice, or reaching the end of the specified face value range.
        :param target_face: An int representing which face in the sequence we are attempting to
                            match dice to.
        :param start: An int representing the
        :param end:
        :return:
        """
        if target_face+1<=end:
            next_dice = set(self.f2d[target_face])-d_sequence
            if len(next_dice)>0:
                with cf.ProcessPoolExecutor(int(os.cpu_count()*.9)) as ppe:
                    lengths = []
                    # ftrs = []
                    for dice in next_dice:
                        d_sequence.add(dice)
                        # ftrs.append(ppe.submit(self._build_sequence,d_sequence, depth+1,
                        # target_face+1,
                        #                        f2d,d2f,start,end))
                        lengths.append(
                            self._build_sequence(d_sequence, depth+1, target_face+1, end))
                        d_sequence.remove(dice)
                depth = max(lengths)
        return depth

def find_straight_end(starting_index: int,
                      check_point: int,
                      right_bound: int,
                      sorted_face_list: list,
                      case_num: int = -1) -> tuple:
    """Binary search for the end of the current straight, which starts at left_bound.

    It is assumed that key_list is already sorted in ascending order, so that we may use the
    value saved at sorted_face_list[left_bound][0] as an offset value for doing a binary search for
    the last index in the sorted_face_list where

    ::

        sorted_face_list[check_point][0]-sorted_face_list[left_bound][0] == check_point-left_bound

    :param starting_index: an int representing the index position for the first element in the
    current straight as it resides within the sorted_face_list.

    :param left_bound: an int representing the index position of a valid member element of the
    current straight that's less than check_point, and greater than or equal to starting_index.

    :param check_point: an int pointing to the next index of key_list that needs to be checked for
    satisfying the ongoing straight

    :param right_bound: an int representing a known maximum limit for where this straight may end.

    :param sorted_face_list: a list of all the unique face values from all dice in the current test
    case, sorted in ascending order.

    :return:
        returns the index positions of the first and last sequence in the current straight
    """
    left_bound = starting_index
    # while -1<left_bound<check_point<right_bound<len(sorted_face_list):
    while left_bound<check_point<right_bound<len(sorted_face_list):
        if sorted_face_list[check_point]-sorted_face_list[left_bound]==check_point-left_bound:
            # check_point indexes to a valid member of the current straight, so the end must be to
            # the right still
            left_bound = check_point
        else:
            # check_point indexes to an invalid member for the current straight, so we need to look
            # to the left of check_point
            right_bound = check_point
        check_point = (left_bound+right_bound)//2
    
    check_point = right_bound\
        if right_bound==check_point+1\
           and sorted_face_list[right_bound]==sorted_face_list[check_point]+1\
        else check_point
    return sorted_face_list[starting_index],\
           (sorted_face_list[check_point]
            if check_point-starting_index==sorted_face_list[check_point]-sorted_face_list[
               starting_index]
            else sorted_face_list[starting_index])

def single_case_solution(dice_list: list, case_num: int) -> tuple:
    """solve for a single case per process

    :param dice_list: a list of lists, where each sublist represents the faces of each descrete dice
    used in this test case.
    :param case_num: an int identifying which test case resulting return values belong to. Needed
    for us to parallel this functionality but not lose track of what the results mean.
    :return:
    """
    dice_list = [tuple(int(s) for s in line.split(" ")) for line in dice_list]
    d2f = {k:v for k, v in enumerate(dice_list)}
    longest_straight = 1
    f2d = dict()
    # building the set of unique dice faces for creating a straight, while also retaining the
    # mapping of which dice have a each face.
    for key in d2f:
        for face in d2f[key]:
            if face not in f2d:
                f2d[face] = list()
            f2d[face].append(key)
    
    sorted_face_list = sorted(list(f2d.keys()))
    strt = 0
    straights_list = []
    last_idx = len(sorted_face_list)-1
    while strt<len(sorted_face_list):
        start_face, end_face = find_straight_end(starting_index=strt,
                                                 check_point=(strt+last_idx)//2,
                                                 right_bound=last_idx,
                                                 sorted_face_list=sorted_face_list,
                                                 case_num=case_num)
        strt = end_face+1
        straights_list.append((start_face, end_face))
    # print("for case {}, we have a sorted list of:\n\t{}\n and straights_list has:\n\t {
    # }\n".format(case_num, sorted_face_list,straights_list))
    seq = sequence_builder(d2f, f2d)
    for start, end in straights_list:
        seq.new_sequence(start, end)
    return case_num, seq.longest

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
        results = []
        for case in range(1, test_num+1):
            dice_count = int(input_seq.pop())  # initial simple testing
            # getting the number of dice in the current test case
            # dice_count = int(input())
            # dice_list = [set(sorted([int(s) for s in input_seq.pop().split(" ")])) for d_count
            # in range(dice_count)]  # initial simple testing
            input_list = [input_seq.pop() for d_count in range(dice_count)]
            # dice_list = [line for line in input_list]a
            results.append(single_case_solution(input_list,case))
            # ftrs.append(ppe.submit(single_case_solution, input_list, case))
        time.sleep(2)
        for cas, res in results:
            print(output_string_template.format(cas, res))
        # for ftr in cf.as_completed(ftrs):
        #     cas, res = ftr.result()
        #     print(output_string_template.format(cas, res))
            # results.append(ftr.result())
        # results.sort(key=lambda tpl: tpl[0])
        # for case_num,res in results:
        #
        #     print(output_string_template.format(case_num,res))
        # print(ftr.result())

if __name__=="__main__":
    main()
