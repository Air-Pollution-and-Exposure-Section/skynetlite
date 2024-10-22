import os

def count_lines_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return sum(1 for line in file)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0

def scan_directory_for_py_files(root_dir, exclude_file):
    line_counts = {}
    total_lines = 0  # Initialize total line count
    excluded_dirs = {'build', 'venv'}  # Set of directory names to exclude
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modify the dirnames list in-place to exclude specified directories
        dirnames[:] = [d for d in dirnames if d not in excluded_dirs]
        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(dirpath, filename)
                # Skip the script file itself
                if os.path.abspath(file_path) == os.path.abspath(exclude_file):
                    continue
                line_count = count_lines_in_file(file_path)
                line_counts[file_path] = line_count
                total_lines += line_count  # Update total line count
    return line_counts, total_lines

def main():
    root_dir = os.getcwd()  # Get the current working directory
    script_file = __file__  # Get the path of the current script
    py_files_line_counts, total_line_count = scan_directory_for_py_files(root_dir, script_file)
    for path, lines in py_files_line_counts.items():
        print(f"{path}: {lines} lines")
    print(f"Total line count for all Python files: {total_line_count}")

if __name__ == "__main__":
    main()
