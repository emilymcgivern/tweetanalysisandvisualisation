from django.db import models
from django.contrib.auth.models import User #allows access to user model
from django.utils.timezone import now
from decimal import Decimal

# Create your models here.
class TweetDetails(models.Model):
	user_id_str = models.ForeignKey(User, on_delete=models.CASCADE, null=True) #which ever logged on user saved a tweet in our app
	id_str = models.CharField(max_length=512, default='', primary_key=True)
	text = models.CharField(max_length=512, default='')
	created_at = models.CharField(max_length=512, default='') 
	likes = models.IntegerField(default=0)
	retweets = models.IntegerField(default=0)
	posted_by = models.CharField(max_length=512, default='') #twitter handle screen name
	userid = models.CharField(max_length=512, default='') #twitter handle id str
	followers_count = models.IntegerField(default=0)
	sentiment_value = models.DecimalField(max_digits=20, decimal_places=5, default=Decimal('0.00000')) #storing sentiment of the tweet
	first_saved = models.DateTimeField(auto_now_add=True, null=True, blank=True)


# storing the saved tweets to not conflict with the tweet details
class Saved(models.Model):
	user_id_str = models.ForeignKey(User, on_delete=models.CASCADE, null=True) #which ever logged on user saved a tweet in our app
	id_str = models.CharField(max_length=512, default='', primary_key=True)
	text = models.CharField(max_length=512, default='')
	created_at = models.CharField(max_length=512, default='') 
	likes = models.IntegerField(default=0)
	retweets = models.IntegerField(default=0)
	posted_by = models.CharField(max_length=512, default='') #twitter handle screen name
	userid = models.CharField(max_length=512, default='') #twitter handle id str
	followers_count = models.IntegerField(default=0)
	sentiment_value = models.DecimalField(max_digits=20, decimal_places=5, default=Decimal('0.00000')) #storing sentiment of the tweet
	first_saved = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	

	def __unicode__(self):
		return self.text
		return self.id_str
		return self.created_at


#setting up model to track the reaction to a tweet
class Reaction(models.Model): 
    auto_increment_id = models.AutoField(primary_key=True)
    tweetid = models.CharField(max_length=512, default='')
    tweet_likes = models.IntegerField(default=0)
    tweet_retweets = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True) #time that the object was created in the db
    created_at = models.CharField(max_length=512, default='') #time that the tweet was posted on twitter
    number_of_followers = models.IntegerField(default=0)
    first_saved = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_id_str = models.CharField(max_length=512, default='')

    def __unicode__(self):
    	return self.tweetid
    	return self.tweet_likes
    	return self.tweet_retweets


# Tracking which tweets have been monitored
class Monitoring(models.Model):
	tweetidstr = models.CharField(max_length=512, default='', primary_key=True)
	tweet_text = models.CharField(max_length=512, default='')
	user_posted = models.CharField(max_length=512, default='')
	user_id_str = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

	def __unicode__(self):
		return self.tweetidstr
		return self.tweet_text
		return self.user_posted













