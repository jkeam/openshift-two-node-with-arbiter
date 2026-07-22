#!/usr/bin/env python3
import argparse
import sys

def calculate_memory_allocation(memory_gib: float) -> float:
    """
    Calculates allocated memory based on tiered percentages:
    - 25% of first 4 GiB
    - 20% of next 4 GiB (4 - 8 GiB)
    - 10% of next 8 GiB (8 - 16 GiB)
    - 6% of next 112 GiB (16 - 128 GiB)
    - 2% of remaining (> 128 GiB)
    """
    tier1 = min(memory_gib, 4) * 0.25
    tier2 = max(0.0, min(memory_gib - 4, 4)) * 0.20
    tier3 = max(0.0, min(memory_gib - 8, 8)) * 0.10
    tier4 = max(0.0, min(memory_gib - 16, 112)) * 0.06
    tier5 = max(0.0, memory_gib - 128) * 0.02
    
    return tier1 + tier2 + tier3 + tier4 + tier5

def calculate_cpu_allocation(total_cpu: float) -> float:
    """
    Calculates recommended CPU reservation based on core count:
    - Base: 0.06 cores for 1 CPU
    - Additional: +0.012 cores for each additional CPU above 1
    """
    base_allocation = 0.06
    increment_per_cpu = 0.012
    
    if total_cpu > 1:
        return base_allocation + increment_per_cpu * (total_cpu - 1)
    return base_allocation

def get_interactive_input(prompt: str) -> float:
    while True:
        try:
            val = float(input(prompt))
            if val < 0:
                print("Error: Value cannot be negative. Try again.")
                continue
            return val
        except (ValueError, KeyboardInterrupt):
            print("\nInvalid input or cancelled.")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Calculate system reserved CPU and Memory allocations.")
    parser.add_argument("-m", "--memory", type=float, help="Total memory in GiB")
    parser.add_argument("-c", "--cpu", type=float, help="Total CPU cores")
    args = parser.parse_args()

    # Get values from flags or prompt if missing
    memory_gib = args.memory
    if memory_gib is None:
        memory_gib = get_interactive_input("Enter total memory in GiB: ")

    total_cpu = args.cpu
    if total_cpu is None:
        total_cpu = get_interactive_input("Enter total CPU cores: ")

    reserved_memory = calculate_memory_allocation(memory_gib)
    reserved_cpu = calculate_cpu_allocation(total_cpu)

    print("\n--- Reserved System Resources ---")
    print(f"Total Memory:     {memory_gib:.2f} GiB  --> Reserved: {reserved_memory:.4f} GiB")
    print(f"Total CPU Cores:  {total_cpu:.2f} cores --> Reserved: {reserved_cpu:.2f} cores ({reserved_cpu * 1000:.0f}m)")

if __name__ == "__main__":
    main()
    # From: https://access.redhat.com/solutions/5843241
