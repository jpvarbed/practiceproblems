import asyncio
# concurrency
from threading import Lock, Thread, Semaphore, Barrier
import threading
import time
import unittest
from io import StringIO
import sys
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, wait

# https://leetcode.com/problems/print-in-order/
# https://leetcode.com/problemset/concurrency/
class Foo:
    """Test doc string"""
    def __init__(self):
        self.firstJobDone = Lock()
        self.secondJobDone = Lock()
        self.firstJobDone.acquire()
        self.secondJobDone.acquire()


    def first(self, printFirst: 'Callable[[], None]') -> None: 
        # printFirst() outputs "first". Do not change or remove this line.
        printFirst()
        self.firstJobDone.release()


    def second(self, printSecond: 'Callable[[], None]') -> None: 
        # printSecond() outputs "second". Do not change or remove this line.
        with self.firstJobDone:
            printSecond()
        self.secondJobDone.release()


    def third(self, printThird: 'Callable[[], None]') -> None:
        # printThird() outputs "third". Do not change or remove this line.
        with self.secondJobDone:
            printThird()

def test_withasyncio():
    async def fetch_data(name):
        print(f"{name}: Starting to fetch data")
        await asyncio.sleep(2)  # Simulate an I/O operation
        print(f"{name}: Finished fetching data")
        return f"{name} data"

    async def main():
        tasks = [
            asyncio.create_task(fetch_data("A")),
            asyncio.create_task(fetch_data("B")),
            asyncio.create_task(fetch_data("C"))
        ]
        results = await asyncio.gather(*tasks)
        print(f"All tasks completed. Results: {results}")

    # Run the main coroutine
    asyncio.run(main())

# modern code uses async/await
# In a generator or simple coroutine, yield does two things:

# It pauses the function and returns a value (if specified).
# It waits for the next call to send() or next() before resuming.
def test_simple_coroutine():
    def simple_coroutine():
        print("Coroutine started")
        x = yield
        print(f"Received: {x}")
        y = yield
        print(f"Received: {y}")

    # Create the coroutine
    co = simple_coroutine()

    # Start the coroutine
    next(co)

    # Send values to the coroutine
    co.send(10)
    co.send(20)



def test_threading():
    def worker(name):
        print(f"Worker {name} starting")
        time.sleep(2)  # Simulate some work
        print(f"Worker {name} finished")

    # Create and start 3 threads
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(f"Thread-{i}",))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    print("All workers finished")


# https://leetcode.com/problems/print-foobar-alternately/
class FooBar:
    def __init__(self, n):
        self.n = n
        self.foo_event = threading.Event()
        self.bar_event = threading.Event()
        self.foo_event.set()


    def foo(self, printFoo: 'Callable[[], None]') -> None:
        
        for i in range(self.n):
            
            # printFoo() outputs "foo". Do not change or remove this line.
            self.foo_event.wait()
            printFoo()
            self.foo_event.clear()
            self.bar_event.set()


    def bar(self, printBar: 'Callable[[], None]') -> None:
        
        for i in range(self.n):
            
            # printBar() outputs "bar". Do not change or remove this line.
            self.bar_event.wait()
            printBar()
            self.bar_event.clear()
            self.foo_event.set()
# 01020304 for n = 4
class ZeroEvenOdd:
    def __init__(self, n):
        self.n = n
        self.zero_lock = Lock()
        self.nonzero_lock = Lock()
        self.even_lock = Lock()
        self.odd_lock = Lock()
        self.nonzero_lock = Lock()
        self.nonzero_lock.acquire()
        self.even_lock.acquire()
        
        
	# printNumber(x) outputs "x", where x is an integer.
    def zero(self, printNumber: 'Callable[[int], None]') -> None:
        for _ in range(self.n):
            self.zero_lock.acquire()
            printNumber(0)
            self.nonzero_lock.release()
        
        
    def even(self, printNumber: 'Callable[[int], None]') -> None:
        for i in range(self.n + 1):
            if i % 2 == 0 and i != 0:
                self.even_lock.acquire()
                self.nonzero_lock.acquire()
                printNumber(i)
                self.zero_lock.release()
                self.odd_lock.release()
        
        
    def odd(self, printNumber: 'Callable[[int], None]') -> None:
        for i in range(self.n + 1):
            if i % 2 == 1:
                self.odd_lock.acquire()
                self.nonzero_lock.acquire()
                printNumber(i)
                self.zero_lock.release()
                self.even_lock.release()

