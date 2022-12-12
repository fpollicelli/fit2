from instaloader import Instaloader, Profile

def postScraper(user,directory):
    completedir = directory+'/'+user
    loader = Instaloader(dirname_pattern=completedir)
    profile = Profile.from_username(loader.context, user)
    posts = profile.get_posts()
    for post in posts:
        loader.download_post(post, user)
    return
