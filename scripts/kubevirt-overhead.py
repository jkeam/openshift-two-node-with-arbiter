#!/usr/bin/env python3

def calculate_vm_memory_overhead_gb(requested_memory_gb: float, vcpus: int, graphics_devices: int = 0) -> float:
    """
    Calculates estimated VM memory overhead in GB.
    Converts input GB to MiB, applies the overhead formula, and returns overhead in GB.
    """
    # 1 GB = 1024 MiB
    requested_memory_mib = requested_memory_gb * 1024

    # Formula calculates overhead in MiB
    overhead_mib = (
        (0.002 * requested_memory_mib)
        + 218
        + (8 * vcpus)
        + (16 * graphics_devices)
    )

    # Convert overhead back to GB
    return overhead_mib / 1024


def main():
    print("=== VM Memory Overhead Calculator (in GB) ===\n")

    try:
        requested_mem_gb = float(input("Enter requested RAM (in GB, e.g., 8 or 16): "))
        vcpus = int(input("Enter number of vCPUs: "))
        gpu_count = int(input("Enter number of graphics devices (default 0): ") or "0")

        overhead_gb = calculate_vm_memory_overhead_gb(requested_mem_gb, vcpus, gpu_count)
        total_ram_gb = requested_mem_gb + overhead_gb

        print("\n--- Results ---")
        print(f"Requested Memory:   {requested_mem_gb:,.2f} GB ({requested_mem_gb * 1024:,.0f} MiB)")
        print(f"Estimated Overhead: {overhead_gb:,.2f} GB ({overhead_gb * 1024:,.0f} MiB)")
        print(f"Total Host RAM:     {total_ram_gb:,.2f} GB ({total_ram_gb * 1024:,.0f} MiB)")

    except ValueError:
        print("\nError: Please enter valid numerical values.")


if __name__ == "__main__":
    main()
    # From: https://access.redhat.com/articles/7107457
