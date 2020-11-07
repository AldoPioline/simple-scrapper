import pandas as pd
import os
import requests
from bs4 import BeautifulSoup as bs
import time
import re
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np
from tqdm import tqdm
import sys
from lxml.html import fromstring
import lxml.html as PARSER
from selenium import webdriver
from selenium.webdriver.chrome.options import Options




def is_not_ascii(string):
    if type(string) == str:
        try:
            return string is not None and any([ord(s) >= 128 for s in string])
        except:
            pass
    else:
        return string

# def get_image(photo_url, dest_path):
#     if not os.path.exists(dest_path):
#         os.mkdir(dest_path)
#     else:
#         # print 'Dir exists, skipping'
#         pass
#     content = photo_url["content"]
#     photo_name = content[-25:-6]
#     requests_url = requests.get(content)
#     f = open(os.path.join(dest_path,'image.jpg'), 'ab')
#     f.write(requests_url.content)
#     f.close()

def get_metadata(soup):
    try:
        # soup = bs(soup.read(),features="lxml")
        soup = PARSER.fromstring(soup)
        body = soup.find('body')
        script = body.find('script')
        raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
        json_data=json.loads(raw)
        posts =json_data['entry_data']['PostPage'][0]['graphql']
        posts= json.dumps(posts)
        posts = json.loads(posts)
        x = pd.DataFrame.from_dict(json_normalize(posts), orient='columns') 
        x.columns = x.columns.str.replace("shortcode_media.", "")
        return x.to_dict()
        # x.to_csv(os.path.join(path,'instagram',str(j['global_user_id']),'metadata.csv'), index=False,encoding='utf-8')    
    except Exception as e:
        print('Exception occured in row', e)

def get_links(username):
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    browser = webdriver.Chrome('/Users/mac/Downloads/chromedriver-2',options=op)
    browser.get(username)
    Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    links=[]
    source = browser.page_source
    data=bs(source, 'html.parser')
    body = data.find('body')
    script = body.find('script', text=lambda t: t.startswith('window._sharedData'))
    page_json = script.string.split(' = ', 1)[1].rstrip(';')
    data = json.loads(page_json)
    for link in data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
        links.append('https://www.instagram.com'+'/p/'+link['node']['shortcode']+'/')
    return links



    
if __name__ == '__main__':
    
    path = '/Users/mac/Documents/projects/instagram_scrapper/'
    if not os.path.exists(os.path.join(path,'instagram')):
        os.mkdir(os.path.join(path,'instagram'))
    else:
        # print 'Dir exists, skipping'
        pass
    filename = sys.argv[-1]
    df = pd.read_excel(filename)
    with tqdm(total=len(df)) as pbar:
        for i,j in tqdm(df.iterrows()):
            if j['network'] == 'instagram':
                try:
                    response = requests.get(j['post_link'])
                    html = response.text
                except Exception as e:
                    print('Oops! Unable to fetch image',e)
                    continue
                
                dest = os.path.join(path,'instagram',str(j['global_user_id']))
                soup = bs(html, 'lxml')
                photo_url = soup.find("meta", property="og:image")
                get_image(photo_url, dest)
                get_metadata(soup)
                pbar.update(1)
            

