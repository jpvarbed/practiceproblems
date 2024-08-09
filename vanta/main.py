import sys
import csv
import json

def process_data(input_data):
    return input_data.upper()

if __name__ == "__main__":
    for line in sys.stdin:
        processed = process_data(line.strip())
        print(processed)