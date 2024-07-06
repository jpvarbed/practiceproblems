import sys
from collections import deque, defaultdict # for aircargobooker
import heapq # for aircargobookercost

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

# We’re going to be implementing a simplified air cargo booking system.
# In the system, users can create orders, and your job is to help match them according to an inventory of flights you have access to.
# To begin implementing our booking system, we must first determine if orders can be fulfilled. For now, each order consists of an origin and a destination.
# Given a network of flights, create a function to determine if a booking order can be satisfied (a direct flight exists between origin and destination). How you choose to model orders, the flights, and the network is totally up to you.
# Part 1: Just check direct flight
# Part 2: find even with connections
# part 3: find with least connections
# part 4 cheapest route - can just use black box 
class AirCargoBooker:
    def __init__(self):
        # useful to avoid key errors accessing keys that do not exist yet
        self.graph = defaultdict(list)
    
    

    def add_flight(self, flight_number: str, origin: str, destination: str):
        self.graph[origin].append(destination)
    # For example, given the following network, an order from (SFO, ORD) can be satisfied but not (SFO, JFK):
    # AA100: SFO → ORD
    # AA200: SFO → LAX
    # AA201: LAX → SFO
    # DL90: ORD → JFK
    def canSupportOrder(self, order: tuple) -> bool:
        origin, destination = order
        path = self._bfs(origin, destination)
        return path if path else False
    
    def _bfs(self, start: str, goal: str):
        if start == goal:
            return [start]
        
        visited = set()
        queue = deque([(start, [start])]) #stores tuples of current airport, path to current
        while queue:
            current, path = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            
            for neighbor in self.graph[current]:
                if neighbor == goal:
                    return path + [neighbor]
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

        return None
    
def test_aircargobooker():
    b = AirCargoBooker()
    b.add_flight("AA100", "SFO", "ORD")
    b.add_flight("AA200", "SFO", "LAX")
    b.add_flight("AA201", "LAX", "SFO")
    b.add_flight("DL90", "ORD", "JFK")
    assert b.canSupportOrder(("SFO", "ORD")) == ["SFO", "ORD"]
    assert b.canSupportOrder(("SFO", "JFK")) == ["SFO", "ORD", "JFK"]
    assert b.canSupportOrder(("LAX", "JFK")) == ["LAX", "SFO", "ORD", "JFK"]
    assert b.canSupportOrder(("JFK", "SFO")) == False

class AirCargoBookerCost:
    def __init__(self):
        # Graph adjacency list where key is an airport and value is a list of tuples (destination, cost)
        self.graph = defaultdict(list)
    
    def add_flight(self, flight_number: str, origin: str, destination: str, cost: int):
        self.graph[origin].append((destination, cost))
    
    def find_cheapest_path_with_stops(self, origin: str, destination: str, max_stops: int):
        # Priority queue to store (cost, current_airport, path_to_current, stops)
        # This makes a heapq minheap.
        # can use neg value to get maxheap version
        queue = [(0, origin, [origin], 0)]
        visited = defaultdict(lambda: float('inf'))  # store the minimum cost to reach each node with a given stops
        
        while queue:
            current_cost, current_airport, path, stops = heapq.heappop(queue)
            
            if current_airport == destination:
                return path, current_cost
            
            if stops > max_stops:
                continue
            
            for neighbor, cost in self.graph[current_airport]:
                new_cost = current_cost + cost
                if new_cost < visited[(neighbor, stops + 1)]:
                    visited[(neighbor, stops + 1)] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor, path + [neighbor], stops + 1))
        
        return None, float('inf')
    
