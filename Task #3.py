import re

text = r"""homEwork:
  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

sentences = text.split('. ')

capitalized_sentences = []
for sentence in sentences:
    if sentence:
        formatted_sentence = sentence[0].upper() + sentence[1:].lower()
    else:
        formatted_sentence = sentence
    capitalized_sentences.append(formatted_sentence)

formatted_text = '. '.join(capitalized_sentences)


words = formatted_text.split()
for i in range(len(words)):
    if words[i].lower() == "iz":
        if i > 0 and words[i - 1].lower() == "fix":
            continue
        words[i] = "is"

# Step 4: Extract the last words of each sentence
statements = formatted_text.split('.')
last_words = [statement.strip().split()[-1] for statement in statements if statement.strip()]
new_statement = ' '.join(last_words)
new_statement = new_statement.capitalize()

# Step 5: Add the new sentence to the end of the paragraph
final_text = formatted_text.strip() + ' ' + new_statement + '.'

whitespace_count = sum(1 for char in final_text if char.isspace())

print (final_text)
print (whitespace_count)


