import os
import string
from collections import Counter
import nltk
import pandas as pd

# #NOTE:: Run these command to extract data using spider 
# #       Avoid, if already done.
# import subprocess
# project_path="dataExtraction"
# subprocess.Popen(["scrapy","crawl","harvester","-o","harvestedfiles.json"],shell=True, cwd=project_path)


nltk.download('punkt', download_dir=r"VirtualEnv\nltk_data")
nltk.download('stopwords', download_dir=r"VirtualEnv\nltk_data")

from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords



def syllable_count_per_word(word):
    #lower 
    word=word.lower()
    #vowels
    vowels = "aeiouy"
    number_of_syllables = 0
        
    if word[0] in vowels:
        number_of_syllables=number_of_syllables+1
        
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            number_of_syllables=number_of_syllables+1
        
    if word.endswith("e"):
        number_of_syllables=number_of_syllables-1
    
    if word.endswith("ed"):
        number_of_syllables=number_of_syllables-1
        
    if word.endswith("es"):
        number_of_syllables=number_of_syllables-1

    if number_of_syllables == 0:
        number_of_syllables=number_of_syllables+1
            
    return number_of_syllables

# Storing all words in a single stop token file
stop_words = []

stop_words_path = "StopWords"
stop_words_file_paths = os.listdir(stop_words_path)

for stop_words_file_path in stop_words_file_paths:
    f = open(r"StopWords\{}".format(str(stop_words_file_path)))
    text = f.read()
    cleanedText = text.translate(str.maketrans('','',string.punctuation))
    tokenizedText = cleanedText.split()
    stop_words.extend(tokenizedText)
    f.close()

# Updating master dictionary for sentiment analysis
master_dict = {"negative_words" : [],
               "positive_words" : []}

master_dict_negative_path = r"MasterDictionary\negative-words.txt"
master_dict_positive_path = r"MasterDictionary\positive-words.txt"

f = open(master_dict_negative_path)
tokenizedText = f.read().lower().split()
master_dict["negative_words"] = list(set(tokenizedText) - set(stop_words))
f.close()

f = open(master_dict_positive_path)
tokenizedText = f.read().lower().split()
master_dict["positive_words"] = list(set(tokenizedText) - set(stop_words))
f.close()

        
df = pd.read_excel("Output Data Structure.xlsx")
files_dir_path = "dataExtraction\Extracted files"
for file_number in df.iloc[:, 0]:
    try:
        file_path = str(file_number) +".txt"
        f = open(r"{}\{}.txt".format(files_dir_path, str(file_number)), 'r', encoding="utf-8")
        text = f.read()
        cleanedText = text.lower().translate(str.maketrans('','',string.punctuation))
        tokenizedText = word_tokenize(cleanedText, "english")


        # Sentimental Analysis

        finalWords = []
        for word in tokenizedText:
            if word not in stop_words:
                finalWords.append(word)

        negative_score = 0
        positive_score = 0
        final_word_count = 0
        for word in finalWords:
            final_word_count += 1
            if word in master_dict["positive_words"]:
                positive_score += 1
            elif word in master_dict["negative_words"]:
                negative_score -= 1

        negative_score *= -1

        polarity_score = (positive_score - negative_score)/((positive_score + negative_score)+0.000001)  
        subjectivity_score = (positive_score + negative_score)/(final_word_count+0.000001)

        # Readability analysis

        sentences = sent_tokenize(text,"english")
        sentence_count = len(sentences)
        words_per_sentence = sum([len(word_tokenize(sentence)) for sentence in sentences])/sentence_count
        words = tokenizedText
        total_word_count = len(tokenizedText)
        average_sentence_length = total_word_count/sentence_count
        nltk_filtered_words = [word for word in tokenizedText if word not in stopwords.words("english")]
        word_count = len(nltk_filtered_words)
        complex_words = []
        total_syllables_in_words = 0
        personal_pronouns_def = ['I',"we","my","ours","us","Ours","our","Us","We","My"]
        personal_pronouns = []
        character_count = 0
        for word in words:
            total_syllables_in_words += syllable_count_per_word(word)
            character_count += len(word)
            if syllable_count_per_word(word)>2:
                complex_words.append(word)
            if word in personal_pronouns_def:
                personal_pronouns.append(word)
            
        complex_word_count = len(complex_words)
        percentage_complex_words = complex_word_count/total_word_count
        fog_index = 0.4 * (average_sentence_length + percentage_complex_words)
        personal_pronouns_desc = Counter(personal_pronouns)
        personal_pronouns_count = sum(personal_pronouns_desc.values())
        average_character_count = character_count/total_word_count

        df.loc[df["URL_ID"] == file_number, "POSITIVE SCORE"] = positive_score
        df.loc[df["URL_ID"] == file_number, "NEGATIVE SCORE"] = negative_score
        df.loc[df["URL_ID"] == file_number, "POLARITY SCORE"] = polarity_score
        df.loc[df["URL_ID"] == file_number, "SUBJECTIVITY SCORE"] = subjectivity_score
        df.loc[df["URL_ID"] == file_number, "AVG SENTENCE LENGTH"] = average_sentence_length
        df.loc[df["URL_ID"] == file_number, "PERCENTAGE OF COMPLEX WORDS"] = percentage_complex_words
        df.loc[df["URL_ID"] == file_number, "FOG INDEX"] = fog_index
        df.loc[df["URL_ID"] == file_number, "AVG NUMBER OF WORDS PER SENTENCE"] = words_per_sentence
        df.loc[df["URL_ID"] == file_number, "COMPLEX WORD COUNT"] = complex_word_count
        df.loc[df["URL_ID"] == file_number, "WORD COUNT"] = word_count
        df.loc[df["URL_ID"] == file_number, "SYLLABLE PER WORD"] = total_syllables_in_words/total_word_count
        df.loc[df["URL_ID"] == file_number, "PERSONAL PRONOUNS"] = personal_pronouns_count
        df.loc[df["URL_ID"] == file_number, "AVG WORD LENGTH"] = average_character_count

        f.close()

    except Exception as ex:
        print(ex)
    
df.to_excel("Output Data Structure.xlsx")



# NOTE:: Support for json file reading 
# import json
# db = json.load(open(r"dataExtraction\harvestedfiles.json", encoding="utf-8"))
# df = pd.DataFrame.from_dict(db)
