import sys
from collections import deque, defaultdict, Counter # for aircargobooker & alienOrder
import heapq # for aircargobookercost
import bisect # calendar
from sortedcontainers import SortedDict # Calendar

## Real life problems

## dialerpad
# DICT = {
#   '1' => ['a', 'b'],
#   '2' => ['c', 'd']
# }
class DialerPad:
    def __init__(self, dictionary):
        self.dict = dictionary

    # keys are one digit
    def get_words(self, nums: str) -> list[str]:
        words = ['']
        for digit in nums:
            possible_letters = self.dict[digit]
            next_words = []
            for l in possible_letters:
                for word in words:
                    next_words.append(word + l)
            words = next_words
        return words
    # keys are multi char
    # recursive
    def get_words_long_keys(self, nums: str) -> list[str]:
        all_words = []
        if len(nums) == 0: return ['']
        # iterate through slices as prefixes
        # get entire string in the slice
        for split in range(len(nums) + 1):
            # check for prefix
            if nums[:split] in self.dict:
                possible_letters = self.dict[nums[:split]]
                suffixes = self.get_words_long_keys(nums[split:])
                words = []
                for l in possible_letters:
                    for suffix in suffixes:
                        words.append(l + suffix)
                all_words += words
        return all_words

def test_DialerPad():
    DICT = {
        '1': ['a', 'b'],
        '2': ['c', 'd'],
    }
    dialer = DialerPad(DICT)
    assert dialer.get_words('') == ['']
    assert dialer.get_words("1") == ['a', 'b']
    assert dialer.get_words("12") == ['ac', 'bc', 'ad', "bd"]
    assert dialer.get_words("122") == ["acc", 'bcc', 'adc', 'bdc', 'acd', 'bcd', 'add', 'bdd']
    LONG_DICT = {
        '1': ['a', 'b'],
        '2': ['c', 'd'],
        '12': ['x'],
        '22': ['y'],
    }
    fancy_dialer = DialerPad(LONG_DICT)
    assert fancy_dialer.get_words_long_keys('12') == ['ac', 'ad', 'bc', 'bd', 'x']
    assert fancy_dialer.get_words_long_keys('122') == ['acc', 'acd', 'adc', 'add', 'ay', 'bcc', 'bcd', 'bdc', 'bdd', 'by', 'xc', 'xd']
                                       
## Calendar

