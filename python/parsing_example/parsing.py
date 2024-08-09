import sys
import re
from collections import defaultdict, OrderedDict

def parse_log_line(line):
    # Regular expression to match the log level
    match = re.search(r'\[(.*?)\]', line)
    if match:
        return match.group(1)
    return None

def process_logs():
    log_counts = defaultdict(int)
    for line in sys.stdin:
        # remove white space from beginning and end of line with strip
        log_level = parse_log_line(line.strip())
        if log_level:
            log_counts[log_level] += 1
    
    for level, count in log_counts.items():
        print(f"{level}: {count}")

def deduplicate_data():
    unique_lines = OrderedDict()

    for line in sys.stdin:
        unique_lines[line.strip()] = None

    for line in unique_lines:
        print(line)

if __name__ == "__main__":
    process_logs()