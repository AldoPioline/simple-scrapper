# supreme_scrapper
***PYTHON 3 IS REQUIRED FOR THE PROJECT***
File descriptions:
  main.py - Contains the main code that controls the flow
  scrapper.py - Contains modules to scrape data using instascrapper
  custom_scrapper.py - Custom scrapping modules that overrides scrapper 

The python package Instagram-scrapper does not support all the necessary operations that we need. So I have written an addtional module that does the needed operations.


Running format: 
pip install -r requirements.txt (Only for the first time)
python main.py <file_name>


Once the scrapping is done,
You can find the images stored in the following schema order under the directory instagram/
instagram/ user_id / campaign_id / image_id
Other metadata is stored in mongoDB with the following format
{user_id:xxx , campaign_id:xxx , metadata_1:xxx, metadata_2:xxx, ...., metadata_n:xxx}

You can visualize the data stored with the find() method in pymongo.
