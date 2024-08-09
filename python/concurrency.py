import asyncio
# concurrency
from threading import Lock
import threading
import time

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