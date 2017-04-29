import twitter
import secrets
import re

class TwitMiner:
    def __init__(self):
        self.api =     twitter.Api(consumer_key = secrets.consumer_key,
                  consumer_secret = secrets.consumer_secret,
                  access_token_key = secrets.access_token_key,
                  access_token_secret = secrets.access_token_secret)

    def clean_tweet(self, tweet):
        text = re.sub(r"^https?:\/\/.*[\r\n]*", '', tweet, flags=re.MULTILINE)
        return ' '.join(re.sub("(@[A-Za-z]+)|([^A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

    def get_hashes(self, tweet_text):
        hashes = [s for s in tweet_text.split() if (s[0]=='#')]
        nhashes=[]
        for shash in hashes:
            nhash=[]
            for ch in shash:
                if(ch=='#'):
                    nhash+="%23"
                else:
                    nhash+=self.clean_tweet(ch)
            nhashes.append(''.join(nhash))
        return nhashes

    def get_tweets(self, username):
        numofload=5
        statuses = self.api.GetSearch(raw_query = "q=from%3A" + username + "&lang=en&count=" + str(numofload))
        #statuses = self.api.GetUserTimeline(screen_name = username, count = 200)
        iterations = min(statuses[0].user.statuses_count // numofload, 16)
        statuses = [s for s in statuses if '#' in s.text]
        for i in range(0,iterations):
            lastId = statuses[-1].id
            nst = self.api.GetSearch(raw_query = "q=from%3A" + username + "&max_id="+str(lastId)+"&lang=en&count="+str(numofload))
            q = [s for s in nst if '#' in s.text]
            statuses += q
            if len(statuses)>=numofload:
                break
        statuses_text = [(s.text) for s in statuses]
        st_hashes = [self.get_hashes(s) for s in statuses_text]
        statuses_text = [self.clean_tweet(s.text) for s in statuses]
        hash_stat =[]
        for h in st_hashes:
            for i in h:
                t=[]
                if len(i)>0:
                    it_data = self.api.GetSearch(raw_query = "q=twitter%20 +" + i + "&lang=en&count="+str(50))
                    t = [self.clean_tweet(s.text) for s in it_data]
                hash_stat.append(t)
        return statuses_text, hash_stat

    def eng_tweets(self, statuses):
        result = []
        for status in statuses:
            if status.lang == "en":
                result.append(status)
        return result

uname = "jayzclassicbars"

gtw = TwitMiner()
tw,htw = gtw.get_tweets(uname)


################ list (tuple(sentimental, list(keywords )))

from gensim import corpora, models, similarities

#Notw = 6 # NoTwit
TwitParametres = []

############################### KeyWords

tokenize = lambda doc: doc.lower().split(" ")

for Notw in range(len(tw)):
    if (len(htw[Notw]) == 0):
        continue
    tokenized_documents = [tokenize(d) for d in htw[Notw]] # tokenized docs
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
    dictionary = corpora.Dictionary(tokenized_documents)
    
    corpus = [dictionary.doc2bow(text) for text in tokenized_documents]
    
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics = 3)
    
    doc = tw[Notw]
    vec_bow = dictionary.doc2bow(doc.lower().split())
    vec_lsi = lsi[vec_bow] 
    
    index = similarities.MatrixSimilarity(lsi[corpus])
    sims = index[vec_lsi]
    
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    i = 0
    counterHtw = 0
    counterRT = 0 
    TextCorp = ""
    while ((sims[i][1] > 0.25) and (i<len(htw[Notw])-1)) and (counterHtw < 10):
            if (str(htw[Notw][sims[i][0]])[0:2] != 'RT'):
                TextCorp += (str(htw[Notw][sims[i][0]]) + "\n \n")
                counterHtw += 1
#                print(i)
            else:
                if (counterRT < 1):
                    TextCorp += (str(htw[Notw][sims[i][0]])[2:] + "\n \n")
                    counterRT += 1
                    counterHtw += 1
    #                print(i)
            i+= 1
#            print(counterHtw)
    #print(Notw)
    TextCorp += str(tw[Notw])      
     
    import textrank
    keywords = list(textrank.extract_key_phrases(textrank.extract_sentences(TextCorp)))
    
    ###################### Sentimental
    
    from textblob import TextBlob
    
    sentimental = (TextBlob(tw[Notw])).sentiment
    sent = sentimental[0]*(1-sentimental[1])
     
    ######################
    SoloTwit = [sent, keywords]
    TwitParametres.append(SoloTwit)
#print (TwitParametres)

################################### Music predict

#nltk
from nltk.corpus import wordnet
import pandas as pd
import numpy as np

df = pd.read_csv("TrackBase5Album2_coeff2.csv", header = 0)
dflist = np.array(df.values.flatten()).reshape(len(df.index), 5)
#
#synonymos
lemmas = []
rast = []
tmp = [] 
ans = []
ansForTwit = []
#print(lemmas)
#print(wordnet.synset('small.n.01').path_similarity(wordnet.synset('dog.n.01')))
#for twit in range(lenT)
for keys in range(len(TwitParametres)):
    lemmas.clear()
    for kw in TwitParametres[keys][1]:
        try:
            #print(str(keys) + ' ' + str(wordnet.synset(kw+'.n.01')))
            lemmas.append(wordnet.synset(kw + '.n.01'))
            #print(wordnet.synset(kw + '.n.01').name().split('.')[0])
        except:
            continue

    rast.clear()
    tmp.clear()
    ans.clear
    bufftmp = 0
    for theme in range(len(dflist)):
        st_to_sim = str(dflist[theme][0]).lower().split('/')[0]
        sets_sim = wordnet.synsets(str(st_to_sim))   
        for set_sim in sets_sim:
            for lem in lemmas:
                tmp.append(set_sim.path_similarity(lem))
        tmp = list(filter(None.__ne__,tmp))
        if len(tmp) != 0:
            buff = max(tmp)
            tmp.clear()
            rast.append([buff, theme, dflist[theme][2]])
    rast = sorted(rast)
    if len(rast) == 0:
        continue
    buff = rast[-1][0]
    
    for i in range(len(rast)):
        if rast[i][0] == buff:
            ans.append(rast[i])
    for i in range(len(ans)):
        ans[i][2]-=TwitParametres[1][0]
    ans = sorted(ans, key=lambda ans: -ans[2])
    ansForTwit.append([keys, dflist[ans[0][1]][3],dflist[ans[0][1]][4]])






