from django.shortcuts import render
from parser_backend.models import Folder, Feed, Post


# Create your views here.
def main_rss(request):
    all_feeds = Feed.objects.all()
    #feed_info = Feed.objects.get(pk=feed)
    post_list = Post.objects.all().order_by("-release_date")
    context = {
        'feed_list': all_feeds,
        'cur_feed': 'all articles',
        'posts': post_list,
    }
    return render(request, "rss_feed.html", context)

def open_feed(request, pk):
    all_feeds = Feed.objects.all()
    feed_info = Feed.objects.get(pk=pk)
    post_list = Post.objects.filter(parent_feed=feed_info).order_by("-release_date")
    context = {
        'feed_list': all_feeds,
        'cur_feed': feed_info.title,
        'posts': post_list,
    }
    print(feed_info)
    return render(request, 'rss_feed.html', context)
