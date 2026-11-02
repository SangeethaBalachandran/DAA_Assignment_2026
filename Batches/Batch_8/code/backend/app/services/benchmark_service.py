import time
import random
from typing import List, Dict, Any
from ..schemas.compression import SymbolFrequency
from .compression_service import compression_service

class BenchmarkService:
    def run_benchmark(self, sizes: List[int] = [8, 32, 128, 512, 1024]) -> List[Dict[str, Any]]:
        """
        Executes actual empirical benchmarks comparing Min-heap Huffman vs Two-Queue
        across different alphabet sizes.
        Uses real execution timings and actual operation counters.
        """
        results = []
        random.seed(1337)

        for n in sizes:
            # Generate random distinct symbols and integer frequencies
            raw_items = [
                SymbolFrequency(symbol=f"S{i}", frequency=random.randint(1, 1000))
                for i in range(n)
            ]

            # Measure Min-Heap Huffman over multiple iterations
            iterations = 20 if n <= 256 else 10
            huff_times = []
            huff_resp = None
            for _ in range(iterations):
                t0 = time.perf_counter()
                huff_resp = compression_service.generate_huffman(raw_items)
                huff_times.append((time.perf_counter() - t0) * 1000.0)

            # Measure Two-Queue (Presorted input)
            # Pre-sort frequencies to reflect van Leeuwen linear-time condition
            sorted_items = sorted(raw_items, key=lambda x: x.frequency)
            tq_times = []
            tq_resp = None
            for _ in range(iterations):
                t0 = time.perf_counter()
                tq_resp = compression_service.generate_two_queue(sorted_items)
                tq_times.append((time.perf_counter() - t0) * 1000.0)

            avg_huff_ms = sum(huff_times) / len(huff_times)
            avg_tq_ms = sum(tq_times) / len(tq_times)

            results.append({
                "alphabet_size": n,
                "min_heap_time_ms": round(avg_huff_ms, 4),
                "two_queue_time_ms": round(avg_tq_ms, 4),
                "min_heap_ops": huff_resp.operations_count if huff_resp else 0,
                "two_queue_ops": tq_resp.operations_count if tq_resp else 0,
                "huffman_avg_len": huff_resp.average_length if huff_resp else 0.0,
                "two_queue_avg_len": tq_resp.average_length if tq_resp else 0.0,
                "costs_equivalent": abs(huff_resp.average_length - tq_resp.average_length) < 1e-6 if huff_resp and tq_resp else False,
                "speedup_factor": round(avg_huff_ms / avg_tq_ms, 2) if avg_tq_ms > 0 else 1.0
            })

        return results

benchmark_service = BenchmarkService()

