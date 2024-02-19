from my_debug_tools import Profiler

@Profiler
def foo():
    for i in range(100):
        print(f"Some heavy and stupid for loop. Iteration: {i}")
        
@Profiler
def bar(i: int):
    return sum(range(i))

def main():
    foo()
    bar(10000)

if __name__ == "__main__":
    main()
