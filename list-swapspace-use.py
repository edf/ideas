import os
import argparse

def format_swap_size(swap_kb):
    # Convert swap size from KB to human-readable format (MB or GB)
    if swap_kb < 1024:
        return f"{swap_kb} KB"
    elif swap_kb < 1024 * 1024:
        return f"{swap_kb / 1024:.2f} MB"
    else:
        return f"{swap_kb / (1024 * 1024):.2f} GB"

def get_swap_usage(sort_by_name=False):
    process_swap = []

    # Iterate over all processes in /proc
    for pid_dir in os.listdir('/proc'):
        if pid_dir.isdigit():
            pid = int(pid_dir)
            try:
                with open(f'/proc/{pid}/status', 'r') as status_file:
                    for line in status_file:
                        if line.startswith('VmSwap:'):
                            swap_kb = int(line.split()[1])
                            if swap_kb > 0:
                                with open(f'/proc/{pid}/cmdline', 'r') as cmdline_file:
                                    cmdline = cmdline_file.read().replace('\x00', ' ')
                                process_swap.append((pid, swap_kb, cmdline.strip()))
            except FileNotFoundError:
                pass

    # Sort by process name (cmdline) or swap size
    if sort_by_name:
        process_swap.sort(key=lambda x: x[2])
    else:
        process_swap.sort(key=lambda x: x[1])

    # Print the results in a table-like format
    print("PID\tSwap Size\tCommand Line")
    for pid, swap_kb, cmdline in process_swap:
        formatted_swap = format_swap_size(swap_kb)
        print(f"{pid}\t{formatted_swap}\t{cmdline}")

    overall_swap = sum(swap_kb for _, swap_kb, _ in process_swap)
    formatted_overall_swap = format_swap_size(overall_swap)
    print(f"\nOverall swap used: {formatted_overall_swap}\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Get swap usage for processes")
    parser.add_argument("--sort-by-name", action="store_true", help="Sort by process name (command line)")
    args = parser.parse_args()

    get_swap_usage(sort_by_name=args.sort_by_name)

