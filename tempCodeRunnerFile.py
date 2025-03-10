

url = "https://www.youtube.com/watch?v=9LNv_mFERwI&list=PL6K-pApFohn-5LWvDr2YAd8Z9Bol0mxv8&index=1&ab_channel=VaniaJunco"
def Playlist(url):
    word = 0
    indexnum = ""
    if "index=" in url: 
        word = url.find("index=")
    elif "radio=" in url:
        word = url.find("radio=")
    else: 
        return 2
    
    while True:
        i = 0
        if url[word + 6 + i] >= '0' and url[word + 6 + i] <= '9':
            indexnum = indexnum + url[word + 6 + i]
        else:
            break
    print(indexnum)