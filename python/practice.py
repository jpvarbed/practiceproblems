import sys

# Question:

# Design a spreadsheet which can support two operations:

# void set_cell(string cell, string value)

# int get_cell(string cell)

# Example:
# set_cell("A1", "13)
# set_cell("A2", "14)
# get_cell("A1") -> 13
# set_cell("A3", "=A1+A2")
# get_cell("A3") -> 27
# https://leetcode.com/discuss/interview-question/860489/google-phone-design-a-spreadsheet
class SpreadSheet:
    # dictionaries
    def __init__(self):
        self.cells = {}
        self.memo = {}
    
    # we don't evaluate the expression here, we just store it
    def set_cell(self, cell, expression):
        self.cells[cell] = expression
        self.memo.clear()
    
    def get_cell(self, cell):
        visited = set()
        if cell in self.cells:
            return self.evaluate_expression(cell, visited)
        return None
    
    def evaluate_expression(self, cell, visited):
        if cell not in self.cells:
            raise ValueError("Cell not found")
        if cell in self.memo:
            return self.memo[cell]
        if cell in visited:
            return -1
        
        value = self.cells[cell]
        result = 0
        # Digit case
        if value.isdigit():
            result += int(value)
        elif value[0] == "-" and value[1:].isdigit():
            result -= int(value)
        elif value[0] == "=":
            values = self.split_expression(value[1:])
            operator = 1
            for value in values:
                if value == '+':
                    operator = 1
                elif value == '-':
                    operator = -1
                elif value.isdigit():
                    result += operator * int(value)
                else: # not an op or a digit so another cell
                    visited.add(cell)
                    sub_cell_value = self.evaluate_expression(value, visited)
                    if sub_cell_value == -1:
                        return -1
                    result += sub_cell_value
        
        self.memo[cell] = result
        return result

    # instead of re.split(r'(\+|\-)', value[1:])
    def split_expression(self, expression):
        values = []
        start = 0
        for i, c in enumerate(expression):
            if c in ('+', '-'):
                if start != i:
                    values.append(expression[start:i])
                values.append(c)
                start = i + 1
        # add the rest
        if start < len(expression):
            values.append(expression[start:])
        return values
    
def test_Spreadsheet():
    s = SpreadSheet()
    s.set_cell("A1", "13")
    s.set_cell("A2", "14")
    assert s.get_cell("A1") == 13
    s.set_cell("A3", "=A1+A2")
    s.get_cell("A3") == 27
    s.set_cell("A4", "=A3+11")
    # A1 = 13, A2 = 14, A3 = A1+A2 = 27, A4 = 38
    assert s.get_cell("A4") == 38
    s.set_cell("A4", "=A3+A2")
    assert s.get_cell("A4") == 41
    s.set_cell("A4", "=A3+A2+A1")
    assert s.get_cell("A4") == 54
    s.set_cell("A3", "=A4+12")
    assert s.get_cell("A3") == -1 # cycle  detected

def twoSum(nums: list[int], target: int) -> list[int]:
    sums = set ()
    for num in nums:
        sums.add(num)
    
    for i, num in enumerate(nums):
        if target - num in sums and (i != nums.index(target - num) or nums.count(num) > 1):
            if nums.count(num) > 1:
                return [i, nums.index(num, i+1)]
            return [i, nums.index(target - num)]
        
    return []

def twoSumBetter(self, nums: list[int], target: int) -> list[int]:
    numMap = {}
    n = len(nums)

    for i in range(n):
        complement = target - nums[i]
        if complement in numMap:
            return [numMap[complement], i]
        numMap[nums[i]] = i

    return []

def test_twoSum():
    assert twoSum([2,7,11,15], 9) == [0, 1]
    assert twoSum([3,2,4], 6) == [1, 2]
    assert twoSum([3,3], 6) == [0, 1]

def containsDuplicate(nums: list[int]) -> bool:
        allNums = set()
        for num in nums:
            if num in allNums:
                return True
            else:
                allNums.add(num)
        return False

def test_containsDuplicate():
    assert containsDuplicate([1,2,3,1]) == True
    assert containsDuplicate([1,2,3,4]) == False
    assert containsDuplicate([1,1,1,3,3,4,3,2,4,2]) == True

# https://leetcode.com/problems/maximum-subarray/description/
def maxSubArray(nums: list[int]) -> int:
        maxi = -sys.maxsize - 1
        sum = 0
        for i in range(len(nums)):
            sum += nums[i]

            if sum >= maxi:
                maxi = sum

            if sum < 0:
                sum = 0

        #if maxi < 0: maxi = 0
        return maxi

def test_maxSubArray():
    assert maxSubArray([-2,1,-3,4,-1,2,1,-5,4]) == 6
    assert maxSubArray([1]) == 1
    assert maxSubArray([5,4,-1,7,8]) == 23

# guaranteed to fit into int
# without division so cant just mult them all
#https://leetcode.com/problems/product-of-array-except-self/
def productExceptSelf(nums: list[int]) -> list[int]:
    ans = [1] * len(nums)
    prod, n_zeros = 1, 0
    for i, n in enumerate(nums):
        if n != 0: prod *= n
        if i < len(nums) - 1: ans[i+1] = prod
        n_zeros += n == 0

    if n_zeros > 1:
        for i in range(len(ans)):
            ans[i] = 0
    elif n_zeros == 1:
        for i in range(len(ans)):
            ans[i] = prod if nums[i] == 0 else 0
    else:
        prod = 1
        for i in range(len(ans) -1, 0, -1):
            ans[i] *= prod
            prod *= nums[i]
        ans[0] = prod
    return ans

def test_productExceptSelf():
    assert productExceptSelf([1,2,3,4]) == [24,12,8,6]
    assert productExceptSelf([-1,1,0,-3,3]) == [0,0,9,0,0]
    
# python practice.py
if __name__ == "__main__":
    test_Spreadsheet()
    test_twoSum()
    test_containsDuplicate()
    test_maxSubArray()
    test_productExceptSelf()
    print("All tests passed")