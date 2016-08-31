# -*-coding:utf-8-*-
from spacy.en import English

parser = English()
from itertools import tee, islice
import re
from collections import Counter
import enchant
import requests
import json

d = enchant.Dict("en_US")
from nltk.corpus import stopwords

ratingDict = {}
stop = set(stopwords.words('english'))


def scrorer(Name):
    try:
        ratingDict[Name] += 10
    except KeyError:
        ratingDict[Name] = 10


def duckSearch(searchList,numberOFSeraches):
    """
    :param searchList:
    :param numberOFSeraches:
    :return: list of urls
    """
    query = '+'.join(searchList)
    print 'http://duckduckgo.com/?q=' + query
    response = requests.get('http://duckduckgo.com/i.js?q=' + query + "&t=h_&ia=web", verify=False)
    data = response.text
    data = json.loads(data)
    returnUrlsList=[]
    for i in range (0,numberOFSeraches):
        returnUrlsList.append(data['results'][i]['url'])
    return returnUrlsList


def nameEntitySpacy(multiSentence):
    parsedData = parser(multiSentence)
    sents = []
    for span in parsedData.sents:
        # go from the start to the end of each span, returning each token in the sentence
        # combine each token using join()
        sent = ''.join(parsedData[i].string for i in range(span.start, span.end)).strip()
        sents.append(sent)

    # for sentence in sents:
    #     print(sentence)
    #
    for span in parsedData.sents:
        sent = [parsedData[i] for i in range(span.start, span.end)]
        break

    # parsedEx = parsedData
    # # shown as: original token, dependency tag, head word, left dependents, right dependents
    # for token in parsedEx:
    #     print(
    #     token.orth_, token.dep_, token.head.orth_, [t.orth_ for t in token.lefts], [t.orth_ for t in token.rights])

    # for token in sent:
    #     print(token.orth_, token.pos_)
    # for token in parsedData:
    #     print(token.orth_, token.ent_type_ if token.ent_type_ != "" else "(not an entity)")

    print("-------------- entities only ---------------")
    # if you just want the entities and nothing else, you can do access the parsed examples "ents" property like this:
    ofInterest = []
    ents = list(parsedData.ents)
    for entity in ents:
        # print(entity.label, entity.label_, ' '.join(t.orth_ for t in entity))
        # if(entity.label_ == 'PERSON'):
        ofInterest.append(' '.join(t.orth_ for t in entity))
    print ofInterest
    return ofInterest


def ngrams(lst, n):
    """
    nonEnglishLine = ""
    nonEnglisharray = []
    # print multiSentence.split(" ")
    for line in multiSentence.split(" "):
        if (d.check(line.strip()) == True):
            pass
        else:
            nonEnglisharray.append(line)

    nonEnglishLine = " ".join(nonEnglisharray)
    nonEnglisharray = [i for i in nonEnglishLine.lower().split() if i not in stop]
    nonEnglishLine = " ".join(nonEnglisharray)
    # print nonEnglishLine
    words = re.findall("\w+", nonEnglishLine)
    print Counter(ngrams(words, 1))

    :param lst:
    :param n:
    :return:
    """
    tlst = lst
    while True:
        a, b = tee(tlst)
        l = tuple(islice(a, n))
        if len(l) == n:
            yield l
            next(b)
            tlst = b
        else:
            break


multiSentence = u"""
Rang De Basanti (IPA: [ˈrəŋɡ d̪eː bəˈsənt̪i]; English: Colour it Saffron) is a 2006 Indian drama film co written, co produced and directed by Rakeysh Omprakash Mehra. The literal meaning of the title can be translated as "Paint me with the colours of spring." It features an ensemble cast comprising Aamir Khan, Siddharth Narayan, Soha Ali Khan, Kunal Kapoor, R. Madhavan, Sharman Joshi, Atul Kulkarni and British actress Alice Patten in the lead roles. Made on a budget of ₹250 million (US$3.7 million), it was shot in and around New Delhi. Upon release, the film broke all opening box office records in India. It was the highest-grossing film in its opening weekend in India and had the highest opening day collections for a Bollywood film. The film was well received and praised for strong screenplay and dialogues.

The story is about a British documentary filmmaker who is determined to make a film on Indian freedom fighters based on diary entries by her grandfather, a former officer of the British Indian Army. Upon arriving in India, she asks a group of five young men to act in her film.

Rang De Basanti's release faced stiff resistance from the Indian Defence Ministry and the Animal Welfare Board due to parts that depicted the use of MiG-21 fighter aircraft and a banned Indian horse race.

The film was released globally on 26 January 2006, the Republic Day of India, it received critical acclaim winning National award for most popular film and it is also rated as 8.4 out of 10 on IMDB which is one of the highest among Bollywood films. It was subsequently nominated for Best Foreign Language Film at the 2006 BAFTA Awards. Rang De Basanti was chosen as India's official entry for the Golden Globe Awards and the Academy Awards in the Best Foreign Language Film category, though it did not ultimately yield a nomination for either award. A. R. Rahman's soundtrack, which earned positive reviews, had two of its tracks considered for the Academy Award nomination. The film was well received by critics and audiences for its production values and had a noticeable influence on Indian society. In India, Rang De Basanti did well at many of the Bollywood awards ceremonies, including a win for Best Movie at the Filmfare Awards. The film was declared "Blockbuster" by Box Office India.
"""
# print nameEntitySpacy(multiSentence)[0]



nonEnglishLine = " ".join(nameEntitySpacy(multiSentence))
words = re.findall("\w+", nonEnglishLine)
print Counter(ngrams(words, 2))
parsedData = parser(multiSentence)
sents = []
for span in parsedData.sents:
    # go from the start to the end of each span, returning each token in the sentence
    # combine each token using join()
    sent = ''.join(parsedData[i].string for i in range(span.start, span.end)).strip()
    sents.append(sent)
for i in sorted(Counter(ngrams(words, 2))):
    # print " ".join(i) # got all the relevant names
    for sent in sents:
        if ("directed" in sent.lower() and " ".join(i).lower() in sent.lower()):
            scrorer(" ".join(i))
            print "director", " ".join(i)
print ratingDict
