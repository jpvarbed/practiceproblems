import sys
from collections import deque, defaultdict, Counter # for aircargobooker & alienOrder
import heapq # for aircargobookercost
import bisect
from typing import Optional # calendar
from sortedcontainers import SortedDict # Calendar
import json # timesheet
from datetime import datetime, timedelta
import os #filestore
import shutil
from heapq import heappush, heappop

## Real life problems
class TimesheetManagementSystem:
    def __init__(self):
        self.workers = {}
        self.timesheets = {}

    def add_worker(self, worker_id, name):
        self.workers[worker_id] = name
        self.timesheets[worker_id] = []

    def clock_in(self, worker_id):
        if worker_id not in self.workers:
            raise ValueError("Worker not found")
        self.timesheets[worker_id].append({"clock_in": datetime.now(), "clock_out": None})

    def clock_out(self, worker_id):
        if worker_id not in self.workers:
            raise ValueError("Worker not found")
        if not self.timesheets[worker_id] or self.timesheets[worker_id][-1]["clock_out"]:
            raise ValueError("No active clock-in found")
        self.timesheets[worker_id][-1]["clock_out"] = datetime.now()

    def get_timesheet(self, worker_id, start_date, end_date):
        if worker_id not in self.workers:
            raise ValueError("Worker not found")
        return [entry for entry in self.timesheets[worker_id] if start_date <= entry["clock_in"].date() <= end_date]

    def calculate_hours(self, worker_id, start_date, end_date):
        timesheet = self.get_timesheet(worker_id, start_date, end_date)
        total_hours = sum((entry["clock_out"] - entry["clock_in"]).total_seconds() / 3600 for entry in timesheet if entry["clock_out"])
        return round(total_hours, 2)

    def generate_report(self, start_date, end_date):
        report = {}
        for worker_id, name in self.workers.items():
            hours = self.calculate_hours(worker_id, start_date, end_date)
            report[worker_id] = {"name": name, "hours": hours}
        return report

    def save_data(self, filename):
        data = {
            "workers": self.workers,
            "timesheets": {worker_id: [{"clock_in": entry["clock_in"].isoformat(), "clock_out": entry["clock_out"].isoformat() if entry["clock_out"] else None} for entry in timesheet]
                           for worker_id, timesheet in self.timesheets.items()}
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_data(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        self.workers = data["workers"]
        self.timesheets = {worker_id: [{"clock_in": datetime.fromisoformat(entry["clock_in"]), 
                                        "clock_out": datetime.fromisoformat(entry["clock_out"]) if entry["clock_out"] else None} 
                                       for entry in timesheet]
                           for worker_id, timesheet in data["timesheets"].items()}

def test_TimesheetManagementSystem():
    tms = TimesheetManagementSystem()
    tms.add_worker("001", "John Doe")
    tms.clock_in("001")
    tms.clock_out("001")
    start_date = datetime.now().date() - timedelta(days=7)
    end_date = datetime.now().date()
    #print(tms.calculate_hours("001", start_date, end_date))
    #print(tms.generate_report(start_date, end_date))
    tms.save_data("timesheet_data.json")
    tms.load_data("timesheet_data.json")

class FileStore:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)

    def set(self, file_name, content):
        file_path = os.path.join(self.root_dir, file_name)
        with open(file_path, 'w') as f:
            f.write(content)

    def get(self, file_name):
        file_path = os.path.join(self.root_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read()
        return None

    def filter(self, extension=None, size=None):
        filtered_files = []
        for file in os.listdir(self.root_dir):
            file_path = os.path.join(self.root_dir, file)
            if extension and not file.endswith(extension):
                continue
            if size and os.path.getsize(file_path) > size:
                continue
            filtered_files.append(file)
        return filtered_files

    def backup(self, backup_dir):
        backup_path = os.path.join(backup_dir, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        shutil.copytree(self.root_dir, backup_path)
        return backup_path

    def restore(self, backup_path):
        shutil.rmtree(self.root_dir)
        shutil.copytree(backup_path, self.root_dir)

def test_FileStore():
    file_store = FileStore("./file_store")
    file_store.set("example.txt", "Hello, World!")
    #print(file_store.get("example.txt"))
    #print(file_store.filter(extension=".txt"))
    backup_path = file_store.backup("./backups")
    file_store.restore(backup_path)

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

# priority queue. heapq mini ue
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
# check each direction in grid
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
# build graph and dfs
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
# topological sorting
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
# dynamic programming
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

# interview bit
# @param A : tuple of integers
# @param B : tuple of integers
# @return an integer
# greedy algorithm means can know best at each step
# https://www.interviewbit.com/problems/gas-station/
def canCompleteCircuit(A: int, B: int) -> int:
    if sum(A) < sum(B):
        return -1
        
    total_gas = 0
    current_gas = 0
    start_index = 0
    for i in range(len(A)):
        total_gas += A[i] - B[i]
        current_gas += A[i] - B[i]
        if current_gas < 0:
            start_index = i + 1
            current_gas = 0
    return start_index if total_gas >= 0 else -1

def test_canCompleteCircuit():
    assert canCompleteCircuit([1,2], [2,1]) == 1


class ListNode:
	def __init__(self, x):
		self.val = x
		self.next = None

# @param A : head node of linked list
# @param B : head node of linked list
# @return the head node in the linked list
# stored in reverse order
# 2->4->3 + 5 6 4
# 342 + 465 = 807
# output 7 -> 0 -> 8 not 7 0 8 0
# first is my implementation and then second is the faster one from chatgpt
# https://www.interviewbit.com/problems/add-two-numbers-as-lists/
def addTwoNumbers(A: ListNode, B: ListNode) -> ListNode:
    # numA = 0
    # numB = 0
    # def countList(num: ListNode) -> int:
    # 	result = 0
    # 	mult = 1
    # 	while num is not None:
    # 		result += num.val * mult
    # 		mult *= 10
    # 		num = num.next
    # 	return result
        
    # numToReturn = countList(A) + countList(B)
    
    # result = ListNode(numToReturn % 10)
    # cur_node = result
    # numToReturn //= 10
    # while numToReturn > 0:
    # 	nextNum = numToReturn % 10
    # 	next_node = ListNode(nextNum)
    # 	cur_node.next = next_node
    # 	cur_node = next_node
    # 	numToReturn //= 10

    # return result
    dummy = ListNode(0)
    current = dummy
    carry = 0
    
    while A is not None or B is not None or carry != 0:
        sum = carry
        if A is not None:
            sum += A.val
            A = A.next
        if B is not None:
            sum += B.val
            B = B.next
        
        carry = sum // 10
        current.next = ListNode(sum % 10)
        current = current.next
    
    return dummy.next

def test_addTwoNumbers():
    A = ListNode(2)
    A.next = ListNode(4)
    A.next.next = ListNode(3)

    B = ListNode(5)
    B.next = ListNode(6)
    B.next.next = ListNode(4)
    assert addTwoNumbers(A, B).val == 7


# @param A : list of list of integers
# @return the same list modified
# NxN
# turn row into column
# https://www.interviewbit.com/problems/rotate-matrix/
def rotateArray(A: list[list[int]]) -> list[list[int]]:
    N = len(A)
    # i is row
    for i in range(N):
        # j is column. swap starting from diagonal
        for j in range(i, N):
            A[i][j], A[j][i] = A[j][i], A[i][j]
    for i in range(N):
        A[i].reverse()
    return A

def test_rotateArray():
    matrix1 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    expected1 = [
        [7, 4, 1],
        [8, 5, 2],
        [9, 6, 3]
    ]
    result1 = rotateArray(matrix1)
    assert result1 == expected1, f"Test case 1 failed: {result1}"

# https://www.interviewbit.com/problems/diffk-ii/
def diffPossible(A: list[int], B: int):
        numMap = set()
        n = len(A)
        for i in range(n):
            if A[i] - B in numMap or B + A[i] in numMap:
                return 1
            numMap.add(A[i])
        return 0

def test_diffPossible():
    assert diffPossible([1, 5, 3], 2) == 1
    assert diffPossible([2, 4, 3], 3) == 0

# @param A : integer
# @return a list of strings
# sorted list of all possible parenthesis
# for each set add () and then inside
# ()
# ()() (())
# ()()() (())() (())() ()(()) ((()))
def generateParenthesis(A: int):
    if A == 0:
        return [""]
    if A == 1:
        return ["()"]
    
    result = set()
    for s in generateParenthesis(A - 1):
        for i in range(len(s)):
            if s[i] == '(':
                #including ith character
                result.add(s[:i + 1] + "()" + s[i + 1:])
        result.add("()" + s)
    return sorted(result)
    # result = []
    # stack = [("(", 1, 0)]  # (current_string, open_count, close_count)
        
    #     while stack:
    #         current, open_count, close_count = stack.pop()
            
    #         if open_count == A and close_count == A:
    #             result.append(current)
            
    #         if open_count < A:
    #             stack.append((current + "(", open_count + 1, close_count))
            
    #         if close_count < open_count:
    #             stack.append((current + ")", open_count, close_count + 1))
        
    #     return sorted(result)
def test_generateParenthesis():
    assert generateParenthesis(3) == [ "((()))", "(()())", "(())()", "()(())", "()()()" ]

# @param A : root node of tree
# @param B : integer
# @param C : integer
# @return an integer
# has both v and w as descendants
# no guarantee they exist
# no dupe values
# dfs and then??
# least common ancestor
# https://www.interviewbit.com/problems/least-common-ancestor/discussion/p/extra-find-functions-before-you-call-actual-lca-logic-is-required-for-this-question/348642/802/
class TreeNode:
	def __init__(self, x):
		self.val = x
		self.left = None
		self.right = None

def lca(A, B, C):
    def dfs(node):
        if node is None:
            return None
        if node.val == B or node.val == C:
            return node
        
        left_lca = dfs(node.left)
        right_lca = dfs(node.right)
        
        if left_lca and right_lca:
            return node
        
        return left_lca if left_lca else right_lca
    
    def exists(node, val):
        if node is None:
            return False
        if node.val == val:
            return True
        return exists(node.left, val) or exists(node.right, val)
    
    if not exists(A, B) or not exists(A, C):
        return -1
    
    lca_node = dfs(A)
    if lca_node:
        return lca_node.val
    return -1

def test_lca():
    root = TreeNode(3)
    root.left = TreeNode(5)
    root.right = TreeNode(1)
    root.left.left = TreeNode(6)
    root.left.right = TreeNode(2)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(8)
    root.left.right.left = TreeNode(7)
    root.left.right.right = TreeNode(4)
        
    assert lca(root, 5, 1) == 3

# @param A : integer
# @return a strings
# 3999 >= A >= 1
def intToRoman(A: int) -> str:
    result = ""
    values = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]
    
    for value, numeral in values:
        while A >= value:
            A -= value
            result += numeral
    
    return result

def test_intToRoman():
    assert intToRoman(14) == "XIV"

# @param A : list of integers
# @return A after the sort
# 0 1 2 are red white blue
# order read white blue so 0 first then 1 then 2
# could count them and then just spit it out
# https://www.interviewbit.com/problems/sort-by-color/
def sortColors(A: list[int]) -> list[int]:
    low, mid, high = 0, 0, len(A) - 1
    while mid <= high:
        if A[mid] == 0:
            # swap to low
            A[low], A[mid] = A[mid], A[low]
            low += 1
            mid += 1
        elif A[mid] == 1:
            mid += 1
        else:
            A[mid], A[high] = A[high], A[mid]
            high -= 1
    return A

def test_sortColors():
    assert sortColors([0, 1, 2, 0, 1, 2]) == [0, 0, 1, 1, 2, 2]

# @param A : root node of tree
# @return an integer
# max depth of binary tree
# dfs and keep track of depth?
# https://www.interviewbit.com/problems/max-depth-of-binary-tree/
def maxDepth(A):
    def dfs(A):
        if A is None:
            return 0
        return 1 + max(dfs(A.left), dfs(A.right))
    return dfs(A)

def test_maxDepth():
    node = TreeNode(1)
    # Create a binary tree:
    #      1
    #     / \
    #    2   3
    #   / \   \
    #  4   5   6
    node = TreeNode(1)
    node.left = TreeNode(2)
    node.right = TreeNode(3)
    node.left.left = TreeNode(4)
    node.left.right = TreeNode(5)
    node.right.right = TreeNode(6)
    
    assert maxDepth(node) == 3
     
# @param A : list of integers
# @param B : integer
# @return an integer
# A array size of N. b is integer target of sum
# do twosum for each
# get closest to B. not necessarily equal
# https://www.interviewbit.com/problems/3-sum/
def threeSumClosest(A: list[int], B: int) -> int:
    A.sort()
    n = len(A)
    closest_sum = float('inf')

    # O(n^2) is kinda weak sauce
    # but you do have to do all the comparisons
    for i in range(n-2):
        left, right = i + 1, n -1
        while left < right:
            current_sum = A[i] + A[left] + A[right]
            if abs(current_sum - B) < abs(closest_sum - B):
                closest_sum = current_sum
                
            if current_sum < B:
                left += 1
            elif current_sum > B:
                right -= 1
            else:
                return closest_sum
    return closest_sum

def test_threeSumClosest():
    A = [-1, 2, 1, -4]
    B = 1
    assert threeSumClosest(A, B) == 2


# @param A : list of integers
# @return a list of list of integers
# all permutations. integer array of size N
# 2-d array all possible unique permutations
# numbers might contain duplicates
# https://www.interviewbit.com/problems/all-unique-permutations/
def permute(A: list[int]) -> list[list[int]]:
    def backtrack(start):
        if start == len(A):
            result.append(A[:])
            return
        seen = set()
        for i in range(start, len(A)):
            if A[i] not in seen:
                seen.add(A[i])
                # put cur element at start and backtrack
                A[start], A[i] = A[i], A[start]
                backtrack(start + 1)
                A[start], A[i] = A[i], A[start]
    result = []
    # get dupes together
    A.sort()
    backtrack(0)
    return result

def test_permute():
    assert permute([1, 1, 2]) == [[1, 1, 2], [1, 2, 1], [2, 1, 1]]

# @param A : list of integers
# @param B : integer
# @return a list of list of integers
# elements must be in non-descending order
# combos in sorted in ascending order
# comboA > comboB a1>b1 
# solution must not contain dupes
# may choose from A unlimited number of times
# https://www.interviewbit.com/problems/combination-sum/
def combinationSum(A: list[int], B: int) -> list[list[int]]:
    def backtrack(start, path, target):
        if target == 0:
            result.append(path[:])
            return
        elif target < 0:
            return
        
        for i in range(start, len(A)):
            # skip dupes
            if i > start and A[i] == A[i - 1]:
                continue
            path.append(A[i])
            # we can re-use i so we keep slamming on it until we reach there
            # or go too far. you then backtrack once you went too far
            # and try the next elt.
            # you append/pop each attempt
            backtrack(i, path, target - A[i])
            path.pop()
            
    A.sort()
    result = []
    backtrack(0, [], B)
    return result

# @param A : tuple of integers
# @param B : tuple of integers
# @param C : tuple of integers
# @return an integer
# find i jk such that max(abs(A[i] - B[i]), abs[B[j]- C[k], abs[C[k] - A[i]]]) is min
# return that min
# 3 arrays, one index per arrays
# arrays are sorted
# https://www.interviewbit.com/problems/array-3-pointers
def minimizeDiff(A, B, C):
    # go through all of A. binary search for element just smaller than or equal in b and c. note the diff
    # repeat for b and c
    i,j,k = 0,0,0
    min_diff = float('inf')
    while i < len(A) and j < len(B) and k < len(C):
        max_val = max(A[i], B[j], C[k])
        min_val = min(A[i], B[j], C[k])
        
        min_diff = min(min_diff, max_val - min_val)
        if min_val == A[i]:
            i += 1
        elif min_val == B[j]:
            j += 1
        else:
            k += 1
    return min_diff

def test_minimizeDiff():
    assert minimizeDiff((1, 4, 10), (2, 15, 20), (10, 12))

# LRU least recently used cache
# some capacity N
# get(key)
# put(key, value)
# total order of last used.
# keep sort order but always inserting at the front
# find the thing that is was just used and put that at the front. random access
# oldest is just the front 
# list, array or linked list. store pointer to the list element and update that
# map to get O(1) key -> value, list to get ordering, map has key -> list node to update in O(1)
class LRUNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

# will have any problems with key 0 in the head
class LRU:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {} # key -> node
        # useful to always have the front and back pointers
        # for access
        self.head = LRUNode(0, 0)
        self.tail = LRUNode(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        # update all the pointers to skip this one
        prev = node.prev
        next = node.next
        # make the prev and next look at eachother instead of node
        prev.next = next
        next.prev = prev

    def _add(self, node):
        # put it in the list right after head
        # update the head, node and next pts to each other
        # next is current 'first'
        # slide in between head and current next
        next = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = next
        next.prev = node
        
    # get item if there, update LRU calculation
    # O(1) check, remove O(1), add O(1) O(1)
    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            # move to front
            self._remove(node)
            self._add(node)
            return node.value
        return -1
    
    # store item, update LRU calculation
    # remove, add, remove, delete, insert into hash map O(1) O(1)
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = LRUNode(key, value)
        self._add(node)
        self.cache[key] = node
        # check capacity and remove least recent
        if len(self.cache) > self.cap:
            lru = self.tail.prev
            self._remove(node)
            del self.cache[lru.key]
        return None

def test_LRU():
    cache = LRU(2)
    # check for key 0
    assert cache.get(0) == -1
    cache.put(1,1)
    cache.put(2,2)
    assert cache.get(1) == 1
    cache.put(3,3)
    assert cache.get(2) == -1

# computes the number of trailing zeros in n!
# trailing zeros
# 1! = 1
# 2! = 2
# 3! = 6
# 4! = 24
# 5! = 120
# 6! = 720
# 7! = 5040
# 8! = 40320
# 9! = 362880
# 10! = 3628800
# is there some trick to
def countZerosInNFact(n: int) -> int:
    # compute factorial, get the number of zeros
    # O(N) factorials
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        else:
            return n * factorial(n - 1)
    fact_result = factorial(n)
    # get trailing zeros
    # go from 1 to log10(result), while % 10 == 0 count ++, stop when not zero
    result = 0
    # result of the factorial is log(N)
    while fact_result > 1:
        if fact_result % 10 == 0:
            result += 1
            fact_result //= 10
        else:
            break
    return result

# can we do this without calculating the factorial
# when can you end in a zero. for every 10 you end up with a zero. when you had an even and a 5
# for every 5 and 10 you get a zero
# for n, how many times would you multiply by 10 and how many times would you multiply by 5
# more 2s factors of 5s are the limiting factor. 
# every divisible by 5 is a 0. always a matching 2 for that 5
# number of 5 factors in 25 is 2
# O(log5(N))
def countZerosInNFactClever(n: int) -> int:
    result = 0
    # result of the factorial is log10 logN ~ N
    while n > 0:
        n //= 5
        result += n
    return result

def test_countZerosInNFact():
    assert countZerosInNFact(1) == 0
    assert countZerosInNFactClever(100) == 24

# 10! 0 -> 10 how many of those have at least one 5 factor in them
# 5 - 1
# 10 - 2 (10 & 5)
# 15 - (15, 10, 5) 3
# 20 - 4 (20, 15, 10, 5) 4
# 25 - 6 (25 - 2, 20, 15, 10, 5) 25 /25 = 1*2 =2 25 / 5= 5 -1
# 25 / 5 = 5 with single factor
# 25 / 25 = 1 with double factor
# 75 / 5 = 25 with single factor
# 75 / 25 = 3 with double factor + 1
# 625 / 5 = 125
# 625 / 25 = 25
# 625 / 125 = 5
# 625 / 625 = 1
# 125 + 25 + 5 + 1
# 0 -n 25, 75, 50, multiples of 25, then its powers of 5 //
# 75 75 /25 = 3 * 2. divide our n by 5. get first order
# 75 / 5 = 25
# log5(N) = max power of 5
# for that power of 5 to 1 divide to get the number of factors
# the factors are the power * the remainder
def numberOfFactorialMembersFactorFive(n: int) -> int:
    result = 0
    i = 5
    while n >= i:
        result += n // i
        i *= 5
    return result

def test_numberOfFactorialMembersFactorFive():
    assert numberOfFactorialMembersFactorFive(3) == 0
    assert numberOfFactorialMembersFactorFive(625) == 156

# Syntax: Generator expressions use parentheses () instead of square brackets [].
# Lazy Evaluation: They generate values on-the-fly, only when needed.
# Memory Efficiency: They don't store all values in memory at once.
# Single-Use Iteration: Once exhausted, they can't be reused without recreation.
def test_generatorExpressions():
    # generator is a separate object than a list. its like an iterator but the memory isnt allocated yet
    # (map_fcn for var in range <optional condition>)
    squares = (x**2 for x in range(1, 11))
    print(list(squares))  # Convert to list to see all values

    even_numbers = (x for x in range(1, 21) if x % 2 == 0)
    print(list(even_numbers))

    words = ['hello', 'world', 'python', 'generator']
    uppercase_words = (words.upper() for word in words)
    print(list(uppercase_words))

    my_dict = {'a': 1, 'b': 7, 'c': 3, 'd': 12, 'e': 5}
    filtered_keys = (key for key, value in my_dict.items() if value > 5)
    print(list(filtered_keys))

    nested_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = (item for sublist in nested_list for item in sublist)
    print(list(flattened))

    with open('example.txt', 'r') as file:
        lines_with_python = (line.strip() for line in file if 'python' in line.lower())
        for line in lines_with_python:
            print(line)

# facebook coding
def has_contiguous_sequence(seq, total):
    prefix_sum_map = {}
    current_sum = 0

    for index, num in enumerate(seq):
        current_sum += num

        # If current_sum is equal to the target, we found a subarray
        if current_sum == total:
            return True

        # If (current_sum - total) exists in the map, it means there is a subarray
        # that sums to the target
        if (current_sum - total) in prefix_sum_map:
            return True

        # Store the current_sum in the map
        prefix_sum_map[current_sum] = index

    return False

def findKthLargest(arr, K):
    # Initialize a min-heap
    min_heap = []
    
    # Iterate over each element in the array
    for num in arr:
        heapq.heappush(min_heap, num)
        
        # If heap size exceeds K+1, remove the smallest element
        if len(min_heap) > K + 1:
            heapq.heappop(min_heap)
    
    # The smallest element in the heap is the Kth largest element
    return heapq.heappop(min_heap)

# amazon leet code
# https://leetcode.com/problems/sort-array-by-increasing-frequency
def frequencySort(nums: list[int]) -> list[int]:
    # could count all the frequencies
    counter = Counter(nums)
    # first sort by counter[x]
    # criterion in order by comma
    nums.sort(key=lambda x: (counter[x], -x))
    return nums

def test_frequencySort():
    assert frequencySort([1,1,2,2,2,3]) == [3,1,1,2,2,2]

# can put any number as long as does not exceed truck size
# number of boxes, number of units for each box type
# return number of units
# https://leetcode.com/problems/maximum-units-on-a-truck/
def maximumUnits(boxTypes: list[list[int]], truckSize: int) -> int:
    # now sorted by frequency
    boxTypes.sort(key = lambda x: (x[1]))
    maxUnits = 0
    while truckSize > 0 and boxTypes:
        most = boxTypes.pop()
        if truckSize >= most[0]:
            truckSize -= most[0]
            maxUnits += most[0] * most[1]
        else:
            maxUnits += most[1] * truckSize
            return maxUnits        
    return maxUnits

def test_maximumUnits():
    assert maximumUnits([[1,3],[2,2],[3,1]], 4) == 8

# https://leetcode.com/problems/make-array-zero-by-subtracting-equal-amounts/description/
def minimumOperations(nums: list[int]) -> int:
    # unique_non_zero_elements = {num for num in nums if num > 0}
    counter = Counter(nums)
    ans = 0
    for count in counter.keys():
        if count >= 1:
            ans += 1
    return ans

def test_minimumOperations():
    assert minimumOperations([1,5,0,3,5]) == 3

# https://leetcode.com/problems/design-parking-system/
class ParkingSystem:
    # car can only part in space of its type
    def __init__(self, big: int, medium: int, small: int):
        self.big = big
        self.medium = medium
        self.small = small
        # self.empty = [big, medium, small]

    def addCar(self, carType: int) -> bool:
        # if self.empty[carType - 1] > 0:
        #     self.empty[carType - 1] -= 1
        #     return True
        if carType == 3 and self.small > 0:
            self.small -= 1
            return True
        elif carType == 2 and self.medium > 0:
            self.medium -= 1
            return True
        elif carType == 1 and self.big > 0:
            self.big -= 1
            return True
        return False

class RandomNode:
    def __init__(self, x: int, next: 'RandomNode' = None, random: 'RandomNode' = None):
        self.val = int(x)
        self.next = next
        self.random = random
    
# https://leetcode.com/problems/copy-list-with-random-pointer
def copyRandomList(head: 'Optional[RandomNode]') -> 'Optional[RandomNode]':
    if head is None:
        return head
    # need to update the random values. can use a map
    # insert nodes in middle, then update next and random around them
    curr = head
    while curr:
        new_node = RandomNode(curr.val)
        new_node.next = curr.next
        curr.next = new_node
        curr = new_node.next

    curr = head
    # update the randoms
    while curr:
        if curr.random:
            curr.next.random = curr.random.next
        # skip 2
        curr = curr.next.next

    # delete the olds
    new_head = head.next
    # where we about to delete
    curr_old = head
    # what we keeping
    curr_new = new_head
    while curr_old:
        curr_old.next = curr_new.next
        curr_old = curr_old.next
        if curr_old:
            curr_new.next = curr_old.next
            curr_new = curr_new.next
    return new_head

def test_copyRandomList():
    nodes = [RandomNode(7), RandomNode(13), RandomNode(11), RandomNode(10), RandomNode(1)]
    
    # Set up next pointers
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    
    # Set up random pointers
    nodes[1].random = nodes[0]
    nodes[2].random = nodes[4]
    nodes[3].random = nodes[2]
    nodes[4].random = nodes[0]

    # Get the head of the original list
    head = nodes[0]
    copied_head = copyRandomList(head)
    assert copied_head.val == 7

# https://leetcode.com/problems/meeting-rooms-ii/
def minMeetingRooms(intervals: list[list[int]]) -> int:
    intervals.sort(key= lambda x: (x[0], x[1]))
    # go through each start
    # find max size of heap
    room_heap = []
    max_size = 0
    for start, end in intervals:
        while room_heap and start >= room_heap[0]:
            heappop(room_heap)
        heappush(room_heap, (end))
        max_size = max(max_size, len(room_heap))
    return max_size

def test_minMeetingRooms():
    assert minMeetingRooms([[0,30],[5,10],[15,20]]) == 2
    assert minMeetingRooms([[1,13], [13, 15]]) == 1

# https://leetcode.com/problems/design-tic-tac-toe/
class TicTacToe:
    # trade space so move can be done in O(1)
    # diag and anti_diagonal
    # assumed to be valid
    # keep track of whole board
    # n marks not 3 omg
    def __init__(self, n: int):
        self.n = n
        self.rows = [0 for _ in range(n)]
        self.cols = [0 for _ in range(n)]
        self.diag = 0
        self.antiDiag = 0
        return

    def move(self, row: int, col: int, player: int) -> int:
        current = 1 if player == 1 else -1
        
        self.rows[row] += current
        self.cols[col] += current
        if row == col:
            self.diag += current

        if row + col == self.n - 1:
            self.antiDiag += current
        
        if abs(self.rows[row]) == self.n or \
            abs(self.cols[col]) == self.n or \
            abs(self.diag) == self.n or \
            abs(self.antiDiag) == self.n:
            return player
        return 0

# https://leetcode.com/problems/reorganize-string/
# no two characters are the same
# or "" if not possible
# alternate most common letters?
def reorganizeString(s: str) -> str:
        char_counts = Counter(s)
        max_heap = [(-count, char) for char, count in char_counts.items()]
        heapq.heapify(max_heap)

        result = []
        while len(max_heap) >= 2:
            count1, char1 = heapq.heappop(max_heap)
            count2, char2 = heapq.heappop(max_heap)
            result.extend([char1, char2])

            if count1 + 1 < 0:
                heapq.heappush(max_heap, (count1 +1, char1))
            if count2 + 1 < 0:
                heapq.heappush(max_heap, (count2 + 1, char2))

        if max_heap:
            # how many leftover
            count, char = heapq.heappop(max_heap)
            if -count > 1:
                return ""
            result.append(char)
        return ''.join(result)

def test_reorganizeString():
    assert reorganizeString("aab") == "aba"

    # mx n grid but can snake around
    # dfs around
def wordSearchExist(board: list[list[str]], word: str) -> bool:
    if not board or not word:
        return False

    rows, cols = len(board), len(board[0])

    def dfs(r, c, idx):
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[idx]:
            return False

        temp = board[r][c]
        board[r][c] = '#'

        found = (dfs(r + 1, c, idx + 1) or
                dfs(r - 1, c, idx+1) or
                dfs(r, c + 1, idx + 1) or
                dfs(r, c - 1, idx + 1))

        board[r][c] = temp
        return found

    for i in range(rows):
        for j in range(cols):
            if board[i][j] == word[0] and dfs(i, j, 0):
                return True
    return False

def test_wordSearchExist():
    assert wordSearchExist([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "SEE") == True
    assert wordSearchExist([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCB") == False

# leetcode.com/problems/move-zeroes
# in place
def moveZeroes(nums: list[int]) -> None:
    """
    Do not return anything, modify nums in-place instead.
    """
    nonzero = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[i], nums[nonzero] = 0, nums[i]
            nonzero += 1
    pass

def test_moveZeros():
    test = [0, 1, 0, 3, 12] 
    moveZeroes(test)
    assert test == [1, 3, 12, 0, 0]


# https://leetcode.com/problems/merge-sorted-array
# two pointer
def mergeSortedArrays(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        p1 = m - 1
        p2 = n - 1

        for p in range(m + n -1, -1, -1):
            if p2 < 0:
                break
            if p1 >= 0 and nums1[p1] > nums2[p2]:
                nums1[p] = nums1[p1]
                p1 -= 1
            else:
                nums1[p] = nums2[p2]
                p2 -= 1

def test_mergeSortedArrays():
    mergeSortedArrays([1,2,3,0,0,0], 3, [2,5,6], 3)

# https://leetcode.com/problems/valid-palindrome-ii
def moveLetterPalindrome(s: str) -> bool:
    def isPalindrome(s, i, j):
        while i <j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return isPalindrome(s, i, j - 1) or isPalindrome(s, i + 1, j)
        i += 1
        j -= 1
    return True

def test_moveLetterPalindrome():
    assert moveLetterPalindrome('aba') == True
    assert moveLetterPalindrome('abca') == True
    assert moveLetterPalindrome('abc') == False

# bin search. isbadversion is a provided api
# https://leetcode.com/problems/first-bad-version
def firstBadVersion(n: int) -> int:
    # bin search
    low = 1
    high = n
    while low < high:
        mid = low + (high - low) // 2
        if isBadVersion(mid):
            high = mid
        else:
            low = mid + 1
    return low

# 1 2 0 0
# 3 4
# 1 2 3 4
# 2 1 5
# 8 0 6
# = 1 0 2 1
# https://leetcode.com/problems/add-to-array-form-of-integer
def addToArrayForm(num: list[int], k: int) -> list[int]:
    tens = 1
    full = 0
    for digit in reversed(num):
        full += digit * tens
        tens *= 10
    
    sum = full + k
    ans = []
    while sum > 0:
        ans.append(sum % 10)
        sum //= 10
    return reversed(ans)

# replace . with [.]
def defangIPaddr(address: str) -> str:
    return address.replace('.', '[.]')

# https://leetcode.com/problems/sum-of-unique-elements
def sumOfUnique(nums: list[int]) -> int:
    unique = defaultdict(int)
    sum = 0
    for num in nums:
        unique[num] += 1

    for key, val in unique.items():
        if val == 1:
            sum += key
    return sum

def test_sumOfUnique():
    assert sumOfUnique([1,2,3,2]) == 4
    assert sumOfUnique([1,2,3,4,5]) == 15
    assert sumOfUnique([1,1,1,1,1]) == 0

# ans[i] = nums[nums[i]]
# https://leetcode.com/problems/build-array-from-permutation
# could multiply by q and not use extra space
def buildArray(nums: list[int]) -> list[int]:
    ans = [0 for i in range(len(nums))]
    for i in range(len(nums)):
        ans[i] = nums[nums[i]]
    return ans

# item = type, color, name
# rule key and rule value
# https://leetcode.com/problems/count-items-matching-a-rule
def countMatches(items: list[list[str]], ruleKey: str, ruleValue: str) -> int:
    count = 0
    for type, color, name in items:
        if ruleKey == 'type' and ruleValue == type:
            count += 1
        elif ruleKey == 'color' and ruleValue == color:
            count += 1
        elif ruleKey == 'name' and ruleValue == name:
            count += 1
    return count

    # powers of 26
    # ZY is 701
def convertToTitle(columnNumber: int) -> str:
    result = []
    while columnNumber > 0:
        # zero indexed
        columnNumber -= 1
        result.append(chr(columnNumber % 26 + ord('A')))
        columnNumber //= 26
    return ''.join(result[::-1])

# https://leetcode.com/problems/longest-common-prefix
def longestCommonPrefix(strs: list[str]) -> str:
    if not strs:
        return ""
    for i in range(len(strs[0])):
        c = strs[0][i]
        for j in range(1, len(strs)):
            if i == len(strs[j]) or strs[j][i] != c:
                # if we find 0 matches we return string 0 to 0
                return strs[0][0:i]
    return strs[0]

def test_longestCommonPrefix():
    assert longestCommonPrefix(["flower","flow","flight"]) == "fl"
    assert longestCommonPrefix(["dog","racecar","car"]) == ""

# https://leetcode.com/problems/merge-two-sorted-lists
def mergeTwoLists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    prehead = ListNode(-1)
    prev = prehead
    while list1 and list2:
        if list1.val < list2.val:
            prev.next = list1
            list1 = list1.next
        else:
            prev.next = list2
            list2 = list2.next
        prev = prev.next
    prev.next = list1 if list1 is not None else list2
    return prehead.next

 # intersect at a val or 0 if no intersection
# easy way store, set each val, once you find intersection you then go back and iterate until you find that val
# how to preserve order
# you can just look at the shorter list
# https://leetcode.com/problems/intersection-of-two-linked-lists
def getIntersectionNode(headA: ListNode, headB: ListNode) -> Optional[ListNode]:
    pA = headA
    pB = headB
    # one goes through shorter and one through longer and they line up
    # this is a bit fancy. could just start at diff in longer list
    while pA != pB:
        pA = headB if pA is None else pA.next
        pB = headA if pB is None else pB.next

    return pA

def max_words_packed(board, dictionary):
    directions = [(0,1), (1,0), (0, -1), (-1, 0)] #right left up down
    def dfs(used, words_packed):
        nonlocal max_packed
        max_packed = max(max_packed, len(words_packed))
        print(f"words {words_packed}")
        for word in dictionary:
            if word in words_packed:
                continue
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if can_place_word(board, word, i ,j, used, set()):
                        new_used = used | set((i, j) for i, j in word_positions)
                        dfs(new_used, words_packed + [word])

    # check if its fits
    # see if you can make your way through the board
    def can_place_word(board, word, i, j, used, current_path):
        # track path
        if len(current_path) == len(word):
            global word_positions
            word_positions = current_path
            return True
        # all that work
        if (i < 0 or i>= len(board) or j < 0 or j >= len(board[0]) or
            (i,j) in used or (i, j) in current_path or
            board[i][j] != word[len(current_path)]):
            return False
        if len(used) > 0 or len(current_path) > 0:
            print(f"used {used} path{current_path}")

        current_path.add((i, j))
        for di, dj in directions:
            if can_place_word(board, word, i + di, j+ dj, used, current_path):
                return True
        current_path.remove((i, j))
        return False

    max_packed = 0
    word_positions= set()
    dfs(set(), [])
    return max_packed

def test_max_words_packed():
    board = [
        ['E', 'N', 'P'],
        ['G', 'S', 'C'],
        ['O', 'N', 'S']
    ]
    dictionary = ['EGO', 'EGOS', 'EGONS', 'SNO', 'SONGS', 'NC', 'SNS', 'P']
    result = max_words_packed(board, dictionary)
    print(result)
    assert result == 3



# python practice.py
if __name__ == "__main__":
    test_FileStore()
    test_TimesheetManagementSystem()
    test_Spreadsheet()
    test_aircargobooker()
    test_aircargobookercost()
    test_calendar()
    test_DialerPad()

    #test_generatorExpressions()
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

    # interview bit
    test_canCompleteCircuit()
    test_addTwoNumbers()
    test_rotateArray()
    test_diffPossible()
    test_generateParenthesis()
    test_intToRoman()
    test_sortColors()
    test_maxDepth()
    test_threeSumClosest()
    test_permute()
    test_minimizeDiff()

    # practice
    test_LRU()
    test_countZerosInNFact()
    test_numberOfFactorialMembersFactorFive()

    # amazon leet code
    test_frequencySort()
    test_maximumUnits()
    test_minimumOperations()
    test_copyRandomList()
    test_minMeetingRooms()
    test_reorganizeString()
    test_wordSearchExist()
    test_moveZeros()
    test_mergeSortedArrays()
    test_moveLetterPalindrome()
    test_sumOfUnique()
    test_longestCommonPrefix()

    test_max_words_packed()

    # concurency
    print("All tests passed")
