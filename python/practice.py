import sys
from collections import deque, defaultdict # for aircargobooker
import heapq # for aircargobookercost
import bisect # calendar
# can't use for test problems but would be nice
# pip3 install sortedcontainers
# from sortedcontainers import SortedDict # Calendar

## Real life problems

## Calendar

# We’re going to be implementing a simplified calendar reservation product.
# You are building a system that helps reserve and arrange time slots on your calendar.
# In order to make it easy for implementing and focus on the real problem, we will use integer to represent timestamp on the calendar.
# i have 20 -25, 15-25 come in. i see the end time greater than start time and less than or equal to previous end time so false.
class Calendar:
    def __init__(self):
        self.events = []
        self.merged_intervals = []

    def _insert(self, time:int, event_type: str):
        bisect.insort(self.events, (time, event_type))

    def _remove(self, time: int, event_type: str):
        # left vs right for duplicates
        index = bisect.bisect_left(self.events, (time, event_type))
        self.events.pop(index)        
    # In order to make this question easier to implement,
    # let's use integer to represent the time on your calendar.
    # You will receive a pair of two integers start_time and end_time, the range of the booking time x should be start_time <= x < end_time.
    # Return true if the time slot is bookable (no double booked) and book the time slot, return false if anytime in the time slot is already booked.
    def book(self, start: int, end: int) -> bool:
        if start >= end:
            return False
        self._insert(start, 'start')
        self._insert(end, 'end')

        active_events = 0
        # check overlap
        for time, event_type in self.events:
            if event_type == 'start':
                active_events += 1
            else:
                active_events -= 1
            if active_events > 1:
                self.events.remove((start, 'start'))
                self.events.remove((end, 'end'))
                return False
        return True
    

    # Before you implement the calendar program above, you've arranged many meetings with overlaps.
    # Now you want to combine and merge meetings that are overlapped or consecutive.
    # There are so many meetings that you don't want to do it manually, so you will write a program to help you finish it.

    # You will receive a pair of two integers start_time and end_time one by one, and the output should be merged time slots without overlap.
    #     Example:
    # merge(10, 20) => [[10, 20]]
    # merge(40, 50) => [[10, 20], [40, 50]]
    # merge(20, 30) => [[10, 30], [40, 50]]
    # merge(45, 55) => [[10, 30], [40, 55]]
    def merge(self, start: int, end: int) -> list[list[int]]:
        new_interval = [start, end]
        merged = []
        i = 0
        while i < len(self.merged_intervals) and self.merged_intervals[i][1] < new_interval[0]:
            merged.append(self.merged_intervals[i])
            i += 1
        
        # Merge overlapping intervals
        while i < len(self.merged_intervals) and self.merged_intervals[i][0] <= new_interval[1]:
            new_interval[0] = min(new_interval[0], self.merged_intervals[i][0])
            new_interval[1] = max(new_interval[1], self.merged_intervals[i][1])
            i += 1

        merged.append(new_interval)
        
        # Add all intervals after the new interval
        while i < len(self.merged_intervals):
            merged.append(self.merged_intervals[i])
            i += 1
        
        self.merged_intervals = merged
        return self.merged_intervals

    # given all at once how to improve time complexity
    # merge([[10, 20], [40, 50], [20, 30], [45, 55]]) => [[10, 30], [40, 55]]
    def mergeAtOnce(self, times: list[list[int]]) -> list[list[int]]:
        return [[]]
    
    # Now you want to know how many times of a time slot is booked, so you want to return the booked times of each slot.

    # For example, if [10, 20) and [15, 25) are booked, the overlap is [15, 20), it is booked twice.
    # The other fragments are booked only once. So the output will be [10, 15), once, [15, 20), twice, [20, 25), once.
    #     Example:
    # merge(10, 20) => [[10, 20, 1]]
    # merge(40, 50) => [[10, 20, 1], [40, 50, 1]]
    # merge(20, 30) => [[10, 30, 1], [40, 50, 1]]
    # merge(45, 55) => [[10, 30, 1], [40, 45, 1], [45, 50, 2], [50, 55, 1]]
    def mergeTimesBooked(self, start: int, end: int) -> list[list[int]]:
        return [[]]

def test_calendar():
    c = Calendar()
    assert c.book(20, 25) == True
    assert c.book(15, 25) == False
    assert c.book(10, 20) == True
    assert c.book(11, 12) == False
    assert c.book(30, 40) == True

    assert c.merge(10, 20) == [[10, 20]]
    assert c.merge(40, 50) == [[10, 20], [40, 50]]
    assert c.merge(20, 30) == [[10, 30], [40, 50]]
    assert c.merge(45, 55) == [[10, 30], [40, 55]]

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

