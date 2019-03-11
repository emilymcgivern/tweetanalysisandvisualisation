from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import tweepy
from tweepy.auth import OAuthHandler
from django.template import loader
from analysis.models import TweetDetails, Reaction, Monitoring, Saved
from django.shortcuts import get_object_or_404, render
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from django.contrib.auth.models import User #allows access to user model
import json
from django.shortcuts import redirect
from background_task import background
import datetime
from dateutil.parser import parse
from dateutil import parser
import sys
from django.contrib.auth.decorators import login_required


#open a file called "keys" with keys and tokens for Twitter separated by newlines
keyFile = open('keys.txt', 'r')
consumer_key = keyFile.readline().rstrip()
consumer_secret = keyFile.readline().rstrip()
access_token = keyFile.readline().rstrip()
access_token_secret = keyFile.readline().rstrip()
keyFile.close()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)



# accounts/views.py     for the accounts only
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

# this is to get to the sign up page:
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'analysis/index.html')


def hashtag_results(request):
    return render(request, 'analysis/hashtag_results.html')

@background(schedule=5)
def gather_response(tweet):
    returned = api.get_status(tweet)
    add_reactions = Reaction(tweetid = returned.id_str, tweet_likes = returned.favorite_count, tweet_retweets = returned.retweet_count, created_at = returned.created_at, number_of_followers = returned.user.followers_count)
    add_reactions.save()
    print ("Reaction Collected") 

@background(schedule=5)
def stop_likes_response(query):
    tweet = query[0]
    date = query[1]
    likes = int(query[2])
    likes_set = Reaction.objects.filter(tweetid = tweet, tweet_likes = likes)
    likes_count = [l.tweet_likes for l in likes_set]
    if likes not in likes_count:
        returned = api.get_status(tweet)
        add_reactions = Reaction(tweetid = returned.id_str, tweet_likes = returned.favorite_count, tweet_retweets = returned.retweet_count, created_at = returned.created_at, number_of_followers = returned.user.followers_count)
        add_reactions.save()
        print ("Reaction collected")
    else:
        print ("exiting")
        sys.exit(0)

@background(schedule=5)
def stop_retweets_response(query):
    tweet = query[0]
    date = query[1]
    retweets = int(query[3])
    retweets_set = Reaction.objects.filter(tweetid = tweet, tweet_retweets = retweets)
    retweets_count = [r.tweet_retweets for r in retweets_set]
    if retweets not in retweets_count:
        returned = api.get_status(tweet)
        # context = {'returned': returned }
        add_reactions = Reaction(tweetid = returned.id_str, tweet_likes = returned.favorite_count, tweet_retweets = returned.retweet_count, created_at = returned.created_at, number_of_followers = returned.user.followers_count)
        add_reactions.save()
        print ("Reaction collected")
    else:
        print ("exiting")
        sys.exit(0)

@background(schedule=5)
def stop_either_response(query):
    tweet = query[0]
    date = query[1]
    likes = int(query[2])
    retweets = int(query[3])
    likes_set = Reaction.objects.filter(tweetid = tweet, tweet_likes = likes)
    retweets_set = Reaction.objects.filter(tweetid = tweet, tweet_retweets = retweets)
    likes_count = [l.tweet_likes for l in likes_set]
    retweets_count = [r.tweet_retweets for r in retweets_set]

    if not (likes in likes_count or retweets in retweets_count):
        returned = api.get_status(tweet)
        # context = {'returned': returned }
        add_reactions = Reaction(tweetid = returned.id_str, tweet_likes = returned.favorite_count, tweet_retweets = returned.retweet_count, created_at = returned.created_at, number_of_followers = returned.user.followers_count)
        add_reactions.save()
        print ("Reaction collected")
    else:
        print ("exiting")
        sys.exit(0)

