import re

text = r""" homEwork:
 tHis iz your homeWork, copy these Text to variable.

 You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

 it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

 last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87. """

# Step 1: Split text into sentences
sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

# Step 2: Capitalize the first letter of each sentence
capitalized_sentences = [sentence.strip().capitalize() for sentence in sentences]

# Step 3: Join sentences back into a single string
formatted_text = '. '.join([sentence.rstrip('.') for sentence in capitalized_sentences]) + '.'

def replace_iz_except_after_fix(text):
    # Find the position of the word "fix"
    fix_match = re.search(r'fix["“]', text, re.IGNORECASE)

    if fix_match:
        fix_position = fix_match.end()  # Position right after "fix"

        # Text before and after "fix"
        before_fix = text[:fix_position]
        after_fix = text[fix_position:]

        # Replace all 'iz' with 'is' in both parts, except the first occurrence after "fix"
        before_fix = re.sub(r'\biz\b', 'is', before_fix, flags=re.IGNORECASE)
        after_fix = re.sub(r'\biz\b', 'is', after_fix, flags=re.IGNORECASE)

        # Leave "iz" unchanged after "fix"
        after_fix = after_fix.replace('is', 'iz', 1)

        return before_fix + after_fix
    else:
        # If "fix" is not present, just replace all 'iz' with 'is'
        return re.sub(r'\biz\b', 'is', text, flags=re.IGNORECASE)

# Apply the replacement in the formatted text
final_text = replace_iz_except_after_fix(formatted_text)

# Step 4: Extract the last words of each sentence
statements = final_text.split('.')
last_words = [statement.strip().split()[-1] for statement in statements if statement.strip()]
new_statement = ' '.join(last_words).capitalize()

# Step 5: Add the new sentence to the end of the paragraph
final_text = final_text.strip() + ' ' + new_statement + '.'

# Count all whitespace characters
whitespace_count = sum(1 for char in final_text if char.isspace())

# Output the final text and the whitespace count
print(final_text)
print(whitespace_count)