# Directory: PIIAgenticSystem/input_interface
# File: cli_input_handler.py

def get_input():
    mode = input("Choose mode - [M]ask or [U]nmask: ").strip().lower()
    path = input("Enter file path: ").strip()
    return mode, path