# We’re going to be implementing a simplified calendar reservation product.
# You are building a system that helps reserve and arrange time slots on your calendar.
# In order to make it easy for implementing and focus on the real problem, we will use integer to represent timestamp on the calendar.
# i have 20 -25, 15-25 come in. i see the end time greater than start time and less than or equal to previous end time so false.
class Calendar:
    def __init__(self):
        self.events = []
        self.merged_intervals = []
        self.merged_events = SortedDict()
        self.events_booked = SortedDict()

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
        for start, end in times:
            if start not in self.merged_events:
                self.merged_events[start] = end
            else:
                self.merged_events[start] = max(self.merged_events[start], end)

        result = []
        prev_start, prev_end = None, None
        # Now we have a bunch of intervals with diff starting times but we haven't looked at intersection
        # N iterations, logn insert
        for start, end in self.merged_events.items():
            if prev_start is None:
                prev_start, prev_end = start, end
            elif start <= prev_end:
                # next interval start is within last event, merge time baby
                prev_end = max(prev_end, end)
            else:
                # it's its own thing
                result.append([prev_start, prev_end])
                prev_start, prev_end = start, end

        # we mostly leave the loop with one extra
        if prev_start is not None:
            result.append([prev_start, prev_end])

        return result
    
    # Now you want to know how many times of a time slot is booked, so you want to return the booked times of each slot.

    # For example, if [10, 20) and [15, 25) are booked, the overlap is [15, 20), it is booked twice.
    # The other fragments are booked only once. So the output will be [10, 15), once, [15, 20), twice, [20, 25), once.
    #     Example:
    # mergeTimesBooked(10, 20) => [[10, 20, 1]]
    # mergeTimesBooked(40, 50) => [[10, 20, 1], [40, 50, 1]]
    # mergeTimesBooked(20, 30) => [[10, 30, 1], [40, 50, 1]]
    # mergeTimesBooked(45, 55) => [[10, 30, 1], [40, 45, 1], [45, 50, 2], [50, 55, 1]]
    # line sweep or interval tree
    def mergeTimesBooked(self, start: int, end: int) -> list[list[int]]:
        # increment the count for the interval
        self.events_booked[start] = self.events_booked.get(start, 0) + 1
        # at this time there is one less active event
        self.events_booked[end] = self.events_booked.get(end, 0) - 1
        result = []
        active_count = 0
        prev_time = None
        for time, change in self.events_booked.items():
            if prev_time is not None and active_count > 0:
                # check last result count and last result time
                # only need to look at last result because we are going in time order
                if result and result[-1][2] == active_count and result[-1][1] == prev_time:
                    # extend the previous interval
                    result[-1][1] = time
                else:
                    result.append([prev_time, time, active_count])
            
            active_count += change
            prev_time = time
        
        return result

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

    assert c.mergeAtOnce([[10, 20], [40, 50], [20, 30], [45, 55]]) == [[10, 30], [40, 55]]

    assert c.mergeTimesBooked(10, 20) == [[10, 20, 1]]
    assert c.mergeTimesBooked(40, 50) == [[10, 20, 1], [40, 50, 1]]
    assert c.mergeTimesBooked(20, 30) == [[10, 30, 1], [40, 50, 1]]
    assert c.mergeTimesBooked(45, 55) == [[10, 30, 1], [40, 45, 1], [45, 50, 2], [50, 55, 1]]


# We’re going to be implementing a simplified air cargo booking system.
# In the system, users can create orders, and your job is to help match them according to an inventory of flights you have access to.
# To begin implementing our booking system,
# we must first determine if orders can be fulfilled. For now, each order consists of an origin and a destination.
# Given a network of flights, create a function to determine if a booking order can be satisfied (a direct flight exists between origin and destination).
# How you choose to model orders, the flights, and the network is totally up to you.
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
    assert pacificAtlantic([[1,1], [1,1], [1,1], [1,1]]) == [[0,0],[0,1],[1,0],[1,1],[2,0],[2,1],[3,0],[3,1]]

# prerequisites[i] = [ai, bi] must take bi before ai
# [0, 1] means you have to take 1 before 0
# true if you can finish, false otherwise
# canFinish(2, [[1, 0]]) = true
# canFinish(2, [[1, 0], [0, 1]])
# have to reach all numCourses
# can build an graph with adjacency list? dfs from there?
# https://leetcode.com/problems/course-schedule/
# adjacency list
def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    # Each course gets edges
    adjacency_list = [[] for _ in range(numCourses)]
    # 0, 1 0 is dest, 1 is src. can go from 1 to 0
    for dest, src in prerequisites:
        adjacency_list[src].append(dest)

    # 0 not visited, visiting, already visitied
    visited = [0] * numCourses
    def dfs(course):
        if visited[course] == 1:
            # cycle
            return False

        if visited[course] == 2:
            # visited and dfs'd from there. no cycle
            return True
        visited[course] = 1
        
        # visit all the neighbors
        for neighbor in adjacency_list[course]:
            if not dfs(neighbor):
                return False

        visited[course] = 2
        return True

    for course in range(numCourses):
        if not dfs(course):
            return False
    return True

def test_canFinish():
    assert canFinish(2, [[1, 0]]) == True
    assert canFinish(2, [[1, 0], [0, 1]]) == False

