keywords = ['GOOGL', 'alphabet', 'google', 'sundar', 'pichai']  

keywords = [keyword.lower() for keyword in keywords]

current = "Alphabet"

original_file_path = f'unscrubbedData/redditData{current}.txt'  # Path to your original file
temp_file_path = f'scrubbedData/scrubbed{current}.txt'  # Temporary file path

counter = 0

with open(original_file_path, 'r', encoding='utf-8') as original_file, open(temp_file_path, 'w', encoding='utf-8') as temp_file:
    for line in original_file:
        # Convert line to lowercase and check if any keyword is in the current line
        if any(keyword in line.lower() for keyword in keywords):
            counter += 1
            temp_file.write(line)  # Write the line to the temporary file if it contains a keyword

print(f"File processing completed. There were {counter} lines with keywords.")