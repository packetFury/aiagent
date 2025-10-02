import os
from functions.config import MAX_CHARS

def get_file_content(working_directory, file_path):
    filepath = os.path.join(working_directory, file_path)

    # Normalize to account for cross-platform compatibility
    abs_working_dir = os.path.normcase(os.path.abspath(working_directory))
    abs_filepath = os.path.normcase(os.path.abspath(filepath))

    # Check for external path
    common_path = os.path.commonpath([abs_working_dir, abs_filepath])

    if common_path != abs_working_dir:
        return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
    
    final_abs_path = os.path.abspath(filepath)
    print(final_abs_path)
    if not os.path.isfile(final_abs_path):
        return f"Error: File not found or is not a regular file: \"{file_path}\""

    try:
        with open(final_abs_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(final_abs_path) > MAX_CHARS:
                file_content_string += (f'[...File "{file_path}" truncated at {MAX_CHARS} characters]')
            return file_content_string
    except Exception as e:
        return f"Error: {e}"