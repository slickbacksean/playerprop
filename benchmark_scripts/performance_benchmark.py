import time
import psutil
import platform
import multiprocessing
import numpy as np
import pandas as pd
from typing import Dict, Any
import json
import os
import socket

class PerformanceBenchmark:
    def __init__(self, output_dir: str = 'benchmark_results'):
        """
        Initialize performance benchmarking system.
        
        Args:
            output_dir (str): Directory to store benchmark results
        """
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir

    def get_system_info(self) -> Dict[str, Any]:
        """
        Collect comprehensive system information.
        
        Returns:
            Dict[str, Any]: Detailed system configuration
        """
        return {
            'hostname': socket.gethostname(),
            'os': {
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
            },
            'cpu': {
                'name': platform.processor(),
                'physical_cores': psutil.cpu_count(logical=False),
                'logical_cores': psutil.cpu_count(logical=True)
            },
            'memory': {
                'total': psutil.virtual_memory().total / (1024 ** 3),  # GB
                'available': psutil.virtual_memory().available / (1024 ** 3)  # GB
            }
        }

    def benchmark_cpu_performance(self, iterations: int = 100000) -> Dict[str, float]:
        """
        Benchmark CPU performance using numerical computations.
        
        Args:
            iterations (int): Number of computation iterations
        
        Returns:
            Dict[str, float]: CPU performance metrics
        """
        start_time = time.time()
        
        # Numerical computation benchmark
        result = 0
        for _ in range(iterations):
            result += np.sqrt(np.random.random())
        
        cpu_time = time.time() - start_time
        
        return {
            'total_time': cpu_time,
            'iterations': iterations,
            'computations_per_second': iterations / cpu_time
        }

    def benchmark_memory_performance(self, data_size: int = 10_000_000) -> Dict[str, float]:
        """
        Benchmark memory performance and data manipulation.
        
        Args:
            data_size (int): Size of random data to process
        
        Returns:
            Dict[str, float]: Memory performance metrics
        """
        # Create large random dataframe
        start_time = time.time()
        df = pd.DataFrame({
            'random_data': np.random.random(data_size),
            'category': np.random.choice(['A', 'B', 'C'], data_size)
        })
        
        # Perform memory-intensive operations
        df_grouped = df.groupby('category').mean()
        df_sorted = df.sort_values('random_data')
        
        memory_time = time.time() - start_time
        
        return {
            'total_time': memory_time,
            'data_size': data_size,
            'processing_speed': data_size / memory_time
        }

    def benchmark_multiprocessing(self, num_processes: int