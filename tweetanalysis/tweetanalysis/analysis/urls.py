from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('user_timeline',views.user_timeline, name='user_timeline'),
    path('get_user_results',views.get_user_results, name='get_user_results'),
    path('chosen_radio',views.chosen_radio, name='chosen_radio'),
    path('hashtag_results',views.hashtag_results, name='hashtag_results'),
    path('search_term_results',views.search_term_results, name='search_term_results'),
    path('sentiment_analyser_scores',views.sentiment_analyser_scores, name='sentiment_analyser_scores'),
    path('profile', views.profile, name='profile'),
    path('testing_retweets', views.testing_retweets, name='testing_retweets'),
    path('testing_likes', views.testing_likes, name='testing_likes'),
    path('testing_followers', views.testing_followers, name='testing_followers'),
    path('monitoring', views.monitoring, name='monitoring'),
    path('replies', views.replies, name='replies'),
    path('sentiment', views.sentiment, name='sentiment'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('switch_graph', views.switch_graph, name='switch_graph'),
    path('stream_graph', views.stream_graph, name='stream_graph'),
    path('update_reactions', views.update_reactions, name='update_reactions'),
    path('view_all', views.view_all, name='view_all'),
    path('view_likes', views.view_likes, name='view_likes'),
    path('view_retweets', views.view_retweets, name='view_retweets'),
    path('view_followers', views.view_followers, name='view_followers'),
    path('view_both', views.view_both, name='view_both'),
    path('check', views.check, name='check'),
]