# [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0
def threeSum(nums: list[int]) -> list[list[int]]:
    # could use Counter(nums) from collections import Counter
    n = len(nums)
    ans = []
    nums.sort()
    for i in range(n):
        # skip dupes
        if i != 0 and nums[i] == nums[i - 1]:
            continue
        j = i + 1
        k = n - 1
        while j < k:
            sum = nums[i] + nums[j] + nums[k]
            if sum < 0:
                # need a larger number. k is already at the end so to get bigger increase j
                j += 1
            elif sum > 0:
                # need a smaller number. j is already at the start so to get smaller decrease k
                k -= 1
            else:
                temp = [nums[i], nums[j], nums[k]]
                ans.append(temp)
                j += 1
                k -= 1
                # ensures new value for nums[j]
                while j < k and nums[j] == nums[j-1]:
                    j += 1
                while j < k and nums[k] == nums[+1]:
                    k -= 1
    return ans

def test_threeSum():
    assert threeSum([-1,0,1,2,-1,-4]) == [[-1,-1,2],[-1,0,1]]
    assert threeSum([0, 1, 1]) == []
    assert threeSum([0,0,0]) == [[0,0,0]]

# https://leetcode.com/problems/container-with-most-water/description/
# container with most water. N vertical lines
# find hte two lines that together hold the most water. may not slant the container
def maxArea(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    maxi = 0
    while (left < right):
        area = min(height[left], height[right]) * (right - left)
        maxi = max(area, maxi)
        if (height[left] > height[right]): right -= 1
        else: left += 1

    return maxi

def test_maxArea():
    # 8 i:1, 7 i:8
    # 7 * 7 = 49
    assert maxArea([1,8,6,2,5,4,8,3,7]) == 49

    assert maxArea([1, 1]) == 1

# https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/
# buy one day, sell another
def maxProfit(prices: list[int]) -> int:
    maxProfit = 0
    minimumPrice = prices[0]
    # dont use prices[1:] because that will do a copy
    for i in range(1, len(prices)):
        if prices[i] < minimumPrice:
            minimumPrice = prices[i]
        if prices[i] - minimumPrice > maxProfit:
            maxProfit = prices[i] - minimumPrice

    return maxProfit

def test_maxProfit():
    assert maxProfit([7,1,5,3,6,4]) == 5
    assert maxProfit([7,6,4,3,1]) == 0

## Graph Problems
# m x n island
# return m by n list
# return cells that can reach both oceans. pacific is top and left, atlantic bottom and right
# water can reach the next cell if it is less than or equal to current cell
# heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
# output = [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]

# heights = [[1]]
# output [[0, 0]]
# could build a graph and then dfs for route?
# https://leetcode.com/problems/pacific-atlantic-water-flow/
def pacificAtlantic(heights: list[list[int]]) -> list[list[int]]:
    if not heights:
        return []

    m, n = len(heights), len(heights[0])
    # make n by m grid. too much mem probably
    pacific_reachable = [[False] * n for _ in range(m)]
    atlantic_reachable = [[False] * n for _ in range(m)]

    # dfs because we want to go to all cells that can be reached by this node
    def dfs(r, c, reachable):
        # edges are reachable. mark them true
        reachable[r][c] = True
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            # new r and c
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < m
                and 0 <= nc < n
                and not reachable[nr][nc]
                and heights[nr][nc] >= heights[r][c]
            ):
                dfs(nr, nc, reachable)

    # mark all the cells that reach the ocean. start from the ocean
    for i in range(m):
        # left edge/column
        dfs(i, 0, pacific_reachable)
        # last column/ right edge
        dfs(i, n - 1, atlantic_reachable)

    for j in range(n):
        # first row/top edge
        dfs(0, j, pacific_reachable)
        # last row/bottom edge
        dfs(m - 1, j, atlantic_reachable)

    result = []
    for i in range(m):
        for j in range(n):
            if pacific_reachable[i][j] and atlantic_reachable[i][j]:
                result.append([i, j])

    return result

def test_pacificAtlantic():
    heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
    assert pacificAtlantic(heights) == [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]
    assert pacificAtlantic([[1]]) == [[0, 0]]
    assert pacificAtlantic([[1,1], [1,1], [1,1], [1,1]]) == [[1,1]]

# python practice.py
if __name__ == "__main__":
    test_Spreadsheet()
    test_aircargobooker()
    test_aircargobookercost()
    test_calendar()
    # Arrays https://takeuforward.org/interviews/blind-75-leetcode-problems-detailed-video-solutions
    test_twoSum()
    test_containsDuplicate()
    test_maxSubArray()
    test_productExceptSelf()
    test_maxProduct()
    test_findMinRotatedSortedArray()
    test_searchRotatedArray()
    test_threeSum()
    test_maxArea()
    test_maxProfit()
    # Graphs
    test_pacificAtlantic()
    print("All tests passed")