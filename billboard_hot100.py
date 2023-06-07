import requests
import datetime 
from bs4 import BeautifulSoup
import pymysql

artists_list= ["Miley Cyrus", "Selena Gomez",   "Ariana Grande"  ]
#["Miley Cyrus", "Selena Gomez", "The Weekend", "The Weeknd", "Ariana Grande", "Taylor Swift" ]

dic = {}

conn = pymysql.connect(host='127.0.0.1', port=3307, user='root', passwd='5555', db='tst1', charset='utf8')
cur = conn.cursor()

now = datetime.datetime.now()
now -= datetime.timedelta(days=now.weekday())
delta = datetime.timedelta(weeks=1)

print( now.strftime("%Y-%m-%d" ) )

while True :

    now -= delta     
    
    nowadays = now.strftime("%Y-%m-%d" )
    print(nowadays)
    
    if now.strftime("%Y") < "2010" :
        break

    dic[nowadays] = []

    r = requests.get("https://www.billboard.com/charts/hot-100/" + nowadays  )



    soup = BeautifulSoup(r.text,features="html.parser")

    lis = soup.findAll('li', attrs = {'class':'o-chart-results-list__item'})

    rank = 1

    for idx, li in enumerate(lis) :
        if idx % 14 == 3 :
            cur.execute( 'insert into tbbillboardtopten values ( "'+ nowadays+ '", ' + str(rank)  + ', "' + li.h3.text.strip()[0:100] + '" , "' + li.span.text.strip()[0:50]+ '" ) '  )            
            rank +=1
            for art in artists_list :
                if art in li.span.text.strip() :
                    dic[nowadays].append( (art, li.h3.text.strip() ) )
                    

        if rank > 10 :
            conn.commit()
            break

cur.close()
conn.close()

for key in dic.keys() :
    if len(dic[key]) >= 3 :
        songs = [ v[1] for v in dic[key] ] 
        if len(set(songs)) >= 3 :        
            print (key, dic[key])