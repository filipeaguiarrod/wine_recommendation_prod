import string
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords


def clean_text(text):
    
    #text = str(text)

    text = text.lower()
    text = text.strip()
    text = text.replace('-','')
    text = ' '.join(text.split()).strip()
    
    return text

def remove_stopwords(text):
    
    text = str(text).lower()
    
    # Define the stopwords in portuguese
    stopwords_pt = set(stopwords.words('portuguese'))
    # Tokenize the text
    words = nltk.word_tokenize(text)
    # Remove the stopwords
    filtered_words = [word for word in words if word.lower() not in stopwords_pt]
    
    # Remove punctuation and special characters
    filtered_words = [word for word in filtered_words if word.isalnum()]
    
    # Remove numbers
    filtered_words = [word for word in filtered_words if not word.isnumeric()]
    
    # Join the filtered words
    filtered_text = ' '.join(filtered_words)
    return filtered_text


def wine_clean(x):
    
    """
    Foco em limpar o nome de vinhos inseridos, removendo 
    informações sobressalentes e não ligadas ao nome do vinho.    
    """
    
    
    x = x.lower()

    not_year = re.compile(r'\b(?!20\d{2}|\d{4})\d+\b')
    
    not_year2 = re.compile(r'\b\d{4}\b')
    
    not_name = re.compile(r'\b(vinho|ml|lata|em|garrafa)\b')
    
    volumn_ml = re.compile(r"\d+ml")
    
    # remove the numbers of length 3 from the string
    x = not_year.sub("", x)
    x = not_year2.sub("", x)
    x = not_name.sub("", x)
    x = volumn_ml.sub("", x)
    
    x = x.strip()

    return x

def clean_teor(x):
    
    """
    Dado um valor de teor alcoólico subistitui carcteres especiais e retorna 
    """
    
    x=str(x)
    
    #x = x.replace('°','')
    #x = x.replace('°|ª','')
    
    
    regex = r'[^\d,.]'
    
    # replace any character that matches the pattern with an empty string
    x = re.sub(regex,'', x)
    
    x=float(x)
    
    while x<10:
        
        x = x*10
        
    return x

def extract_numbers_and_average(text):
    # extract all groups of digits separated by non-numeric characters
    numbers = [int(match) for match in re.findall(r'\d+', text)]
    
    return np.mean(numbers)
    