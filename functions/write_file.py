import os

def write_file(working_directory, file_path, content):
    filepath = os.path.join(working_directory, file_path)

    # Normalize to account for cross-platform compatibility
    abs_working_dir = os.path.normcase(os.path.abspath(working_directory))
    abs_filepath = os.path.normcase(os.path.abspath(filepath))

    # Check for external path
    common_path = os.path.commonpath([abs_working_dir, abs_filepath])

    if common_path != abs_working_dir:
        return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"

    final_abs_path = os.path.abspath(filepath)
    file_dir = os.path.dirname(final_abs_path)
    if file_dir and not os.path.isdir(file_dir):
        try:
            os.makedirs(final_abs_path)
        except Exception as e:
            return f"Error: {e}"

    try:
        with open(final_abs_path, "w") as f:
            f.write(content)
            return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
    except Exception as e:
        return f"Error: {e}"