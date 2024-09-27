import re

# Define transformation functions
def uppercase_all(text):
    return text.upper()

def uppercase_first_word(text):
    # Process each line separately
    lines = text.split('\n')
    processed_lines = []
    for line in lines:
        words = line.split()
        if words:
            words[0] = words[0].upper()
        processed_line = ' '.join(words)
        processed_lines.append(processed_line)
    return '\n'.join(processed_lines)


def uppercase_tagged_text(text):
    import re
    # Regex pattern to match tags with attributes
    pattern = re.compile(r'(<(b|u|i)(\s[^>]*)?>)(.*?)(</\2>)', re.DOTALL | re.IGNORECASE)
    
    def uppercase_match(match):
        opening_tag = match.group(1)   # The full opening tag (e.g., <b class="bold">)
        tag_name = match.group(2)      # The tag name ('b', 'u', or 'i')
        inner_text = match.group(4)    # The text inside the tags
        closing_tag = match.group(5)   # The closing tag (e.g., </b>)
        
        # Uppercase the inner text
        uppercased_inner_text = inner_text.upper()
        
        # Reconstruct the tagged text with uppercased inner text
        return f'{uppercased_inner_text}'
        # return f'{opening_tag}{uppercased_inner_text}{closing_tag}'
    
    transformed_text = pattern.sub(uppercase_match, text)
    return transformed_text
