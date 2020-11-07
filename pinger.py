import urllib
def check_url_live(link):
    try:
        urllib.urlopen(link)
        return True
    except Exception as e:
        return False

