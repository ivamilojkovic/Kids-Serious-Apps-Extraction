import pandas as pd


df=pd.read_csv('Google-Playstore.csv')

#####################################################################################################################
####FOR PERFORMANCE ASSESSMENT####
ref=open('reference.txt', 'r')
lines=ref.readlines()

df1=pd.DataFrame(columns=['App Name', 'App Id', 'Category', 'Rating', 'Rating Count', 'Installs', 'Minimum Installs', 'Maximum Installs', 'Free', 'Price', 'Currency', 'Size', 'Minimum Android', 'Developer Id', 'Developer Website', 'Developer Email', 'Released', 'Last Updated', 'Content Rating', 'Privacy Policy', 'Ad Supported', 'In App Purchases', 'Editors Choice', 'Scraped Time'])
for line in lines:
    x=line.split('\n')
    x=x[0]
    print(x)
    df2=df.loc[df['App Id']==x]
    df1=pd.concat([df2, df1])
print(df1.shape)
#out of 160 apps, only 156 were found in kaggle database
df1.to_csv('156apps.csv')
#####################################################################################################################


#print(df.head())
#print several rows
#print(df.loc[0])
#print(df.loc[[0,10], :])

#categories we are interested in: 
#Board, Card, Education, Educational, Parenting, Productivity, Puzzle, Role Playing, Strategy

#Education NB: 15 minutes to run just this :/ 1239 elements at this point for rate 3.5 without min installs
education_df=df.loc[df['Category']=='Education']
education_df=education_df.loc[df['Rating']>=3.7]
education_df=education_df.loc[df['Rating Count']>=100000]
education_df=education_df.loc[df['Minimum Installs']>=100]

#Educational
educational_df=df.loc[df['Category']=='Educational']
educational_df=educational_df.loc[df['Rating']>=3.7]
educational_df=educational_df.loc[df['Rating Count']>=100000]
educational_df=educational_df.loc[df['Minimum Installs']>=100]

#Puzzle
puzzle_df=df.loc[df['Category']=='Puzzle']
puzzle_df=puzzle_df.loc[df['Rating']>=3.7]
puzzle_df=puzzle_df.loc[df['Rating Count']>=100000]
puzzle_df=puzzle_df.loc[df['Minimum Installs']>=100]

#Strategy
strategy_df=df.loc[df['Category']=='Strategy']
strategy_df=strategy_df.loc[df['Rating']>=3.7]
strategy_df=strategy_df.loc[df['Rating Count']>=100000]
strategy_df=strategy_df.loc[df['Minimum Installs']>=100]

#####################################################################################################################
####FOR PERFORMANCE ASSESSMENT####
#df=pd.concat([education_df, educational_df, puzzle_df, strategy_df])
#15 serious games, meeting the above mentioned requirements, out of 156
#####################################################################################################################

#creation of the database that will store apps' info
from tinydb import TinyDB
db=TinyDB('./Ourdatabase.json')

###APIs -> json files
from google_play_scraper import app
import json
import  urllib.request
import urllib.parse
from bs4 import BeautifulSoup

#####################################################################################################################
#loop on education apps
IDs=education_df[["App Id"]]

for i in range(education_df.shape[0]):
    #print(IDs.iloc[i-1,0])

    existing=1
    try:
        response = urllib.request.urlopen("https://play.google.com/store/apps/details?id="+IDs.iloc[i-1,0])
    except urllib.error.HTTPError as exception:
        print(exception)
        existing=0

    if existing==1:
        result = app(IDs.iloc[i-1,0], lang='en', country='us')
        #json_result=json.dumps(result)
        #json_result=json.loads(json_result)
        #print(json_result)
        #print(json_result['title'])
        #print(result, "\n" )
        db.insert(result)

#####################################################################################################################
#loop on educational apps
IDs=educational_df[["App Id"]]

for i in range(educational_df.shape[0]):
    existing=1
    try:
        response = urllib.request.urlopen("https://play.google.com/store/apps/details?id="+IDs.iloc[i-1,0])
    except urllib.error.HTTPError as exception:
        print(exception)
        existing=0

    if existing==1:
        result = app(IDs.iloc[i-1,0], lang='en', country='us')
        db.insert(result)

#####################################################################################################################
#loop on puzzle apps
IDs=puzzle_df[["App Id"]]

for i in range(puzzle_df.shape[0]):
    existing=1
    try:
        response = urllib.request.urlopen("https://play.google.com/store/apps/details?id="+IDs.iloc[i-1,0])
    except urllib.error.HTTPError as exception:
        print(exception)
        existing=0

    if existing==1:
        result = app(IDs.iloc[i-1,0], lang='en', country='us')
        db.insert(result)

