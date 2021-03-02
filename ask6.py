import tweepy
import re

#Στοιχεια συνδεσης στο Twitter API

consumer_key='your_consumer_key'
consumer_secret='your_consumer_secret'
access_token='your_access_token'
access_token_secret='your_access_token_secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Κεντρική συνάρτηση ανάλυσης δεδομένων χρήστη
def useranalysis():
    #Επιλογή χρήστη
    selectuser=input("\nSelect a twitter username: @")
    try:
        user = api.get_user(selectuser)
        # (Optional feature): General Stats
        print("\nSelected User: ",user.name)
        print("Verified: ",user.verified)
        print("Followers: ",user.followers_count)
        print("Total tweets: ",user.statuses_count)
        print("Total no. of liked posts: ",user.favourites_count)
        print("Profile created in: ",user.created_at)
        # (Optional feature): Shows recent tweets
        interest=input("\nDo you want to see the user's 10 latest tweets?(Y/N): ")
        if interest=="Y" or interest=="y":
            print("\nLatest tweets:\n")
        else:
            print("\nAlright! Here are some more interesting stats then:\n")
        #Calls Twitter API με return τα πρωτα 10 tweets,retweets,replies
        public_tweets = api.user_timeline(id=user.id,count=10,tweet_mode = 'extended')
        words=[]
        for tweet in public_tweets:
            #Λαμβάνουμε το πλήρες κείμενο των tweet/retweet
            if hasattr(tweet, 'retweeted_status'):
                tweet=tweet.retweeted_status.full_text
            else:
                tweet=tweet.full_text
            if interest=="Y" or interest=="y":
                print("\n",tweet,"\n")
                print("-------------------------------------")
            wordcompiler(words,tweet)
        if user.statuses_count!=0:
            wordpresenter(words)
        else:
            print(" Whoops! No tweets found from this user")
    #Εαν ο χρήστης δεν υπάρχει,η συνάρτηση κανει fall back στην περίπτωση except
    except tweepy.error.TweepError:
        if selectuser!=".exit":
            print("\nThis user does not exist")
    #Επιστρέφεται το selectuser για να γίνει ο έλεγχος εξόδου
    return selectuser

#Συνάρτηση που εισάγει σε πίνακα τις λέξεις του tweet
def wordcompiler(userwordarray,tweet):
    txt=tweet
    #1ο φιλτράρισμα : Αφαίρεση URL
    txt=re.sub("http\S+", "", txt)
    #2ο φιλτράρισμα : Αφαίρεση username
    txt=re.sub("@\S+", "", txt)
    #3ο φιλτράρισμα : Αφαίρεση των hashtag
    txt=re.sub("#\S+", "", txt)
    #4o φιλτράρισμα : Αφαίρεση ειδικών χαρακτήρων και αριθμων
    txt=re.sub("[^a-zA-Z]+"," ",txt)
    #5ο φιλτράρισμα : Αφαίρεση των single letter εκτός των a και i που θεωρουνται λεξεις
    txt=re.sub(r"\b[^A,a,I,i,]\b", " ", txt)
    #Διαχωρισμός σε list λέξεων
    txt=txt.split()
    #Προσθήκη των λέξεων του tweet στο array των λέξεων
    i=0
    while i<len(txt):
        userwordarray.append(txt[i])
        i+=1

def wordpresenter(userwordarray):
    #Αφαίρεση των duplicates
    words=list(set(userwordarray))
    words=sorted(words, key=len)
    print ("The five biggest words this user has used in their last 10 tweets:\n")
    for i in range(-5,5):
        print (words[i])
        if i==-1:
            print ("\nCompared to the five smallest:\n")

#Κεντρικό μπλόκ κώδικα
print("\nWelcome to my tweet analyser! Made with love :)")
print("To exit,simply enter .exit as a username")
select=useranalysis()
while select!=".exit":
    select=useranalysis()
