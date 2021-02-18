import feedparser as fparser
from time import localtime
from datetime import datetime

from parser_backend.models import Feed, Post

def convert_time_to_datetime(struct_time_input):
    #return datetime.datetime(*structime[:6]) #easy way, error if leapsecond
    return datetime(*struct_time_input[:5]+(min(struct_time_input[5], 59),))


#update a single feed.
def update_feed(feed_url):
    #we might need to use value_from_object() and value_to_string()
    new_feed_parsed = fparser.parse(feed_url)

    #   !!!!!input HTTP status exception handler here!!!!!! (i'm too lazy right now)

    #take feed that is being updated
    current_feed = Feed.objects.get(url=feed_url) #we'll need it for parent_feed key and to update info about this Feed

    #use ForeignKey in Posts to retrieve posts from selected feed
    #post_list = Post.objects.filter(parent_feed=feed)

    #test: get list of posts using lookups
    post_list = Post.objects.filter(parent_feed__url=feed_url)
    #test2: create cache
    #[old_post for old_post in post_list]
    ##after this our QuerySet is cached and all further access to it will not trigger database activity
    #lets get our guid list to exclude old posts from new
    guid_list = [post.guid for post in post_list]
    
    current_time = datetime.utcnow() #get current time in UTC timezone
    is_new_posts_found = False
    for new_post_parsed in new_feed_parsed.entries: #get each entry in feed
        if not(new_post_parsed.id in guid_list): #if this post is not in database (this part can be ~3 times more efficient)
            is_new_posts_found = True

            if "title" in new_post_parsed:
                title = new_post_parsed.title
            else:
                title = "Article name not found."
            
            if "published" in new_post_parsed:
                published = convert_time_to_datetime(new_post_parsed.published_parsed)
            elif "updated" in new_post_parsed:
                published = convert_time_to_datetime(new_post_parsed.updated_parsed)
            else:
                published = current_time
            
            if "link" in new_post_parsed:
                post_url = new_post_parsed.link
            else:
                post_url = feed_url
            
            if "guid" in new_post_parsed:
                new_guid = new_post_parsed.id
            else:
                if "link" in new_post_parsed:
                    new_guid = new_post_parsed.link
                else:
                    new_guid = title
            #needs descriptions/content[] support
            #needs enclosures support
            #did you know that rss supports textforms? but why?
                
            new_post = Post(
                is_read = False,
                title=new_post_parsed.title,
                release_date = published,
                url = post_url,
                is_starred = False,
                parent_feed = current_feed,
                guid = new_guid
            )
            new_post.save()
        else:
            #what to do with post if it's not new
            pass
    
    #update feed information
    if "published" in new_feed_parsed:
        last_mod_feed = convert_time_to_datetime(new_feed_parsed.published_parsed)
    elif "updated" in new_feed_parsed:
        last_mod_feed = convert_time_to_datetime(new_feed_parsed.updated_parsed)
    else:
        last_mod_feed = current_time
    current_feed.last_modified = last_mod_feed
    current_feed.last_updated = current_time
    current_feed.is_available = True
    current_feed.save()

    return is_new_posts_found

    
def update_all_feeds():
    feed_list = Feed.objects.all()
    feed_url_list = [feed.url for feed in feed_list]
    for feed_url in feed_url_list:
        update_feed(feed_url)


if __name__ == "__main__":
    pass