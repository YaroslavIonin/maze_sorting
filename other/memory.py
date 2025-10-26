import tracemalloc


def memory_checker(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(current / 1024 / 1024, peak / 1024 / 1024)
        return result
    return wrapper