# words = ["wrt","wrf","er","ett","rftt"]
# output "wertf"
# words = ["z","x"]
# output "zx"
# Input: words = ["z","x","z"]
# ""
# the words are ordered by not in each word
# can never have a prefix after so abcd and ab is always wrong
# extract the rules
# putting the rules into a graph
# topo sorting
def alienOrder(words: list[str]) -> str:
    adj_list = defaultdict(set)
    # each unique letter to 0
    # we iteratively remove those with no incoming
    # Counter
    # fill with 0s
    in_degree = {c: 0 for word in words for c in word}

    # zip combines multiple into one iterable
    # looking for first difference between words
    for first_word, second_word in zip(words, words[1:]):
        for c, d in zip(first_word, second_word):
            if c != d:
                # c is before d
                # d has an indegree now of c
                if d not in adj_list[c]:
                    adj_list[c].add(d)
                    in_degree[d] += 1
                break
        else:  # Found no differences. Check for the prefix case
            if len(second_word) < len(first_word): return ""
    
    # pick off nodes with indegree of 0
    # bfs
    # as you pop off then check the adj list for its neigbors.
    # now that it has one less neighbor does it have no letters that have to be before it now?
    output = []
    #  Automatically provides a default value of 0 for any key that does not exist. This means you can increment a key without initializing it first.
    queue = deque([c for c in in_degree if in_degree[c] == 0])
    while queue:
        c = queue.popleft()
        output.append(c)
        for d in adj_list[c]:
            in_degree[d] -= 1
            if in_degree[d] == 0:
                queue.append(d)
    
    # if you hit here it's a cycle. Some letters never got added to queue b/c they were in each others adj list
    if len(output) < len(in_degree):
        return ""
    return "".join(output)

def test_alienOrder():
    assert alienOrder(["wrt","wrf","er","ett","rftt"]) == "wertf"
    assert alienOrder(["z","x"]) == "zx"
    assert alienOrder(["z","x","z"]) == ""


#     grid = [
#   ["1","1","1","1","0"],
#   ["1","1","0","1","0"],
#   ["1","1","0","0","0"],
#   ["0","0","0","0","0"]
# ]
# output 1
# grid = [
#   ["1","1","0","0","0"],
#   ["1","1","0","0","0"],
#   ["0","0","1","0","0"],
#   ["0","0","0","1","1"]
# ]
# output 3
# edges are water, find those surrounded by water
def numIslands(grid: list[list[str]]) -> int:
    if not grid:
        return 0

    def dfs(grid, r, c):
        if (
            r < 0
            or c < 0
            or r >= len(grid)
            or c >= len(grid[0])
            or grid[r][c] != "1"
        ):
            return
        # the secret sauce
        grid[r][c] = "0"
        # now dfs all the rest of the connecting 1s/land
        # to set to 0
        dfs(grid, r -1, c)
        dfs(grid, r + 1, c)
        dfs(grid, r, c - 1)
        dfs(grid, r, c + 1)

    num_islands = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "1":
                dfs(grid, i, j)
                num_islands += 1
        
    return num_islands

def test_numIslands():
    assert numIslands([
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
    ]) == 1
    assert numIslands([
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
    ]) == 3

## Heaps

# nums = [1,1,1,2,2,3], k = 2
# LRU with k spots?
# sort, use Counter, find k most recent?
def topKFrequent( nums: list[int], k: int) -> list[int]:
    if k == len(nums):
        return nums
    
    count = defaultdict(int)
    for num in nums:
        count[num] += 1
    # count = Counter(nums)
    # build heap where key is count
    # then you need to extract but can use this built in
    return heapq.nlargest(k, count.keys(), key=count.get)

def test_topKFrequent():
    assert topKFrequent([1,1,1,2,2,3], 2) == [1, 2]
## String

# s = "abcabcbb" 3
# s = "bbbbbb" 1
# s = "dvdf" 3
# s = "asjrgapa" 6
# move in each side while theres no repeat.
def lengthOfLongestSubstring(s: str) -> int:
    chars = Counter()

    left = right = 0
    res = 0
    while right < len(s):
        r = s[right]
        chars[r] += 1

        while chars[r] > 1:
            l = s[left]
            chars[l] -= 1
            left += 1
        res = max(res, right - left + 1)

        right += 1
    return res

