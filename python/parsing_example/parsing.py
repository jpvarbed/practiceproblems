import sys
import re
from collections import defaultdict, OrderedDict

"""
# pattern match
text = "The quick brown fox jumps over the lazy dog"
if re.search(r"quick.*fox", text):
    print("Pattern found!")

# extract info
email = "contact@example.com"
username = re.findall(r"(.+)@", email)[0]
print(username)  # Output: contact

# split strings
text = "apple,banana;cherry:date"
fruits = re.split(r"[,;:]", text)
print(fruits)  # Output: ['apple', 'banana', 'cherry', 'date']

# replace
text = "The price is $100"
new_text = re.sub(r"\$(\d+)", lambda m: f"${int(m.group(1)) * 2}", text)
print(new_text)  # Output: The price is $200

# validate
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

print(is_valid_email("user@example.com"))  # Output: True
print(is_valid_email("invalid-email"))  # Output: False


"""

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