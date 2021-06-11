import sqlite3
import re
import itertools
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import json


def page_url(url):
    a=[]
    for x in range(1,20):
        a.append(url+str(x))
    return a

def get_page(a):
    m=[]
    for i in a:
        #print('for page ',i)
        response=requests.get(i)
        if not response.ok:
            print("Server Responded ",response.status_code)
        else:
            print("Server responded for page ",i)
            soup=BeautifulSoup(response.content , 'lxml')
            m.append(get_detail(soup))
    print("type is : ",type(m[1]))
    print("printing data for :",m[1])
    new_df = pd.concat(m)
    #print("data format",type(new_df))
    print("Data Collected :",new_df)
    return new_df

def get_detail(soup):
    title = soup.find_all('h3',{'class':'s-item__title'})
    price = soup.find_all('span',{'class':'s-item__price'})
    rating = soup.find_all('span',{'class':'s-item__reviews-count'})
    sold = soup.find_all('span',{'class':'BOLD NEGATIVE'})

    a={
        'Title' : list(t.text for t in title),
        'Price' : list(p.text.strip('$') for p in price),
        'Rating' : list(re.sub('[^0-9]', '', r.text) for r in rating),
        'Sold' : list(re.sub('[^0-9]', '', s.text) for s in sold)
    }
    b = pd.DataFrame.from_dict(a,orient='index')
    b = b.transpose()
    print('records collected - ',b.shape)
    return b


def save_to_db(new_df):
    x = input("Do you want to save it in DataBase ? \nEnter yes or no : ")
    if x == 'yes':
        conn = sqlite3.connect('Ebay1.db')
        c = conn.cursor()

        print("Give different table name while accessing second time otherwise it will give Error. ")
        print("Give table name accordingly which category you have selected earlier.\nTry to give a number after it to make it more accurate .")
        y = input("Enter Table name : ")
        c.execute('CREATE TABLE {} (Title text, Price number, Rating number, Sold number )'.format(y))
        conn.commit()

        df = DataFrame(new_df, columns=['Title', 'Price','Rating','Sold'])       #pass dataframe
        df.to_sql('{}'.format(y), conn, if_exists='replace', index=False)        #pass DB table
        print('Data stored in the Database . ')
        c.execute(''' SELECT * FROM {} '''.format(y))

        print("Records are : ....")
        for row in c.fetchall():
            print(row)
        z=input("Do you want to export data as csv :\nEnter yes or no : ")
        if z=='yes':
            # save sqlite table in a DataFrame
            df = pd.read_sql('SELECT * from {}'.format(y), conn)
            # write DataFrame to CSV file
            m=input("Enter the name of the csv file to save : ")
            df.to_csv('{}.csv'.format(m), index=False)
            print("CSV exported successfully .... ")
        else:
            print('Thanks ...........')
        conn.close()
    else:
        print("Thanks.....")

def main():
    url={
        'url_mobile' : 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=mobile&_sacat=15032&_ipg=200&_pgn=',
        'url_watch' : 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=watch&_sacat=0&_pgn=',
        'url_game' : 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=video+games&_sacat=1249&_pgn=',
        'url_laptop' : 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=laptops&_sacat=58058&_pgn=',
        'url_headphone':'https://www.ebay.com/sch/i.html?_from=R40&_nkw=headphones&_sacat=0&_pgn=',
        'url_audio':'https://www.ebay.com/sch/i.html?_from=R40&_nkw=audio&_sacat=0&_pgn=',
        'url_tv':'https://www.ebay.com/sch/i.html?_from=R40&_nkw=television&_sacat=0&_pgn=',
        'url_vehicle':'https://www.ebay.com/sch/i.html?_from=R40&_nkw=vehicle&_sacat=0&_pgn=',
        'url_smart_home':'https://www.ebay.com/sch/i.html?_from=R40&_nkw=smart+home&_sacat=0&_pgn='
    }

    print(" Type 1 for Mobile\n Type 2 for watch \n Type 3 for Video Game \n Type 4 for PC and Laptops \n Type 5 for Headphones \n Type 6 for Audio Speaker \n Type 7 for TV \n Type 8 for Electronic Vehicle \n Type 9 for Smart Home ")
    a=int(input("What do you what to get : "))
    print("Wait content is loading .... ")
    if a==1:
        save_to_db(get_page(page_url(url['url_mobile'])))
    if a==2:
        save_to_db(get_page(page_url(url['url_watch'])))
    if a==3:
        save_to_db(get_page(page_url(url['url_game'])))
    if a==4:
        save_to_db(get_page(page_url(url['url_laptop'])))
    if a==5:
        save_to_db(get_page(page_url(url['url_headphone'])))
    if a==6:
        save_to_db(get_page(page_url(url['url_audio'])))
    if a==7:
        save_to_db(get_page(page_url(url['url_tv'])))
    if a==8:
        save_to_db(get_page(page_url(url['url_vehicle'])))
    if a==9:
        save_to_db(get_page(page_url(url['url_smart_home'])))

if __name__ == '__main__':
    main()