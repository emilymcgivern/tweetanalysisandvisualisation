# Tweet Analysis and Visualisation Tool

To run Tweet Analysis and Visualisation Tool, there are a number of steps to be followed.

1. First, clone the gitlab repository, located at:

https://github.com/emilymcgivern/tweetanalysisandvisualisation.git

2. Save the repository locally. Next, navigate to the directory :

tweetanalysisandvisualisation-master/tweetanalysis/tweetanalysis

3. Run the following command:

$ pip3 install -r requirements.txt

This command will install all necessary packages and libraries to run the application. It will install the following packages:

Django==2.1.5

django-allauth==0.38.0

django-extensions==2.1.5

django-plotly-dash==0.9.8

django-background-tasks==1.2.0

tweepy==3.7.0

vaderSentiment==3.2.1

python-dateutil==2.7.5

4. Next, run the command:

$ python3 manage.py runserver

5. Open a second terminal window and navigate to :

tweetanalysisandvisualisation-master/tweetanalysis/tweetanalysis

6. Run the command:

$ python3 manage.py process_tasks

7. Navigate to http://127.0.0.1:8000 to use the application.