class TestZeroEvenOdd(unittest.TestCase):
    def setUp(self):
        self.output = StringIO()
        sys.stdout = self.output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_zero_even_odd(self):
        def run_test(n):
            zeo = ZeroEvenOdd(n)
            threads = []
            
            def printNumber(x):
                print(x, end='')

            threads.append(threading.Thread(target=zeo.zero, args=(printNumber,)))
            threads.append(threading.Thread(target=zeo.even, args=(printNumber,)))
            threads.append(threading.Thread(target=zeo.odd, args=(printNumber,)))

            for t in threads:
                t.start()

            for t in threads:
                t.join()

            result = self.output.getvalue()
            expected = ''.join(['0' + str(i) for i in range(1, n+1)])
            self.assertEqual(result, expected)

            self.output.truncate(0)
            self.output.seek(0)

        # Test cases
        run_test(5)
        run_test(1)
        run_test(10)

# https://leetcode.com/problems/traffic-light-controlled-intersection/
class TrafficLight:
    def __init__(self):
        self.lock = Lock()
        self.green = 1

    def carArrived(
        self,
        carId: int,                      # ID of the car
        roadId: int,                     # ID of the road the car travels on. Can be 1 (road A) or 2 (road B)
        direction: int,                  # Direction of the car
        turnGreen: 'Callable[[], None]', # Use turnGreen() to turn light to green on current road
        crossCar: 'Callable[[], None]'   # Use crossCar() to make car cross the intersection
    ) -> None:
        # critical section. Only one can execute this change
        with self.lock:
            if self.green != roadId:
                self.green = roadId
                turnGreen()
            crossCar()

class TestTrafficLight(unittest.TestCase):
    def setUp(self):
        self.traffic_light = TrafficLight()
        self.green_road = 1
        self.crossed_cars = []
        self.green_changes = []

    def turnGreen(self):
        self.green_road = 3 - self.green_road  # Switch between 1 and 2
        self.green_changes.append(self.green_road)

    def crossCar(self, carId):
        self.crossed_cars.append(carId)

    def simulate_car(self, carId, roadId, direction):
        self.traffic_light.carArrived(
            carId,
            roadId,
            direction,
            self.turnGreen,
            lambda: self.crossCar(carId)
        )

    def test_traffic_light(self):
        # Simulate cars arriving
        cars = [
            (1, 1, 1),  # Car 1 on Road 1
            (2, 1, 2),  # Car 2 on Road 1
            (3, 2, 3),  # Car 3 on Road 2
            (4, 2, 4),  # Car 4 on Road 2
            (5, 1, 1),  # Car 5 on Road 1
        ]

        threads = []
        for carId, roadId, direction in cars:
            thread = Thread(target=self.simulate_car, args=(carId, roadId, direction))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check if the cars crossed in the correct order
        self.assertEqual(self.crossed_cars, [1, 2, 3, 4, 5])

        # Check if the traffic light changed correctly
        self.assertEqual(self.green_changes, [2, 1])  # change to road 2 then 1

    def test_concurrent_arrivals(self):
        # Simulate concurrent arrivals on both roads
        cars = [
            (1, 1, 1),  # Car 1 on Road 1
            (2, 2, 3),  # Car 2 on Road 2
            (3, 1, 2),  # Car 3 on Road 1
            (4, 2, 4),  # Car 4 on Road 2
        ]

        threads = []
        for carId, roadId, direction in cars:
            thread = Thread(target=self.simulate_car, args=(carId, roadId, direction))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check if all cars crossed
        self.assertEqual(set(self.crossed_cars), {1, 2, 3, 4})

        # Check if the traffic light changed at least once
        self.assertGreater(len(self.green_changes), 0) 

