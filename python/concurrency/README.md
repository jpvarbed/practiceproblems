# Concurrency

Practice concurrency in python.

```bash
python3 python/concurrency/concurrency.py
```

## Concurrency Primitives

### Condition

Combines a lock and a wait queue.

### Lock vs Semaphore

1. A lock allows only one thread at a time, while a semaphore can allow a specified number of threads.
2. A lock is typically used for mutual exclusion, while a semaphore is used for limiting concurrent access to resources.

### Lock/Semaphore vs Barrier

1. Locks and semaphores control access to resources, while barriers synchronize the progress of multiple threads.
2. Barriers wait for a specific number of threads to reach a point before any can proceed, unlike locks or semaphores which don't have this "all-or-nothing" behavior.

### Semaphore vs Barrier

1. A semaphore controls the number of threads that can access a resource concurrently.
2. A barrier ensures that a specific number of threads have reached a certain point before any can proceed.

### Examples of when to use each

1. Lock: When you need to ensure that only one thread at a time can access a shared resource, like a shared variable or file.
2. Semaphore: When you want to limit the number of threads that can access a resource simultaneously, like limiting the number of concurrent database connections.
3. Barrier: When you need multiple threads to wait for each other before proceeding, like in parallel computing where you need all threads to finish one phase before starting the next.
