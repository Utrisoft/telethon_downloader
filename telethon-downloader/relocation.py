import os
import re
import shutil

MOVIES_FOLDER_NAME = "Pelis"
TV_SERIES_FOLDER_NAME = "Series"
# List of suffixes to remove
suffixes_to_remove = ["720p", "1080p", "HDTV",
                      "WEBRip", "DVDRip", ".@CineNcasaa", "@CineNcasaa"]
# Extensiones de archivos de video admitidas
video_extensions = [".avi", ".mkv", ".mp4", ".mov", ".wmv", ".flv"]


# Function to rename the file by removing suffixes


def rename_file(file, suffixes):
    base_name, extension = os.path.splitext(file)
    base_name = base_name.strip()  # Remove whitespace
    for suffix in suffixes:
        base_name = re.sub(re.escape(suffix), '', base_name,
                           flags=re.IGNORECASE).strip()
    new_name = base_name + extension
    return new_name

# Function to determine if the file is a TV series episode or a movie


def determine_file_type(file):
    base_name, extension = os.path.splitext(file)
    if re.search(r'S\d{2}E\d{2}', base_name, re.IGNORECASE) or re.search(r'\d+X\d+', base_name, re.IGNORECASE):
        return TV_SERIES_FOLDER_NAME
    else:
        return MOVIES_FOLDER_NAME

# Function to extract series name and season number from the file name


def extract_series_info(file):
    base_name, _ = os.path.splitext(file)
    match = re.search(r'(.+?)S(\d{2})E(\d{2})', base_name, re.IGNORECASE)
    if match:
        series_name, season = match.group(1), int(match.group(2))
        return series_name.strip().title(), season
    match = re.search(r'(.+?)(\d+) (\d+)X(\d+)', base_name, re.IGNORECASE)
    if match:
        series_name, season = match.group(1), int(match.group(2))
        return series_name.strip().title(), season
    return None, None

# Function to move the file to the appropriate destination


def move_file(file, source_directory, movies_directory, tvSeries_directory):
    if determine_file_type(file) == MOVIES_FOLDER_NAME:
        destination_path = movies_directory
    else:
        series_name, season = extract_series_info(file)
        if not series_name or season is None:
            print(
                f"Error: Could not determine series name or season for '{file}'")
            return None
        destination_path = os.path.join(
            tvSeries_directory, series_name, f"Season {season}")

    if not os.path.exists(destination_path):
        os.makedirs(destination_path, exist_ok=True)

    source_path = os.path.join(source_directory, file)
    destination_path = os.path.join(destination_path, file)
    print(f"Moving from '{source_path}' to '{destination_path}'")
    shutil.move(source_path, destination_path)
    return destination_path.replace(file, "")


# Move function
def move(file_name, directory, movies_directory, tvSeries_directory):

    # Comprobar que el archivo tiene una extensión de video válida
    _, extension = os.path.splitext(file_name)
    if extension.lower() not in video_extensions:
        print(f"The file '{file_name}' is not a valid video file.")
        return file_name, directory

    full_path = os.path.join(directory, file_name)

    # Rename the file by removing suffixes
    new_name = rename_file(file_name, suffixes_to_remove)
    new_path = os.path.join(directory, new_name)
    print(f"The file '{full_path}' will be renamed to '{new_path}.")
    os.rename(full_path, new_path)

    # Move the file to the appropriate destination
    destination_path = move_file(
        new_name, directory, movies_directory, tvSeries_directory)

    return new_name, destination_path


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 5:
        print(
            "Usage: python script.py <file_name> <source_directory> <movies_directory> <tvSeries_directory>")
    else:
        file_name = sys.argv[1]
        source_directory = sys.argv[2]
        movies_directory = sys.argv[3]
        tvSeries_directory = sys.argv[4]
        move(file_name, source_directory, movies_directory, tvSeries_directory)
