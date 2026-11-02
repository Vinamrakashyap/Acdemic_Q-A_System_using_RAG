#1. Maan lo PDF se extracted text aisa aa raha hai:
#"" Introduction     to Machine Learning


#Machine Learning   is a subset
#of Artificial Intelligence.


#It uses algorithms    to learn patterns.""
#Notice karo:
#- Words ke beech unnecessary spaces hain.
#- Multiple blank lines hain.
#- Text mein inconsistent formatting hai.
#Agar hum is text ko directly chunk karenge, toh unnecessary whitespace bhi chunks mein jayega.
#2. Yahan re ka role aata hai
#Regular Expressions ki help se hum specific text patterns identify karke unhe replace kar sakte hain.

#Python mein re.sub() iska important function hai.
import re

def clean_text(text):
    #remove nul characters
    text = text.replace("\x00","")

    #replace multiple spaces and tabs with a single space
    text = re.sub("[ \t]+"," ", text)

    #replace multiple new lines with a single new line
    text = re.sub(r"\n+", "\n",text)

    #remove leading and trailing whitespaces
    text = text.strip()

    return text
