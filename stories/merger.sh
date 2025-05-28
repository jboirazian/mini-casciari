#!/bin/bash

# Define the output file name
output_file="merged_output.txt"

# Check if the output file already exists and remove it to avoid appending to old data
if [ -f "$output_file" ]; then
    rm "$output_file"
    echo "Removed existing $output_file"
fi

# Loop through all files ending with .txt in the current directory
for file in *.txt; do
    # Check if the file is actually a file (and not a directory or if no .txt files were found)
    if [ -f "$file" ]; then
        echo "Merging $file..."
        echo "" >> "$output_file"
        cat "$file" >> "$output_file"
        echo "" >> "$output_file"
    fi
done

echo "All .txt files have been merged into $output_file"