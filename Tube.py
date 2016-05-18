from bs4 import BeautifulSoup as bs
import urllib.request
from pytube import YouTube
import re
# make function to fetch video_links from pages
# make function to fetch video_qualities in which it is available
# make function to user asked selection to get selected
# download that video

def fetch_video_links(url):

    try:
        page = urllib.request.urlopen(url)
    except ValueError:
        print("URl seems to be incorrect")
        return None

    page = bs(page, "html.parser")
    bs_page = page.find_all('a',{'class':'yt-uix-sessionlink'})
    href = []
    for link in bs_page:
        if('/watch' in link.get('href').split('?')):
            href.append(link.get('href'))
    links = []
    for values in href:
        links.append('https://www.youtube.com'+values)
    return links

def fetch_video_qualtiy(url):
    yt = YouTube(url)
    videos = list()
    for element in yt.get_videos():
        videos.append(element)
    return videos

def user_select(list):
    print('select the desired qualtiy')
    count = 0
    for element in list:
        print(count, element)
        count+=1
    selected_quality = int(input())
    return selected_quality

url ='http://www.youtube.com/watch?v=Ik-RsDGPI5Y'

all_videos_links = fetch_video_links(url)
#print(all_videos_links)

qual = fetch_video_qualtiy(all_videos_links[2])
print(str(qual[0]))
value = re.search("(- \d{3,4}[p] -)",str( qual[4]))
print(str(qual[4])[value.span()[0]+2:value.span()[1]-2])
