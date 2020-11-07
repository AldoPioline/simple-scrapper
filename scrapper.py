from instascrape import *
from custom_scrapper import *

class scrapper:
    def __init__(self, link):   
        self.google_post = Post(link)
        self.google_post.scrape()
      
    def scrape_data(self, basic_info = {},post_type = 'main'):
        # print(self.google_post.__dict__['url'],'llllllllllll')
        basic_info['hashtags'] = self.google_post.hashtags
        basic_info['tagged_users'] = self.google_post.tagged_users
        basic_info['upload_date'] = self.google_post.upload_date.strftime("%m/%d/%Y, %H:%M:%S")
        basic_info['likes'] = self.google_post.likes
        basic_info['caption'] = self.google_post.caption
        basic_info['comments_disabled'] = self.google_post.comments_disabled
        basic_info['location'] = self.google_post.location
        basic_info['display_url'] = self.google_post.display_url
        custom_data = get_metadata(self.google_post.html)
        basic_info['owner_name'] = custom_data['owner.full_name'][0]
        basic_info['username'] = custom_data['owner.username'][0]
        basic_info['followers'] = custom_data['owner.edge_followed_by.count'][0]
        basic_info['comments'] = custom_data['edge_media_to_parent_comment.edges'][0]
        basic_info['post_type'] = post_type
        basic_info['post_id'] = self.google_post.id
        return basic_info
        

    def download_media(self, file_path):
        self.google_post.download(file_path)

    

        

