# MIT License

# Copyright (c) 2023 Kallol7

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import re
from collections import defaultdict

def clean_middle_punctuation(input_list,punctuation)->list:
    out = []
    for word in input_list:
      if word:
        if punctuation==" " and "্ " in word:
            # don't alter, to prevent interfering with remove_spaced_hosonto function
            return [word]
        out.extend(word.split(punctuation))
    return out

def clean_begin_end_punctuations(word: str) -> str:
    s = word.strip()
    s= word.strip("“‘’””,­")
    while s.startswith("‘") or s.startswith("*") or s.startswith('“'):
        s=s[1:]
    while s.endswith(",") or s.endswith(";"):
        s=s[:-1]
    return s

def clean_punctuations(input_word: str) -> list:
    out = []
    d=defaultdict(list)
    input_word = input_word.replace('”',"’")
    input_word = clean_begin_end_punctuations(input_word)
    punc_list = [',', ';', '।', ' ', "‘", "[", "]", "(", ")", "*", "\\", "/", "{", "}", "$", "+", "-"]
    if not any([punctuation in input_word for punctuation in punc_list]):
        return [input_word]
    
    s=input_word.split(',')
    for punc in punc_list[1:]:
        s = clean_middle_punctuation(s, punctuation=punc)
    for word in s:
      if word:
        out.append(clean_begin_end_punctuations(word))
    return out

def remove_spaced_hosonto(input_word: str) -> str:
    """
    remove spaced hosonto from word
    """
    out = input_word
    word_parts = re.match(r'(.*)্ +(.*)', input_word)
    if word_parts: 
        a,b = word_parts.groups()
        if b.startswith('র') or b.startswith('য'):
            out=a+b
        else:
            out=a+'্'+b
    out = re.sub(r"\u200c", "", out)
    return out
 
def clean_function_by_kallol( words: list ) -> list:
    temp = []
    for word in words:
        s = clean_begin_end_punctuations(word)
        while s.endswith(",") or s.endswith(";"):
            s=s[:-1]
        
        # uncomment to remove spaced hosonto
        s = remove_spaced_hosonto(s)
        if s and len(s)>1:
            cleaned_list = clean_punctuations(s)
            temp.extend(cleaned_list)
    words=temp
    return words

def clean_text(wordList: list) -> list:
    """ ( input: list of strings )
    ##### Input: ['দুই,টা', 'এপার-ওপার', 'যেখানে  সেখানে', 'তোমার-আমার', 'গেল। করিম[রহিমের ভাই]', 'শিগ্ রই', 'হাল্ কা', 'ফক্\u200cফকা', 'থপ্ থপ্', 'রুগ্ ণ রোগী']
    ##### Output: ['দুই', 'টা', 'এপার', 'ওপার', 'যেখানে', 'সেখানে', 'তোমার', 'আমার', 'গেল', 'করিম', 'রহিমের', 'ভাই', 'শিগরই', 'হাল্কা', 'ফক্ফকা', 'থপ্থপ্', 'রুগ্ণ', 'রোগী']
    """
    words = clean_function_by_kallol(wordList)
    return words

if __name__=="__main__":
    _input = ["দুই,টা", "এপার-ওপার", "যেখানে  সেখানে", "তোমার-আমার", "গেল। করিম[রহিমের ভাই]", "শিগ্ রই", "হাল্ কা", "ফক্‌ফকা", "থপ্ থপ্", "রুগ্ ণ রোগী"]
    cleaned = clean_text(_input)
    print()
    print("Input:",_input)
    print("Output:",cleaned)
