import os
import shutil
import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"{func.__name__} start execution")
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} execution time: {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def spaced_timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"\t-> {func.__name__} execution time: {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def clear_directory(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)