def test_aircargobookercost():
    booker = AirCargoBookerCost()
    booker.add_flight("AA100", "SFO", "ORD", 3000)
    booker.add_flight("AA200", "SFO", "LAX", 1500)
    booker.add_flight("AA201", "LAX", "SFO", 1500)
    booker.add_flight("DL90", "ORD", "JFK", 1500)
    booker.add_flight("DL123", "SFO", "DEN", 2000)
    booker.add_flight("DL456", "DEN", "JFK", 2000)
    path, cost = booker.find_cheapest_path_with_stops("SFO", "JFK", 1)
    assert path == ["SFO", "DEN", "JFK"]
    assert cost == 4000

    # Find the cheapest path with at most 2 stops
    path, cost = booker.find_cheapest_path_with_stops("SFO", "JFK", 2)
    assert path == ["SFO", "DEN", "JFK"]
    assert cost == 4000
    # print(f"Cheapest path with at most 2 stops: {path} with cost ${cost}")

# find a subarray with the largest product and return the product
# 2,3,-2,4 -> 6 2,3
# -2, 0, -1 -> 0 -2, -1 is not a subarray
# https://leetcode.com/problems/maximum-product-subarray/description/
# keep multipling until you hit 0 or negative. but then if you get another negative it switches
# find number of negatives
# if zero you restart from 1
# by doing backwards and forwards you catch the negative cases
def maxProduct(nums: list[int]) -> int:
    prod = 1
    maxi = float('-inf')
    for num in nums:
        prod *= num

        if prod > maxi:
            maxi = prod
        
        if prod == 0:
            prod = num

        if num > maxi:
            maxi = num

    prod = 1
    for num in nums[::-1]:
        prod *= num
        if prod > maxi:
            maxi = prod
        if prod == 0:
            prod = num
    return maxi

def test_maxProduct():
    assert maxProduct([2, 3, -2, 4]) == 6
    assert maxProduct([-2, 0, -1]) == 0
    assert maxProduct([0, 2]) == 2
    assert maxProduct([3, -1, 4]) == 4

# nums = [0,1,2,4,5,6,7]
# [4,5,6,7,0,1,2] if it was rotated 4 times.
# [0,1,2,4,5,6,7] if it was rotated 7 times.
# find min in o logn time
# bin search
# unique no equals
def findMinRotatedSortedArray(nums: list[int]) -> int:
    first = 0
    last = len(nums) - 1
    while (first < last - 1):
        midpoint = first + (last - first) // 2
        # print(f"{first}-{last}-{midpoint}")
        if nums[midpoint] > nums[last]:
            # go right
            first = midpoint
            last = last
        elif nums[midpoint] < nums[first]:
            # check left
            first = first
            last = midpoint
        else:
            break


    return min(nums[first], nums[last])

def test_findMinRotatedSortedArray():
    assert findMinRotatedSortedArray([4,5,6,7,0,1,2]) == 0
    assert findMinRotatedSortedArray([0,1,2,4,5,6,7]) == 0

# find the min
# search from there would be 2 logn
# do i need to find the min?
# can i just always look above or below based on my num?
# [4,5,6,7,0,1,2]
# [0, 1, 2, 3, 4, 5, 6, 7] 0 4
# was stuck on 3 4 3
def searchRotatedArray( nums: list[int], target: int) -> int:
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = (left + right) //2
        if nums[mid] == target:
            return mid
        # left half is sorted
        elif nums[mid] >= nums[left]:
            # mid bigger than left edge. If target is in between us try there
            if nums[left] <= target <= nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] <= target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1


def test_searchRotatedArray():
    assert searchRotatedArray([4,5,6,7,0,1,2], 0) == 4
    assert searchRotatedArray([4,5,6,7,0,1,2], 3) == -1
    assert searchRotatedArray([1], 0) == -1

# python practice.py
if __name__ == "__main__":
    # Arrays https://takeuforward.org/interviews/blind-75-leetcode-problems-detailed-video-solutions
    test_Spreadsheet()
    test_twoSum()
    test_containsDuplicate()
    test_maxSubArray()
    test_productExceptSelf()
    test_aircargobooker()
    test_aircargobookercost()
    test_maxProduct()
    test_findMinRotatedSortedArray()
    test_searchRotatedArray()
    print("All tests passed")