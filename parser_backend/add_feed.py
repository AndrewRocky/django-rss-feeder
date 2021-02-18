import feedparser as fparser

from parser_backend.models import Feed, Post
from datetime import datetime
from parser_backend.update_feeds import update_feed


def convert_time_to_datetime(struct_time_input):
    #return datetime.datetime(*structime[:6]) #easy way, error if leapsecond
    return datetime(*struct_time_input[:5]+(min(struct_time_input[5], 59),))


def new(input_url):
    current_time = datetime.utcnow() #get current time in UTC timezone
    #first prepare url:
    final_url = str(input_url)
    if not (final_url.startswith("http://") or final_url.startswith("https://")):
        final_url = "https://" + final_url
    
    feed = fparser.parse(final_url)
    if feed.feed == {}:
        #    ERROR wrong feed url - logging here
        return "Error: wrong feed url"
    
    actual_url = feed.url
    
    #check if this Feed is already in database
    all_feeds = Feed.objects.all()
    all_feeds_urls = [old_feed.url for old_feed in all_feeds]
    if actual_url in all_feeds_urls:
        #   ERROR - this feed is already in database
        return "Error: this feed is already in database"

    if "title" in feed.feed:
        title = feed.feed.title
    else:
        title = feed.url
    if "description" in feed.feed:
        description = feed.feed.description
    else:
        description = title
    if "icon" in feed.feed:
        picture = feed.feed.icon
    elif "logo" in feed.feed:
        picture = feed.feed.logo
    else: picture = "static/images/default_feed.ico"

    if "published" in feed:
        last_mod_feed = convert_time_to_datetime(feed.published_parsed)
    elif "updated" in feed:
        last_mod_feed = convert_time_to_datetime(feed.updated_parsed)
    else:
        last_mod_feed = current_time
    
    new_feed = Feed(
        url = actual_url,
        title=title,
        description = description,
        picture = picture,
        last_modified = last_mod_feed,
        last_updated = current_time,
        is_available = True
    )
    print(last_mod_feed)
    print(current_time)
    new_feed.save()

    is_new_posts = update_feed(actual_url)
    
    return is_new_posts


    
    







if __name__ == "__main__":
    pass