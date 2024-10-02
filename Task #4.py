# Module 2
import random
import string


def generate_random_dicts():
    dict_count = random.randint(2, 10)
    num_keys = random.randint(1, len(string.ascii_lowercase))
    return [
        {random.choice(string.ascii_lowercase): random.randint(0, 100) for _ in range(num_keys)}
        for _ in range(dict_count)
    ]


def update_common_dict(common_dict, current_dict, index):
    for key, value in current_dict.items():
        if key in common_dict:
            if value > common_dict[key][0]:
                common_dict[key] = (value, f"{key}_{index + 1}")
        else:
            common_dict[key] = (value, f"{key}_{index + 1}")


def create_final_dict(common_dict):
    return {new_key: value for key, (value, new_key) in common_dict.items()}


def main():
    random_dicts = generate_random_dicts()
    print( random_dicts)

    common_dict = {}
    index = 0

    for current_dict in random_dicts:
        update_common_dict(common_dict, current_dict, index)
        index += 1  # Manually increment the index

    final_dict = create_final_dict(common_dict)
    print(final_dict)


# Call the main function directly
main()

#Module 3
import re


def normalize_case(sentences):
    return [
        (sentence[0].upper() + sentence[1:].lower()) if sentence else sentence
        for sentence in sentences
    ]


def fix_mistakes(text):
    return re.sub(r'\biz\b', 'is', text)


def extract_last_words(sentences):
    return [
        statement.strip().split()[-1] for statement in sentences if statement.strip()
    ]


def count_whitespace(text):
    return sum(1 for char in text if char.isspace())


def main(text):
    sentences = text.split('. ')

    # Step 1: Normalize case
    capitalized_sentences = normalize_case(sentences)

    # Step 2: Join sentences
    formatted_text = '. '.join(capitalized_sentences)

    # Step 3: Fix "iz" to "is"
    formatted_text = fix_mistakes(formatted_text)

    # Step 4: Extract last words and create new sentence
    last_words = extract_last_words(formatted_text.split('.'))
    new_statement = ' '.join(last_words).capitalize()

    # Step 5: Add new sentence to the end
    final_text = formatted_text.strip() + ' ' + new_statement + '.'

    # Count whitespace characters
    whitespace_count = count_whitespace(final_text)

    return final_text, whitespace_count


# Original text
text = r"""homEwork:
  tHis iz your homeWork, copy these Text to variable.

  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

  last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

# Call the main function and print results
final_text, whitespace_count = main(text)
print(final_text)
print(whitespace_count)