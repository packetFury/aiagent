"""
get_file_info() unit tests

from functions.get_files_info import get_files_info

print(f"Results from current directory: \n{get_files_info('calculator', '.')}")

print(f"Results from calculator directory: \n{get_files_info('calculator', 'pkg')}")

print(f"Results from calculator directory: \n{get_files_info('calculator', '/bin')}")

print(f"Results from calculator directory: \n{get_files_info('calculator', '../')}")
"""

"""
get_file_content() unit tests

from functions.get_file_content import get_file_content

print(f"Results from lorem.txt: {get_file_content('calculator', 'lorem.txt')}")

print(f"Results from main.py: {get_file_content('calculator', 'main.py')}")

print(f"Results from calculator.py: {get_file_content('calculator', 'pkg/calculator.py')}")

print(f"Results from /bin/cat: {get_file_content('calculator', '/bin/cat')}")

print(f"Results from does_not_exist.py: {get_file_content('calculator', 'pkg/does_not_exist.py')}")
"""

"""
write_file() unit tests

from functions.write_file import write_file

print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
"""

"""
run_python_file() unit tests

from functions.run_python_file import run_python_file

print(run_python_file("calculator", "main.py"))
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print(run_python_file("calculator", "tests.py"))
print(run_python_file("calculator", "../main.py"))
print(run_python_file("calculator", "nonexistent.py"))
"""