def replies(request):
    user = request.user
    query = request.POST.getlist('tweet') 
    tweet = query[0]
    date = query[1]
    likes = query[2]
    retweets = query[3]
    tweet_details = api.get_status(tweet, tweet_mode='extended')
    new_monitoring = Monitoring(tweetidstr = tweet, tweet_text = tweet_details.full_text, user_posted = tweet_details.user.screen_name, user_id_str = user)
    new_monitoring.save()
    find_tweet = Saved.objects.get(id_str=tweet)  
    find_tweet.delete()

    if date == '':
        if likes == '':
            stop_retweets_response(query, repeat=10)
            response = redirect('/profile')
            return response
        elif retweets == '':
            stop_likes_response(query, repeat=10)
            response = redirect('/profile')
            return response
        else:
            stop_either_response(query, repeat=10)
            response = redirect('/profile')
            return response
    else:
        dt = parser.parse(date)
        gather_response(tweet, repeat=10, repeat_until=dt)
        response = redirect('/profile')
        return response

@login_required(login_url='/accounts/login/')
def profile(request):
    try:
        user = request.user
        saved_tweets = Saved.objects.filter(user_id_str = user)  
        returned = Monitoring.objects.filter(user_id_str = user) 
        context = {'saved_tweets' : saved_tweets, 'returned' : returned}
        return render(request, 'analysis/profile.html', context)
    except tweepy.TweepError as e:
        if e == "[{u'message': u'Rate limit exceeded', u'code': 88}]":
            time.sleep(60*5) #Sleep for 5 minutes
        else:
            print (e)

def testing(request):
    return render(request, 'analysis/testing.html')

def monitoring(request):
    try:
        if 'delete' in request.POST:
            query = request.POST.get('tweet')
            project = TweetDetails.objects.get(id_str=query)  
            project.delete()
            response = redirect('/profile')
            return response
        else:
            query = request.POST.get('tweet')
            projects = TweetDetails.objects.filter(id_str=query)  
            context = {'projects' : projects}
            return render(request, 'analysis/monitoring.html', context)
    except tweepy.TweepError as e:
        if e == "[{u'message': u'Rate limit exceeded', u'code': 88}]":
            time.sleep(60*5) #Sleep for 5 minutes
        else:
            print (e)

def search_term_results(request):
    try:
        query = request.POST.get('query')
        matching_tweets = api.search(query + "-filter:retweets -filter:replies" , lang = 'en', count = 50, tweet_mode='extended')
        return render(request, 'analysis/search_term_results.html', {'matching_tweets': matching_tweets})
    except tweepy.TweepError as e:
        if e == "[{u'message': u'Rate limit exceeded', u'code': 88}]":
            time.sleep(60*5) #Sleep for 5 minutes
        else:
            return render(request, 'analysis/index.html')

def user_timeline(request):
    try:
        sentiment = []
        tweet = request.POST.get('tweet')
        user_tweets = api.user_timeline(tweet, lang = 'en', count = 50, tweet_mode='extended')
        context = {'user_tweets': user_tweets}
        return render(request, 'analysis/user_tweets.html', context)
    except tweepy.TweepError as e:
        return redirect('/index')

def get_user_results(request):
    try:
        handle = request.POST.get('handle')
        users = api.get_user(handle, count = 5)
        return render(request, 'analysis/get_user_results.html', {'users': users})
    except tweepy.TweepError as e:
        return render(request, 'analysis/index.html')

def hashtag_results(request):
    try:
        hashtag = request.POST.get('hashtag')
        go_find = api.search("#" + hashtag + "-filter:retweets -filter:replies", lang = 'en', count = 50, tweet_mode='extended')
        return render(request, 'analysis/hashtag_results.html', {'go_find': go_find})
    except tweepy.TweepError as e:
        return render(request, 'analysis/index.html')


