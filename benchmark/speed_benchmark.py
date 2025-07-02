from __future__ import annotations

import csv
import random
import time
from functools import lru_cache
from pathlib import Path
from statistics import mean, stdev
from typing import Any, Callable

from fast_unidecode import unidecode as fast_unidecode
from unidecode import unidecode


# It's a good practice to use a cache to simulate real-world usage
# where the same strings might be processed multiple times.
@lru_cache(maxsize=8)
def py_unidecode(text: str) -> str:
    """Cached version of the original Python unidecode."""
    return unidecode(text)


@lru_cache(maxsize=8)
def rust_unidecode(text: str) -> str:
    """Cached version of the fast_unidecode (Rust implementation)."""
    return fast_unidecode(text)


def run_benchmark(
    func: Callable[[str], str], text: str, iterations: int
) -> list[float]:
    """
    Benchmark a given unidecode function.

    Args:
        func: The unidecode function to benchmark.
        text: The string to process.
        iterations: The number of times to run the benchmark.

    Returns:
        A list of execution times in seconds.
    """
    timings = []
    for _ in range(iterations):
        # Shuffle the string to prevent lower-level caching and ensure the
        # function's performance is tested on varied (but same-character) inputs.
        shuffled_text = "".join(random.sample(text, len(text)))
        start_time = time.perf_counter()
        func(shuffled_text)
        end_time = time.perf_counter()
        timings.append(end_time - start_time)
    return timings


def get_mocked_data() -> dict[str, str]:
    """Provides a dictionary of strings for benchmarking."""
    return {
        "a": "看看谁的脚丫子更大，就踩上去",
        "b": "回去以后",
        "c": 14 * "回去以后",
        "num": "100,23",
        "cur": "100,23 CZK",
        "d": " げんまい茶 ᔕᓇᓇ",
        "e": "csonbhxehj",
        "f": "KNFOTVDFLQ",
        "g": "kRAaicQQMzSFtOkZPeyUumzAJoRmjDXJ",
        "h": 5 * "299mm73d28rg6x7m8qe",
        "i": "8LhNr31RxtmUrtWponbl",
        "j": 100 * "8LhNr31RxtmUrtWponbl",
        "k": "}<[,[{<#[/=-'@-%(*&~",
        "l": (
            int(5e4)
            * "Æneid 1234 098 @#$!@)() -0/'ˇmkdaslllsmdlamdlkas げんまい茶 ᔕᓇᓇ 北亰 étude 四千年前有一个姑娘叫姜嫄，她有一天觉得很空虚，就到郊外玩，看见一只巨人脚印，也许是外星人留下的，她想上去比一比，看看谁的脚丫子更大，就踩上去。踩上去就发现肚子里乱动，跟怀了孕似的。回去以后，肚子里的小孩，又老不出来，过了十二个月才生下来。"
        ),
        "m": ".H<ncWi&dY_Wf)`'bNR=P@)G\8EkVEdmTZdMVO]gM2v m!",
        "n": 14 * "aDc4__uu3I_jq/68=YK(=Z'/3u5@{cu5_6{ v]U9q nZ_#X&ZbXBv~tFmb@p}Z",
    }


def main() -> None:
    """Main function to run the benchmark and save results."""
    test_data = get_mocked_data()
    all_results: list[dict[str, Any]] = []
    iteration_counts = [1, 5, 10, 20, 100, 500]
    num_rounds = 10

    print("Starting benchmark...")

    for iterations in iteration_counts:
        for round_num in range(num_rounds):
            print(
                f"\n--- Running: {iterations} iterations, "
                f"round {round_num + 1}/{num_rounds} ---"
            )
            round_results: dict[str, Any] = {
                "iterations": iterations,
                "round": round_num + 1,
            }

            for key, text in test_data.items():
                print(f"Benchmarking case: '{key}'")

                # Adjust iterations for the very long string 'l'
                current_iters = min(3, iterations) if key == "l" else iterations

                if current_iters == 0:
                    print("Skipping due to 0 iterations.")
                    round_results[key] = 1.0
                    continue

                py_timings = run_benchmark(py_unidecode, text, current_iters)
                rust_timings = run_benchmark(rust_unidecode, text, current_iters)

                py_mean = mean(py_timings)
                py_std = stdev(py_timings) if len(py_timings) > 1 else 0
                rust_mean = mean(rust_timings)
                rust_std = stdev(rust_timings) if len(rust_timings) > 1 else 0

                print(f"  Python: {py_mean * 1000:.3f} ± {py_std * 1000:.3f} ms")
                print(f"  Rust:   {rust_mean * 1000:.3f} ± {rust_std * 1000:.3f} ms")

                if rust_mean > 0:
                    speedup = py_mean / rust_mean
                    if speedup > 1:
                        print(f"  Speedup: {speedup:.2f}x")
                    else:
                        print(f"  Slowdown: {1 / speedup:.2f}x")
                else:
                    speedup = float("inf") if py_mean > 0 else 1.0
                    print(
                        "  Rust version was instantaneous, speedup is effectively infinite."
                    )

                round_results[key] = round(speedup, 4)
                print("-" * 20)

            py_unidecode.cache_clear()
            rust_unidecode.cache_clear()
            all_results.append(round_results)

    # --- Save results to CSV ---
    output_file = Path("result.tsv")
    fieldnames = ["iterations", "round"] + list(test_data.keys())
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(all_results)
    print(f"\nBenchmark results saved to {output_file}")

    # --- Final Summary ---
    total_comparisons = 0
    rust_was_faster = 0
    total_speedup = 0.0

    for res in all_results:
        for key in test_data:
            speedup = res.get(key, 1.0)
            if speedup != 1.0:  # Exclude cases with no difference
                total_comparisons += 1
                if speedup > 1.0:
                    rust_was_faster += 1
                total_speedup += speedup

    if total_comparisons > 0:
        outperformance_pct = 100 * rust_was_faster / total_comparisons
        average_speedup = total_speedup / total_comparisons
        print("\n--- Summary ---")
        print(
            f"Rust implementation was faster in {outperformance_pct:.2f}% "
            "of comparisons."
        )
        print(f"Average speedup across all comparisons: {average_speedup:.2f}x.")
    else:
        print("\n--- Summary ---")
        print("No conclusive performance difference observed.")


if __name__ == "__main__":
    main()
