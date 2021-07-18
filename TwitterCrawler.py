import tweepy,sys,jsonpickle

consumer_key = '' # masukkan consumer_key yang didapat dari akun Twitter Developer
consumer_secret = '' # masukkan consumer_secret yang didapat dari akun Twitter Developer

qry='covid-19 indonesia -RT' # masukkan query yang akan dicari
maxTweets =  1000 # masukkan banyaknya tweets yang ingin dihasilkan. isi nilai sesuai kebutuhan 
tweetsPerQry = 100  
fName='covid19-indo.json' # menyimpan data hasil crawling ke dalam file json

auth = tweepy.AppAuthHandler(consumer_key,consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

if (not api):
    sys.exit('Autentifikasi gagal, mohon cek "Consumer Key" & "Consumer Secret" dari akun Developer Twitter Anda.')

sinceId, max_id, tweetCount = None, -1, 0

print("Mulai mengunduh maksimum {0} tweets".format(maxTweets))
with open(fName,'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets=api.search(q=qry,count=tweetsPerQry)
                else:
                    new_tweets=api.search(q=qry,count=tweetsPerQry,since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets=api.search(q=qry,count=tweetsPerQry,max_id=str(max_id - 1))
                else:
                    new_tweets=api.search(q=qry,count=tweetsPerQry,max_id=str(max_id - 1),since_id=sinceId)
            if not new_tweets:
                print('Tidak ada tweet yang ditemukan dengan Query = "{0}"'.format(qry));break
            for tweet in new_tweets:
                f.write(jsonpickle.encode(tweet._json,unpicklable=False)+'\n')
            tweetCount+=len(new_tweets)
            sys.stdout.write("\r");sys.stdout.write("Jumlah tweets telah tersimpan: %.0f" %tweetCount);sys.stdout.flush()
            max_id=new_tweets[-1].id
        except tweepy.TweepError as e:
            print("Some error : " + str(e));break
print ('\nSelesai! {0} Tweets tersimpan di "{1}"'.format(tweetCount,fName))