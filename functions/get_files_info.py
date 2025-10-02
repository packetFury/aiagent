import os

def get_files_info(working_directory, directory="."):
    filepath = os.path.join(working_directory, directory)

    # Normalize to account for cross-platform compatibility
    abs_working_dir = os.path.normcase(os.path.abspath(working_directory))
    abs_filepath = os.path.normcase(os.path.abspath(filepath))

    # Check for external path
    common_path = os.path.commonpath([abs_working_dir, abs_filepath])

    if common_path != abs_working_dir:
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"

    final_abs_path = os.path.abspath(filepath)
    if not os.path.isdir(final_abs_path):
        return f"Error: \"{directory}\" is not a directory"

    try:
        contents = os.listdir(final_abs_path)
    except Exception as e:
        return f"Error: {e}"
    results = []
    for i in contents:
        i_full_path = os.path.join(final_abs_path, i)
        try:
            file_size = os.path.getsize(i_full_path)
            is_dir = os.path.isdir(i_full_path)
            results.append(f"- {i}: file_size={file_size} bytes, is_dir={is_dir}")
        except Exception as e:
            results.append(f"Error: {e}")
    return "\n".join(results)