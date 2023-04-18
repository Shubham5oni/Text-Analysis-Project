from bs4 import BeautifulSoup as Soup
from nltk.tokenize import word_tokenize
from textstat.textstat import textstatistics

import requests
import os
import re

path = os.getcwd()  # this method returns current working directory.
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}  # an HTTP header that can be used in an HTTP request to provide information about the client browser and more.

url = input('Give article link:')
r = requests.get(url, headers=header)  # this method requests data from the url.

soup = Soup(r.text, "html.parser")  # Soup() reads the response of the url.
contents = soup.body.find_all(['h1', 'h2', 'h3', 'p']) + soup.find_all(class_="_s30J clearfix")
text = ''
for content in contents:
    text = text + ' ' + content.get_text()

# reads the Stopwords provided.
with open("Stopwords.txt") as f:
    stop_words = f.read()

# for WORD COUNT
words = re.findall("[a-zA-Z-]+", text)
number_of_words = len(words)

# for AVG WORD LENGTH
total_characters = 0
for word in words:
    total_characters += len(word)
Average_Word_Length = total_characters/number_of_words

# for SYLLABLE PER WORD
vowels = 0
for word in words:
    if word.endswith("es") or word.endswith("ed"):
        vowels -= 1
        for char in word:
            if char in "aeiouAEIOU":
                vowels += 1
    else:
        for char in word:
            if char in "aeiouAEIOU":
                vowels += 1
total_syllables_count = vowels
Avg_Syllable_Per_Word = total_syllables_count/number_of_words

# for AVG SENTENCE LENGTH
sents = re.split("[.!?]+", text)
number_of_sents = len(sents)-1
Avg_Sent_Length = number_of_words/number_of_sents

# for PERCENTAGE OF COMPLEX WORDS and COMPLEX WORD COUNT
list_of_complex_words = []
for word in words:
    syllable_count = textstatistics().syllable_count(word)
    if word not in stop_words and syllable_count > 2:
        list_of_complex_words.append(word)
Complex_Words_Count = len(list_of_complex_words)
Per_Complex_Words = Complex_Words_Count / number_of_words * 100

# for PERSONAL PRONOUNS
personal_pronouns = re.findall(r'\b(I|we|my|ours|(?-i:us))\b', text, re.IGNORECASE)
Count_of_Personal_Pronouns = len(personal_pronouns)

# for FOG INDEX
Fog_Index = 0.4 * (Avg_Sent_Length + Per_Complex_Words)

# cleaning text for Sentiment Analysis
word_tokens = word_tokenize(text)  # tokenize the string using 'nltk' library.
clean_text = [x for x in word_tokens if x not in stop_words]  # excludes the words found in Stop Word List from the text

# for POSITIVE SCORE
Positive_Score = 0
with open("positive-words.txt") as f:
    positive_words = f.read().split()
    for word in clean_text:
        if word in positive_words:
            Positive_Score = Positive_Score+1

# for NEGATIVE SCORE
Negative_Score = 0
with open("negative-words.txt") as f:
    negative_words = f.read().split()
    for word in clean_text:
        if word in negative_words:
            Negative_Score = Negative_Score-1
    Negative_Score = Negative_Score*-1

# for POLARITY SCORE
Polarity_Score = (Positive_Score - Negative_Score)/((Positive_Score + Negative_Score) + 0.000001)

# for SUBJECTIVITY SCORE
Subjectivity_Score = (Positive_Score + Negative_Score)/((len(clean_text)) + 0.000001)


print('\nWarning: Be careful while giving a file name in below input because '
      'it can overwrite an existing text file if the same name is given.')
filename = f"{path}\Generated Result files\{input('Enter a name for the generated text file:')}.txt"
with open(filename, 'w', encoding="utf-8") as textfile:
    textfile.write(f"The article url: {str(url)}"'\n\n')
    textfile.write(f"Web article content: {text}"'\n\n')
    textfile.write('Analysis Results-''\n\n')
    textfile.write(f"The word count is: {number_of_words}"'\n\n')
    textfile.write(f"Average word length is: {Average_Word_Length}"'\n\n')
    textfile.write(f"Average number of syllables per word is: {Avg_Syllable_Per_Word}"'\n\n')
    textfile.write(f"Average number of words per sentence is: {Avg_Sent_Length}"'\n\n')
    textfile.write(f"The count of complex words is: {Complex_Words_Count}"'\n\n')
    textfile.write(f"The complex words percentage is: {Per_Complex_Words}"'\n\n')
    textfile.write(f"The count of personal pronouns is: {Count_of_Personal_Pronouns}"'\n\n')
    textfile.write(f"The Fog Index is: {Fog_Index}"'\n\n')
    textfile.write(f"The positive score is: {Positive_Score}"'\n\n')
    textfile.write(f"The negative score is: {Negative_Score}"'\n\n')
    textfile.write(f"The polarity score is: {Polarity_Score}"'\n\n')
    textfile.write(f"The subjectivity score is: {Subjectivity_Score}"'\n\n')
