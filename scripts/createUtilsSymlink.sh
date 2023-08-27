#!/bin/bash

# Get the directory containing the script
script_dir=$(dirname "$(realpath "$0")")

source_folder=$(realpath $script_dir/../src/utils)
target_parent_directory="$1"

# Convert source folder to an absolute path
source_folder=$(realpath "$source_folder")

# Check if source folder exists
if [ ! -e "$source_folder" ]; then
    echo "Source folder/file '$source_folder' does not exist."
    exit 1
fi

# Extract the name of the source folder
source_folder_name=$(basename "$source_folder")

# Check if target parent directory exists
if [ ! -d "$target_parent_directory" ]; then
    echo "Target parent directory '$target_parent_directory' does not exist."
    exit 1
fi

target_location="$target_parent_directory/$source_folder_name"

# Check if target location exists
if [ -e "$target_location" ] || [ -L "$target_location" ]; then
    if [ -L "$target_location" ]; then
        current_link=$(readlink "$target_location")
        if [ "$current_link" = "$source_folder" ]; then
            echo "Symlink is already present and points to the same location."
            exit 0
        else
            echo "Symlink already exists but points to a different location."
            echo "Deleting the existing symlink..."
            rm "$target_location"
        fi
    else
        echo "Folder/File already exists at '$target_location'."
        echo "Please delete the existing folder/file at '$target_location' and retry."
        exit 1
    fi
fi

# Create symlink
ln -s "$source_folder" "$target_location"

if [ $? -eq 0 ]; then
    echo "Success"
else
    echo "Failed to create symlink."
fi