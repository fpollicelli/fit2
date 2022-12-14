from instaloader import Instaloader, Profile
from argparse import ArgumentParser
from glob import glob
from os.path import expanduser
from platform import system
from sqlite3 import OperationalError, connect

try:
    from instaloader import ConnectionException, Instaloader
except ModuleNotFoundError:
    raise SystemExit("Instaloader not found.\n  pip install [--user] instaloader")

def postScraper(user,directory):
    completedir = directory+'/'+user
    loader = Instaloader(dirname_pattern=completedir)
    profile = Profile.from_username(loader.context, user)
    posts = profile.get_posts()
    for post in posts:
        loader.download_post(post, user)
    return

def storyScraper(user, directory):
    completedir = directory + '/' + user
    loader = Instaloader(dirname_pattern=completedir)

    try:
        loader.download_stories("kyliejenner")
    except Exception as e:
        print(e)

    return


def get_cookiefile():
    default_cookiefile = {
        "Windows": "~/AppData/Local/Microsoft/Edge/User Data/Profile 1/Network/Cookies", #.sqlite?
        "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
    }.get(system(), "~/.Microsoft/Edge/*/Cookies")
    cookiefiles = glob(expanduser(default_cookiefile))
    if not cookiefiles:
        raise SystemExit("No Edge cookies.sqlite file found. Use -c COOKIEFILE.")
    return cookiefiles[0]


def import_session(cookiefile, sessionfile):
    print("Using cookies from {}.".format(cookiefile))
    conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
    try:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
        )
    except OperationalError:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
        )

    instaloader = Instaloader(max_connection_attempts=1)
    instaloader.context._session.cookies.update(cookie_data)
    username = instaloader.test_login()
    if not username:
        raise SystemExit("Not logged in. Are you logged in successfully in Firefox?")
    print("Imported session cookie for {}.".format(username))
    instaloader.context.username = username
    instaloader.save_session_to_file(sessionfile)

    try:
        instaloader.download_stories("kyliejenner")
    except Exception as e:
        print(e)

