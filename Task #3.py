import re

text = r"""homEwork:
  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

sentences = text.split('. ')

capitalized_sentences = []
for sentence in sentences:
    if sentence:
        formatted_sentence = sentence[0].upper() + sentence[1:].lower()
    else:
        formatted_sentence = sentence
    capitalized_sentences.append(formatted_sentence)

formatted_text = '. '.join(capitalized_sentences)

formatted_text = re.sub(r'\biz\b', 'is', formatted_text)

print(formatted_text)


