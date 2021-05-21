import bs4 as bs #Beautifulsoup package
import urllib.request #Fetch url
import nltk #Natural Language tool kit
import re #Regular Expression
scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Machine_learning') #scrap data from web url
article = scraped_data.read() #Read scraped data
parsed_article = bs.BeautifulSoup(article,'lxml') #Parse scraped data
paragraphs = parsed_article.find_all('p') # Use find_all function of the Beautiful Soup object to fetch all contents from the paragraph tags of the article
article_text = ""
for p in paragraphs:
    article_text += p.text #Append all paragraph contents

#Pre-process text
#article_text = re.sub(r'[[0-9]*\]', ' ', article_text) # Substitute numbers, Square Brackets and Extra Spaces with a space
article_text = re.sub(r'[*[0-9]*]', ' ', article_text)
formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text) # Removing anything (like special characters and numbers) other than alphabets
#formatted_article_text = re.sub(r's+', ' ', formatted_article_text)

sentence_list = nltk.sent_tokenize(article_text) #mark the beginning and end of sentence

#Calculate word scores
stopwords = nltk.corpus.stopwords.words('english') #Remove words like is, at, the, etc.,
word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text): #If the word is tokenized
    if word not in stopwords: #and not in stopwords
        if word not in word_frequencies.keys(): #and not part of word frequencies dictionary
            word_frequencies[word] = 1 #then assign the bag of words value as 1
        else:
            word_frequencies[word] += 1 #else add 1 to the existing value
maximum_frequncy = max(word_frequencies.values())
for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy) #TF-IDF formula to obtain weighted word frequency i.e., frequency of the most occuring word
    
#Calculate sentence scores
sentence_scores = {}
for sent in sentence_list: #mark the beginning and end of sentence
    for word in nltk.word_tokenize(sent.lower()): #Tokenize all the words in a sentence
        if word in word_frequencies.keys(): #If the word exists in word_frequences 
            if len(sent.split(' ')) < 30: #if the length of sentences is less than 30
                if sent not in sentence_scores.keys():#If the sentence is not occuring frequently in the over all article
                    sentence_scores[sent] = word_frequencies[word] #then add word frequency to sentence score
                else:
                    sentence_scores[sent] += word_frequencies[word]#else add 1 to the existing value

#Print Summary:
import heapq #priority queue algorithm to sort sentences with top n largest score
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get) #Get sentence score; sort sentences based on the sentence score. Please note to count sentences ending with . and not the no of lines reading the output
summary = ' '.join(summary_sentences) #Join sentences in a paragraph format to present as a summary
print(summary) #print summary as output