def test_lengthOfLongestSubstring():
    assert lengthOfLongestSubstring("abcabcbb") == 3
    assert lengthOfLongestSubstring("bbbbb") == 1
    assert lengthOfLongestSubstring("dvdf") == 3
    assert lengthOfLongestSubstring("asjrgapa") == 6

# s = "ABAB" k = 2 4. Replace two As with Bs
# s = "AABABBA" k = 1 output 4
# Can change any character of the string and change it to any other
# can perform it at most k times
# longest subsstring containg the same letter
# O(n)
def characterReplacement(s: str, k: int) -> int:
    start = 0
    frequency_map = {}
    max_freq = 0
    longest_substring_length = 0
    for end in range(len(s)):
        frequency_map[s[end]] = frequency_map.get(s[end], 0) + 1

        max_freq = max(max_freq, frequency_map[s[end]])
        # move the start pointer towards right if current window invalid
        is_valid = (end + 1 - start - max_freq <= k)
        if not is_valid:
            frequency_map[s[start]] -= 1
            start += 1
        
        # window is valid now
        longest_substring_length = end + 1 - start
    return longest_substring_length

def test_characterReplacement():
    assert characterReplacement("ABAB", 2) == 4
    assert characterReplacement("AABABBA", 1) == 4

# strs = ["eat","tea","tan","ate","nat","bat"]
# [["bat"],["nat","tan"],["ate","eat","tea"]]
# [""] [[""]]
# strs = ["a"] [["a"]]
# strs = ["aab", "aba", "baa", "abbccc"]
# words can have repeat letters so can't just hash by letter
# could sort each word. can have tuple but not a list as key
# tuple(sorted(s)).append(s) O(NKlogK) because you have to sort. K is longest string
# hash tuples
def groupAnagrams(strs: list[str]) -> list[list[str]]:
    ans = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for c in s:
            # ord is the unicode point
            count[ord(c) - ord('a')] += 1
        # count for each letter. python hashes for us. yay python
        ans[tuple(count)].append(s)
    return list(ans.values())

def test_groupAnagrams():
    assert groupAnagrams(["eat","tea","tan","ate","nat","bat"]) == [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    assert groupAnagrams(['']) == [['']]
    assert groupAnagrams(['a']) == [['a']]
    groupAnagrams(['aab', 'aba', 'baa', 'abbccc']) == [['aab', 'aba', 'baa'], ['abbccc']]


# no stack in python so gotta add your own
def isOperatorValid(s: str) -> bool:
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}

    for char in s:
        if char in mapping:
            top = stack.pop() if stack else "#"
            if mapping[char] != top:
                return False
        else:
            stack.append(char)
            
    return not stack

def test_isOperatorValid():
    isOperatorValid("()") == True
    isOperatorValid("()[]{}") == True

# s = 'abc'
# output = 3
# s = 'aaa'
# 6
# how can we reuse palindrome calculation
# if "aba" is palindrome is "xabax"
def countSubStrings(s: str) -> int:
    n = len(s)
    ans = 0
    if n == 0:
        return 0
    # nested for loops, list comprehension
    dp = [[False for _ in range(n)] for _ in range(n)]

    # single letter
    for i in range(n):
        ans += 1
        dp[i][i] = True

    for i in range(n - 1):
        dp[i][i+1] = s[i] == s[i + 1]
        ans += dp[i][i+1]

    # 3 to nested
    # for each length check if those letters match on the ends
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = dp[i + 1][j - 1] and (s[i] == s[j])
            ans += dp[i][j]
    return ans

def test_countSubStrings():
    assert countSubStrings('aaa') == 6
    assert countSubStrings('abc') == 3

# python practice.py
if __name__ == "__main__":
    test_Spreadsheet()
    test_aircargobooker()
    test_aircargobookercost()
    test_calendar()
    test_DialerPad()
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
    test_canFinish()
    test_alienOrder()
    test_numIslands()

    # Heap
    test_topKFrequent()

    # Strings
    test_lengthOfLongestSubstring()
    test_characterReplacement()
    test_groupAnagrams()
    test_isOperatorValid()
    test_countSubStrings()
    print("All tests passed")