# pip install readerwriterlock
# from rwlock import RWLock
# class TrafficLightRW:
#     def __init__(self):
#         self.rw_lock = RWLock()
#         self.green_road = 1
#         self.green_direction = 'straight'

#     def carArrived(self, carId, roadId, direction, turnGreen, crossCar):
#         change_light = False
#         change_direction = False
        
#         with self.rw_lock.reader():
#             if self.green_road != roadId or self.green_direction != direction:
#                 change_light = True

#         if change_light:
#             with self.rw_lock.writer():
#                 if self.green_road != roadId:
#                     self.green_road = roadId
#                     self.green_direction = 'straight'
#                     turnGreen()
#                 elif self.green_direction != direction:
#                     self.green_direction = direction
#                     switchDirection()
        
#         crossCar()

# when hydrogen arrives must await another hydrogen and oxygen
# when oxygen arrives must await 2 hydrogen
# https://leetcode.com/problems/building-h2o/
class H2O:
    def __init__(self):
        self.h_sem = Semaphore(2)
        self.o_sem = Semaphore(1)
        self.barrier = Barrier(3)

    def hydrogen(self, releaseHydrogen: 'Callable[[], None]') -> None:
        self.h_sem.acquire()
        self.barrier.wait()
        releaseHydrogen()
        self.h_sem.release()

    def oxygen(self, releaseOxygen: 'Callable[[], None]') -> None:
        self.o_sem.acquire()
        self.barrier.wait()
        releaseOxygen()
        self.o_sem.release()

class TestH2O(unittest.TestCase):
    def setUp(self):
        self.h2o = H2O()
        self.result = Queue()

    def releaseHydrogen(self):
        self.result.put('H')

    def releaseOxygen(self):
        self.result.put('O')

    def test_h2o_formation(self):
        threads = []
        # Create 6 H and 3 O, which should form 3 water molecules
        for _ in range(6):
            t = Thread(target=self.h2o.hydrogen, args=(self.releaseHydrogen,))
            threads.append(t)
            t.start()
        for _ in range(3):
            t = Thread(target=self.h2o.oxygen, args=(self.releaseOxygen,))
            threads.append(t)
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

        # Collect results
        molecules = []
        while not self.result.empty():
            molecules.append(self.result.get())

        # Check results
        self.assertEqual(len(molecules), 9)  # 9 atoms in total
        h_count = molecules.count('H')
        o_count = molecules.count('O')
        self.assertEqual(h_count, 6)  # 6 hydrogen atoms
        self.assertEqual(o_count, 3)  # 3 oxygen atoms

        # Check if atoms are grouped correctly
        for i in range(0, 9, 3):
            molecule = ''.join(sorted(molecules[i:i+3]))
            self.assertEqual(molecule, 'HHO')  # Each group should form H2O

    def test_concurrent_formation(self):
        # full water molecule each
        def run_formation():
            threads = []
            for _ in range(2):
                t = Thread(target=self.h2o.hydrogen, args=(self.releaseHydrogen,))
                threads.append(t)
                t.start()
            t = Thread(target=self.h2o.oxygen, args=(self.releaseOxygen,))
            threads.append(t)
            t.start()
            for t in threads:
                t.join()

        # Run multiple formations concurrently
        formation_threads = [Thread(target=run_formation) for _ in range(100)]
        for t in formation_threads:
            t.start()
        for t in formation_threads:
            t.join()

        # Check results
        molecules = []
        while not self.result.empty():
            molecules.append(self.result.get())

        self.assertEqual(len(molecules), 300)  # 100 water molecules * 3 atoms each
        h_count = molecules.count('H')
        o_count = molecules.count('O')
        self.assertEqual(h_count, 200)  # 200 hydrogen atoms
        self.assertEqual(o_count, 100)  # 100 oxygen atoms

