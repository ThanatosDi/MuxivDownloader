import requests
from bs4 import BeautifulSoup
import os,sys

playlist = 'https://muxiv.com/tc/playlist/832533149'

def source(url):
    """回傳HTML"""
    html = requests.get(url=url)
    html.encoding = 'utf-8'
    htmlcode = BeautifulSoup(html.text, "html.parser")
    return htmlcode
def songs(playlist):
    """取得playlist中的每首歌網址"""
    html = source(playlist)
    songs = {}
    for song in html.find_all('a',{'class':r'flexlist flex-center'}):
        songs[song.text] = f'https://muxiv.com{song["href"]}'
    return songs
def playlistname(playlist):
    """回傳playlist標題"""
    html = source(playlist)
    return html.find('h1',{'class':'mint-header-title'}).text
def song_download_link(songurl):
    """取得歌曲的下載連結"""
    html = source(songurl)
    return html.find('a',{'class':'mn_list'})['href']
def download(playlist):
    """從json取得網址並進行下載歌曲動作"""
    songsjson = songs(playlist)
    songs_title = songsjson.keys()
    dirname = playlistname(playlist)
    for song_title in songs_title:
        if songsjson[song_title] is not None:
            resp = requests.get(song_download_link(songsjson[song_title]))
            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            with open(f'{dirname}/{song_title}.mp3', "wb") as code:
                code.write(resp.content)
                print(f' {song_title} downloading...')

if __name__ == '__main__':
    while True:
        Enter = input('輸入 Muxiv playlist 網址:')
        if Enter.lower()=='exit':
            sys.exit()
        if Enter.lower()=='help':
            print(' help    幫助清單\n exit    離開本程式')
            continue
        if Enter.find('muxiv.com/tc/playlist/')==-1:
            print('>> 請輸入正確的 Muxiv playlist 網址')
            continue
        download(Enter)