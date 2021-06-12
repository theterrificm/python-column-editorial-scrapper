from typing import final
from flask import Flask, request, render_template
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as urlReq
import datetime



app = Flask(__name__)




@app.route('/')
def hello_world():
    return 'hello'

@app.route('/scrapper', methods=['POST', 'GET'])
def scrape():
    if request.method == 'POST':
        fromDate = request.form['from']
        toDate = request.form['to']
        content_type = request.form['type']
        fromDate = fromDate.split('-')
        toDate = toDate.split('-')
        fromDay = int(fromDate[2])
        
        toDay = int(toDate[2])
        result = ''
        while fromDay <= toDay:
            sss = str(fromDay)
            if len(sss) == 1:
                sss = '0' + sss

            page_url = 'https://www.dawn.com/newspaper/'+ content_type +'/'+ fromDate[0] + '-' + fromDate[1] + '-' + sss

            client = urlReq(page_url)

            page_soup = soup(client.read(), "html.parser")

            client.close();

            content = page_soup.findAll('article', {'class': 'story'})

            

            for content_text in content:
                title_name = content_text.h2.text
                title_link = content_text.h2.a['href']
                title_excerpt = content_text.div.text
                currentDay = str(fromDay) +'-'+ str(fromDate[1])+'-'+ str(fromDate[0])
                result += '<div class="py-3 border-bottom"><span class="badge rounded-pill bg-light text-dark px-1">'+ currentDay +'</span><span class="pb-3 border-secondary"><h1>'+ title_name +'</h1><p>'+ title_excerpt +'</p><a class="btn btn-light" target="_blank" href="'+ title_link +'">Click here</a></span></div>' 
                
            fromDay+= 1    

        
            # x = datetime.datetime(fromDate)

        return  render_template('boiler.html', hell= result) 
    return 'yeah'



if __name__ == '__main__':
    app.run()