# Explicit is better than implicit
from typing import * 

import tracemalloc
import threading
import time


class Profiler:
    
    class FunctionProfiler:
        class ProfilerOutput:  
            def __init__(self, perfomance_over_time: dict = {}, peak_consumption: int = 0, time: int = 0) -> None:
                self.perfomance_over_time = perfomance_over_time
                self.peak_consumption = peak_consumption
                self.time = time

            def __str__(self) -> str:
                return f"Peak consumption: {self.peak_consumption} bytes\nTime: {self.time}ns\nPerfomance over time(time: bytes): {self.perfomance_over_time}"

        def __init__(self) -> None:
            self._func_is_running: bool = False
            self._start_time: int = 0
            self._output = self.ProfilerOutput()
            
        def _profiling_cycle(self):
            while self._func_is_running:
                self._output.perfomance_over_time[time.perf_counter_ns() - self._start_time] = tracemalloc.get_traced_memory()[0]
                time.sleep(0.001)
            
        def start_profiling(self) -> None:
            tracemalloc.start()
            self._start_time = time.perf_counter_ns()
            self._func_is_running = True
            profiling_thread = threading.Thread(target = self._profiling_cycle)
            profiling_thread.start()
            
        def stop_profiling(self) -> ProfilerOutput:
            self._func_is_running = False
            self._output.time = time.perf_counter_ns() - self._start_time
            self._output.peak_consumption = tracemalloc.get_traced_memory()[1]
            self._output.perfomance_over_time = dict(sorted(self._output.perfomance_over_time.items()))
            tracemalloc.stop()
            return self._output
    
    def __init__(self, func: callable) -> None:
        self._function = func
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        func_profiler = Profiler.FunctionProfiler()
        func_profiler.start_profiling()
        self._function(*args, **kwargs)
        print(func_profiler.stop_profiling())
        