# https://leetcode.com/problems/web-crawler-multithreaded/
class WebCrawler:
    def __init__(self):
        self.lock = Lock()
        self.visited = set()

    def extractHostName(self, url):
        return '.'.join(url.split('/')[2].split('.')[1:])

    # start from startUrl
    # call htmlparse.getUrls to get all urls from a webpage
    # do not crawl same link twice
    # explore only the links that are under the same hostname as start url
    def crawl(self, startUrl: str, htmlParser: 'HtmlParser') -> list[str]:
        def crawler(url):
            for next_url in htmlParser.getUrls(url):
                if self.extractHostName(next_url) == start_hostname:
                    # lock multithreaded access. could technically do rw on the visited but not worth it
                    with self.lock:
                        if next_url not in self.visited:
                            # have to add to visited before we queue so we dont double push links
                            self.visited.add(next_url)
                            self.queue.put(next_url)
        self.visited = set([startUrl])
        self.queue = Queue()
        self.queue.put(startUrl)
        start_hostname = self.extractHostName(startUrl)
        with ThreadPoolExecutor(max_workers = 10) as executor:
            while not self.queue.empty():
                futures = []
                for _ in range(self.queue.qsize()):
                    url = self.queue.get()
                    futures.append(executor.submit(crawler, url))

                wait(futures) 
        return list(self.visited)


from collections import deque
from threading import Condition
# https://leetcode.com/problems/design-bounded-blocking-queue 
# condition combos lock and wait scenario
class BoundedBlockingQueue:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.queue = deque()
        self.condition = Condition()

    def enqueue(self, element: int) -> None:
        with self.condition:
            while len(self.queue) == self.capacity:
                self.condition.wait()
            self.queue.append(element)
            self.condition.notify()

    def dequeue(self) -> int:
        with self.condition:
            while len(self.queue) == 0:
                self.condition.wait()
            item = self.queue.popleft()
            self.condition.notify()
            return item

    def size(self) -> int:
        with self.condition:
            return len(self.queue)

from threading import Condition
# https://leetcode.com/problems/fizz-buzz-multithreaded/
class FizzBuzz:
    def __init__(self, n: int):
        self.n = n
        self.i = 1
        self.condition = Condition()

    # fizzbuzz if i is divisible by 3 and 5
    # fizz if divisible by 3 and not 5
    # buzz if i is divisible by 5 and not 3
    # i if not divisible by 3 or 5
    # printFizz() outputs "fizz"
    def fizz(self, printFizz: 'Callable[[], None]') -> None:
        with self.condition:
            while self.i <= self.n:
                if self.i % 3 == 0 and self.i % 5 != 0:
                    printFizz()
                    self.i += 1
                    self.condition.notify_all()
                else:
                    self.condition.wait()

    # printBuzz() outputs "buzz"
    def buzz(self, printBuzz: 'Callable[[], None]') -> None:
        with self.condition:
            while self.i <= self.n:
                if self.i % 3 != 0 and self.i % 5 == 0:
                    printBuzz()
                    self.i += 1
                    self.condition.notify_all()
                else:
                    self.condition.wait()
    	

    # printFizzBuzz() outputs "fizzbuzz"
    def fizzbuzz(self, printFizzBuzz: 'Callable[[], None]') -> None:
        with self.condition:
            while self.i <= self.n:
                if self.i % 3 == 0 and self.i % 5 == 0:
                    printFizzBuzz()
                    self.i += 1
                    self.condition.notify_all()
                else:
                    self.condition.wait()
    	

    # printNumber(x) outputs "x", where x is an integer.
    def number(self, printNumber: 'Callable[[int], None]') -> None:
        with self.condition:
            while self.i <= self.n:
                if self.i % 3 != 0 and self.i % 5 != 0:
                    printNumber(self.i)
                    self.i += 1
                    self.condition.notify_all()
                else:
                    self.condition.wait()

if __name__ == '__main__':
    unittest.main()