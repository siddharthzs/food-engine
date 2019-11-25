import sqlite3
import os
import nltk
import string
from mysite.settings import BASE_DIR


from nltk.stem.porter import PorterStemmer

import pickle
# nltk.download('punkt')
stemmer = PorterStemmer()


def partition(x):
    if x < 3:
        return "negative"
    return "positive"


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    #tokens = [word for word in tokens if word not in stopwords.words('english')]
    stems = stem_tokens(tokens, stemmer)
    return ' '.join(stems)


def train():
    con = sqlite3.connect('database.sqlite')
    messages = pd.read_sql_query("""SELECT Score, Summary FROM Reviews WHERE Score != 3""", con)
    Score = messages['Score']
    Score = Score.map(partition)
    Summary = messages['Summary']
    X_train, X_test, y_train, y_test = train_test_split(Summary, Score, test_size=0.1, random_state=42)

    
    intab = string.punctuation
    outtab = "                                "
    trantab = str.maketrans(intab, outtab)


    corpus = []
    for text in X_train:
        text = text.lower()
        text = text.translate(trantab)
        text=tokenize(text)
        corpus.append(text)
        
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(corpus)        
        
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    
    model = MultinomialNB().fit(X_train_tfidf, y_train)

    filename1 = 'foodreviewmodel.pkl'
    filename2 = 'foodreviewvector.pkl'
    filename3 = 'foodreviewtfidf.pkl'

    with open(filename1, 'wb') as f:
        pickle.dump(model,f)
    
    with open(filename2, 'wb') as f:
        pickle.dump(count_vect,f)

    with open(filename3, 'wb') as f:
        pickle.dump(tfidf_transformer,f)





def predictfood(foodlist):
    intab = string.punctuation
    outtab = "                                "
    trantab = str.maketrans(intab, outtab)

    xtest = []
    for text in foodlist:
        text = text.lower()
        text = text.translate(trantab)
        text=tokenize(text)
        xtest.append(text)

    f1 = str(os.path.join(BASE_DIR,''))
    f2 = f1+"\\foodreviewmodel.pkl"
    f3 = f1 + "\\foodreviewvector.pkl"
    f4 = f1 + "\\foodreviewtfidf.pkl"
    with open(f2,'rb') as f:
        loadmodel = pickle.load(f)
    
    with open(f3,'rb') as f:
        loadvector = pickle.load(f)
    
    with open(f4,'rb') as f:
        loadtfidf = pickle.load(f)


    X_train_counts = loadvector.transform(xtest)        
        
   
    s = loadtfidf.transform(X_train_counts)


    result = loadmodel.predict(s)
    x = sum([1 for i in result if i == 'positive'])
    return (x/len(result))*4.7



# train()
ans = predictfood(['good food','tasty food', 'ugly','great','fabolous','hate it','lovely','sweet','total waste','tasteless','salty'])
print(ans)




    