#####################################################################################################################
#loop on strategy apps
IDs=strategy_df[["App Id"]]

for i in range(strategy_df.shape[0]):

    existing=1
    try:
        response = urllib.request.urlopen("https://play.google.com/store/apps/details?id="+IDs.iloc[i-1,0])
    except urllib.error.HTTPError as exception:
        print(exception)
        existing=0

    if existing==1:
        result = app(IDs.iloc[i-1,0], lang='en', country='us')
        db.insert(result)
#####################################################################################################################

#for item in db: 
    #print(item)


#once we have the db, we can enrich it with another API: play_scraper
import play_scraper

def ISIN(string, database):
    for item in database:
        if item['appId']==string:
            return(1)
    return(0)

#print(ISIN("ru.yandex.translate", db)) #returns 1 since it is already in db
#print(ISIN("com.combo.matcher", db)) # returns 0 since it is not in db 

#gosh, we need to filter the apps according to the same parameters than before
query="serious game"
answer=play_scraper.search(query)
for item in answer:
    print(item['app_id'])
    if ISIN(item['app_id'],db)==0: #mean the item is not in the db
        result = app(item['app_id'], lang='en', country='us')
        if result['score']>3.5 :
            if result['minInstalls']>100:
                db.insert(result)

query = 'game ADHSD'
answer=play_scraper.search(query)
for item in answer:
    print(item['app_id'])
    if ISIN(item['app_id'],db)==0: #mean the item is not in the db
        result = app(item['app_id'], lang='en', country='us')
        if result['score']>3.5 :
            if result['minInstalls']>100:
                db.insert(result)

query = 'serious game ADHD'
answer=play_scraper.search(query)
for item in answer:
    print(item['app_id'])
    if ISIN(item['app_id'],db)==0: #mean the item is not in the db
        result = app(item['app_id'], lang='en', country='us')
        if result['score']>3.5 :
            if result['minInstalls']>100:
                db.insert(result)

#at this point we updated the db with new apps obtained from specific queries
#####################################################################################################################
#delete columns 

from tinydb.operations import delete
db.update(delete('descriptionHTML'))
db.update(delete('summaryHTML'))
db.update(delete('free'))
db.update(delete('currency'))
db.update(delete('saleTime'))
db.update(delete('originalPrice'))
db.update(delete('saleText'))
db.update(delete('offersIAP'))
db.update(delete('androidVersionText'))
db.update(delete('developerAddress'))
db.update(delete('developerInternalID'))
db.update(delete('icon'))
db.update(delete('headerImage'))
db.update(delete('screenshots'))
db.update(delete('video'))
db.update(delete('recentChangesHTML'))
db.update(delete('videoImage'))

#####################################################################################################################
#first element of the db?
db.all()[0]



#####################################################################################################################
#creating the reference db
import play_scraper
ref_list=[]

query = 'game for children'
answer=play_scraper.search(query, page=2)
for item in answer:
    print(item['app_id'])
    ref_list.append(item['app_id'])

query='games'
answer=play_scraper.search(query, page=2)
for item in answer:
    print(item['app_id'])
    if ref_list.count(item['app_id'])==0:
        ref_list.append(item['app_id'])

query='game'
answer=play_scraper.search(query, page=2)
for item in answer:
    print(item['app_id'])
    if ref_list.count(item['app_id'])==0:
        ref_list.append(item['app_id'])

query='children games'
answer=play_scraper.search(query, page=2)
for item in answer:
    print(item['app_id'])
    if ref_list.count(item['app_id'])==0:
        ref_list.append(item['app_id'])

query='education games'
answer=play_scraper.search(query, page=2)
for item in answer:
    print(item['app_id'])
    if ref_list.count(item['app_id'])==0:
        ref_list.append(item['app_id'])

len(ref_list)

import pandas as pd    
ref_df = pd.DataFrame(ref_list)
ref_df.to_csv('ref_to_be_labeled.csv', index=False)

#####################################################################################################################
#EVALUATING THE PERFORMANCE OF THE ALGORITHM
#the few lines above randomly chose applications from certain fields, without filtering whether they are serious or not.
#we automatically simulated what we would have done if we had randomly searched for games.
#That way we have a lot of apps and we avoid repetition...

#These randomly chosen application are contained in the following file:
import numpy as np

ref=pd.read_excel('156refApps.xlsx')

#we could have passed the file through the whoel code but we realized all the apps were containedin the google play csv file used at the beginning of the code
#so we are just going to check if the apps are returned at the end of the code

