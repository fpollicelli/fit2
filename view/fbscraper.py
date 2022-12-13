from facebook_page_scraper import Facebook_scraper

#TODO: in costruzione

page_name = "metaai"
posts_count = 10
browser = "firefox"
proxy = "IP:PORT" #if proxy requires authentication then user:password@IP:PORT
timeout = 600 #600 seconds
headless = True
meta_ai = Facebook_scraper(page_name, posts_count, browser, proxy=proxy, timeout=timeout, headless=headless)
meta_ai.scrap_to_csv('priv.csv')