import time


def time_checker(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Потраченное время: {end_time - start_time:.4f}")
        return result
    return wrapper
