from scrapper import *
import pandas as pd
from instascrape import *
import os
import sys
from tqdm import tqdm
import traceback
import pymongo
from datetime import datetime
from pinger import check_url_live
import shutil


if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["instagram"]
    mycol = mydb["influencers"]
    filename = sys.argv[-1]
    path = os.getcwd()
    df = pd.read_excel(filename)
    if not os.path.exists(os.path.join(path,'instagram')):
        os.mkdir(os.path.join(path,'instagram'))
    else:
        pass
    with tqdm(total=len(df)) as pbar:
        for i,j in tqdm(df.iterrows()):
            basic_info ={'pinged_dates':[datetime.now().strftime("%m/%d/%Y, %H:%M:%S")],'date_taken_down':''}
            dest = os.path.join(path,'instagram',str(j['global_user_id']))
            if j['network'] == 'instagram':
                basic_info['campaign_id'] = j['campaignId']
                basic_info['brandid'] = j['brandId']
                basic_info['post_link'] = j['post_link']
                basic_info['global_user_id'] = j['global_user_id']
                try:
                    if not os.path.exists(os.path.join(path,'instagram',str(j['global_user_id']))):
                        os.mkdir(os.path.join(path,'instagram',str(j['global_user_id'])))
                    if not os.path.exists(os.path.join(path,'instagram',str(j['global_user_id']),str(basic_info['campaign_id']))):
                        os.mkdir(os.path.join(path,'instagram',str(j['global_user_id']),str(basic_info['campaign_id'])))
                    if not os.path.exists(os.path.join(path,'instagram',str(j['global_user_id']),str(basic_info['campaign_id']),'main_campaign')):
                        os.mkdir(os.path.join(path,'instagram',str(j['global_user_id']),str(basic_info['campaign_id']),'main_campaign'))
                    
                    dest = os.path.join(path,'instagram',str(j['global_user_id']),str(basic_info['campaign_id']))
                    
                    scrapper_obj = scrapper(j['post_link'])
                    
                    basic_data = scrapper_obj.scrape_data(basic_info, post_type='main')
                    if mycol.find({'global_user_id':j['global_user_id'], 'campaign_id':j['campaignId'], 'post_link':j['post_link']}).count():
                        print('exists!')
                        continue
                    x = mycol.insert_one(basic_data)
                    if scrapper_obj.google_post.is_video:
                        new_dest = os.path.join(dest,'main_campaign','video.mp4')
                        scrapper_obj.download_media(new_dest)
                    scrapper_obj.download_media(os.path.join(dest,'main_campaign','image.jpg'))
                    
                    user_link = 'https://www.instagram.com/'+basic_data['username'] + '/'
                    links = get_links(user_link)
                    for i in links:
                        scrapper_obj = scrapper(i)
                        user_info = {'pinged_dates':[datetime.now().strftime("%m/%d/%Y, %H:%M:%S")],'date_taken_down':''}
                        user_info['campaign_id'] = None
                        user_info['brandid'] = j['brandId']
                        user_info['global_user_id'] = j['global_user_id'] 
                        user_info['post_link'] = i
                        next_data = scrapper_obj.scrape_data(user_info, post_type='other') 
                        x = mycol.insert_one(next_data)
                        
                        if not os.path.exists(os.path.join(dest,next_data['post_id'])):
                            os.mkdir(os.path.join(dest,next_data['post_id']))
                        
                        r = requests.get(scrapper_obj.google_post.display_url, stream = True)
                        if scrapper_obj.google_post.is_video:
                            scrapper_obj.download_media(os.path.join(dest,next_data['post_id'],'video.mp4'))
                        new_dest = os.path.join(dest,next_data['post_id'],'image.jpg')
                        with open(new_dest,'wb') as f:
                            shutil.copyfileobj(r.raw, f)
                        
                    
                except Exception as e:
                    print( traceback.format_exc())
                    if not check_url_live(j['post_link']):
                        basic_info['date_taken_down'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                