# If they are returned, the code says they are positive. 
# Depending on label we assign to them, they will be either false positive or true positive, since our labelling is supposed to be the gold standard.
ref=ref.assign(AutomaticScore=pd.Series(np.random.randn(156)).values)

for index, row in ref.iterrows():
    print(row['AppID'])
    if ISIN(row['AppID'], db)==1:
        ref.at[index,'AutomaticScore']=1
    else:
        ref.at[index,'AutomaticScore']=0

ref.to_csv('156refApps_results.csv', index=False)

TP_count=0
FP_count=0
TN_count=0
FN_count=0

#computing TP, FP, FN, TN
ref=ref.assign(Class='What')

for index, row in ref.iterrows():
    if row['AutomaticScore']==1: #gold standard positive
        if row['Scores']==1:
            ref.at[index,'Class']='TP'
            TP_count=TP_count+1
        else:
            ref.at[index,'Class']='FP'
            FP_count=FP_count+1
    else:
        if row['Scores']==0:
            ref.at[index,'Class']='TN'
            TN_count=TN_count+1
        else:
            ref.at[index,'Class']='FN'
            FN_count=FN_count+1


#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#Looking for publications on serious games

###################################
#read the serious games' dictionary
fp=open('keywords_context.txt', 'r')
lines=fp.readlines()
KeyWords=list()

for line in lines:
    x=line.split('\n')
    KeyWords.append(x[0])
fp.close()
print(*KeyWords)

###################################
#read the study design's dictionary
fp=open('keywords_studydesign.txt', 'r')
lines=fp.readlines()
EvidenceLevel=list()

for line in lines:
    x=line.split('|')
    x=x[1]
    x=x.split('\n')
    EvidenceLevel.append(x[0])
fp.close()
print(*EvidenceLevel)

#########################################################################
class publication:
    url = ""
    abstract=""

    def __init__(self, in_url):
        self.url=in_url

        page=urllib.request.urlopen(self.url)
        soup=BeautifulSoup(page, 'lxml')
        abs=soup.find(id="abstract")
        self.abstract=abs.get_text(' ')
        print('\n The instance was built.')

    def display_abstract(self): 
        print(self.abstract)

    def count_overall_occurancies(self):
        abs=self.abstract
        abs=abs.lower()
        sum=0
        for w in KeyWords:
            count=abs.count(w)
            sum=sum+count
        return(sum)
    
    def KeyWords_Found_in_Abstract(self):
        abs=self.abstract
        kw=[]
        for w in KeyWords:
            if w in abs.lower():
                kw.append(w)
        return(kw)

    def Number_of_different_keywords(self):
        return(len(self.KeyWords_Found_in_Abstract()))

    def study_quality(self):
        abs=self.abstract
        abs=abs.lower()
        sd=[]
        for w in EvidenceLevel:
            wl=w.lower()
            if w in abs or wl in abs:
                sd.append(w)
        return(sd)


#########################################################################
import  urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from pymed import PubMed

#pubmed = PubMed(tool='ehealth_group00', email='my@email.address')
pubmed = PubMed(tool='ehealth_group14')

results = pubmed.query('Vedantu: LIVE Learning App', max_results=100)
#papers = []

for res in results:
    paper_info=res.toDict() #each element of the papers list is a dictionary class
    id=paper_info["pubmed_id"]
    if len(id)>10:
        id=id.split('\n')
        id=id[0]
    print(id)
    paper=publication("https://pubmed.ncbi.nlm.nih.gov/"+id+"/")
    nb=paper.count_overall_occurancies()
    kw=paper.KeyWords_Found_in_Abstract()
    nb_diff=paper.Number_of_different_keywords()
    sd=paper.study_quality()
    print('The global occurancy of keywords is', nb)
    print('\n')
    print('The keywords found in the abstract are the following:', kw)
    print('\n')
    print('The words characterizing the level of evidence and found in the abstract are the following:', sd)
    print('\n _____________________________________ \n')

#the function returns pubmed id, the title, the entire abstract, keywords, methods (sometimes null), conclusions and results
#the url can be found using: https://pubmed.ncbi.nlm.nih.gov/INSERT_THE_ID_OF_THE_PUBLICATION/

#NB: sometimes, pubmed id may have this form. '34746753\n13155707\n32272089\n30630920\n33707215\n24855259\n30212458\n32109011',
#manage the error

#Recall on the objective:

# development of autmatic methods to extract information from pubmed webpages
# select relevant publications and make a DB
# automated methods to characterize publications

#idea. 
# 1.Search evidence on specific games ; 
# 2.extract info from pubmed text ; 
# 3. characterize the app