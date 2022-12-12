from pytube import YouTube

def videoScraper(url,directory):
    video = YouTube(url)
    video.streams.get_highest_resolution().download(directory)
    return