def update_reactions(request):
    try:
        tweet = request.session.get('tweet')
        reactions = Reaction.objects.filter(tweetid = tweet)
        tweet_text = Monitoring.objects.filter(tweetidstr = tweet)
        text = [t.tweet_text for t in tweet_text]
        date_saved = [r.first_saved.strftime('%d-%m %H:%M') for r in reactions]
        likes_count = [r.tweet_likes for r in reactions]
        retweets_count = [r.tweet_retweets for r in reactions]
        followers_count = [r.number_of_followers for r in reactions]
        data = [date_saved, likes_count, retweets_count, followers_count, text]

        return JsonResponse(data,  safe=False)
            
    except tweepy.TweepError as e:
        if e == "[{u'message': u'Rate limit exceeded', u'code': 88}]":
            time.sleep(60*5) #Sleep for 5 minutes
        else:
            print (e)


def view_all(request):
    return render(request, 'analysis/view_all.html',)

def check(request):
    tweet = request.POST.get('tweet')
    request.session['tweet'] = tweet
    return render(request, 'analysis/check.html',)


analyser = SentimentIntensityAnalyzer()
def sentiment_analyser_scores(text):            # this function gets the sentiment of the tweet
    score = analyser.polarity_scores(text)['compound']
    return score


def chosen_radio(request):
    try:
        tweet_id = request.POST.get('tweet')
        get_tweet = api.get_status(tweet_id, tweet_mode='extended')

        get_sentiment = sentiment_analyser_scores(get_tweet.full_text)     # added to get sentiment of the tweet

        # adding tweet to database
        first_save = TweetDetails(id_str = get_tweet.id_str, text = get_tweet.full_text, created_at = get_tweet.created_at, user_id_str = request.user, likes=get_tweet.favorite_count, retweets = get_tweet.retweet_count, posted_by = get_tweet.user.screen_name, followers_count = get_tweet.user.followers_count, userid = get_tweet.user.id_str, sentiment_value = get_sentiment)
        first_save.save()

        saved_tweets = Saved(id_str = get_tweet.id_str, text = get_tweet.full_text, created_at = get_tweet.created_at, user_id_str = request.user, likes=get_tweet.favorite_count, retweets = get_tweet.retweet_count, posted_by = get_tweet.user.screen_name, followers_count = get_tweet.user.followers_count, userid = get_tweet.user.id_str, sentiment_value = get_sentiment)
        saved_tweets.save()

        return_sentiment = TweetDetails.objects.filter(id_str = get_tweet.id_str)
        for value in return_sentiment:
            sentiment = value.sentiment_value


        context = {'get_tweet': get_tweet, 'sentiment': sentiment}

        return render(request, 'analysis/chosen_radio.html', context)
    except tweepy.TweepError as e:
        if e == "[{u'message': u'Rate limit exceeded', u'code': 88}]":
            time.sleep(60*5) 
        else:
            print (e)




def sentiment(request):
    try:
        reactions = TweetDetails.objects.all()
        sent_deets = [r.sentiment_value for r in reactions]
        user_ids = [r.id_str for r in reactions]
        user_retweets = [r.retweets for r in reactions]
        user_likes = [r.likes for r in reactions]
        user_follrs = [r.followers_count for r in reactions]



        data = [sent_deets, user_retweets, user_likes, user_follrs]

        return JsonResponse(data,  safe=False)

    except tweepy.TweepError as e:
        if e == "[{u'message': u'Rate limit exceeded', u'code': 88}]":
            time.sleep(60*5) 
        else:
            print (e)


def testing_retweets(request):
    return render(request, 'analysis/testing_retweets.html', )

def testing_likes(request):
    return render(request, 'analysis/testing_likes.html',)

def testing_followers(request):
    return render(request, 'analysis/testing_followers.html',)

def switch_graph(request):
    return render(request, 'analysis/switch_graph.html',)

def stream_graph(request):
    return render(request, 'analysis/stream_graph.html',)

def view_likes(request):
    return render(request, 'analysis/view_likes.html',)

def view_retweets(request):
    return render(request, 'analysis/view_retweets.html',)

def view_followers(request):
    return render(request, 'analysis/view_followers.html',)

def view_both(request):
    return render(request, 'analysis/view_both.html',)


