from pytube import YouTube

def videoScraper(url,directory):
    video = YouTube(url)
    video.streams.get_highest_resolution().download(directory)
    return
def infoScraper(url):
    video = YouTube(url)
    title = video.title
    views = video.views
    length = video.length
    rating = video.rating
    thumburl = video.thumbnail_url
    row = title+','+views+','+length+','+rating+','+thumburl
    return row