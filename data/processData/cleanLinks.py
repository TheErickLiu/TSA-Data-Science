import re

def remove_urls(line):
    pattern = r'https?://\S+|www\.\S+'
    # Substitute found URLs with an empty string
    clean_line = re.sub(pattern, '', line)
    return clean_line

def clean_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in lines:
            clean_line = remove_urls(line)
            output_file.write(clean_line)

    print(f"Processed file saved to {output_file_path}.")

# Example usage
input_file_path = 'scrubbedData/scrubbedTesla.txt'  # Path to your original text file
output_file_path = 'clean.txt'  # Path to save the cleaned text file

clean_file(input_file_path, output_file_path)