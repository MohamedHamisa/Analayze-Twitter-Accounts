# Import Dependencies
!pip install tweepy
!pip install ibm_watson 
#IBM Watson is AI for business.
#Watson helps organizations predict future outcomes, automate complex processes, and optimize employees' time

# Get Data from Twitter
# Import os to work with the operating system
import os 

# Import tweepy to work with the twitter API
import tweepy as tw

# Import pandas to work with dataframes
import pandas as pd

consumer_key = 'YOUR TWITTER CONSUMER KEY'
consumer_secret = 'YOUR TWITTER CONSUMER SECRET'
access_token = 'YOUR TWITTER ACCESS TOKEN' # from twitter developers in the app
access_token_secret = 'YOUR TWITTER ACCESS TOKEN SECRET'
 
# Authenticate
auth = tw.OAuthHandler(consumer_key, consumer_secret)
# Set Tokens
auth.set_access_token(access_token, access_token_secret)
# Instantiate API
api = tw.API(auth, wait_on_rate_limit=True)

handle = 'TiffanyHaddish' #to help to grap data from twitter 

res = api.user_timeline(screen_name=handle, count=100, include_rts=True) #including retweets

tweets = [tweet.text for tweet in res]

tweets

text = ''.join(str(tweet) for tweet in tweets) #joint it into one big text

text

# Setup Personality Insights

# Import Watson
from ibm_watson import PersonalityInsightsV3

# Import authenticator
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Creds for Personality Insights
apikey = 'YOUR PERSONALITY INSIGHTS API KEY' #from ibm cloud
url = 'YOUR PERSONALITY INSIGHTS URL'
# Authenticate to PI service
authenticator = IAMAuthenticator(apikey) #instance from the authenticator 
personality_insights = PersonalityInsightsV3(
        version='2017-10-13', 
        authenticator=authenticator
)
personality_insights.set_service_url(url) #where the personality api reside in the world wide

profile = personality_insights.profile(text, accept='application/json').get_result()
profile

for personality in profile['personality']:
    print(personality['name'], personality['percentile'])


for personality in profile['values']:
    print(personality['name'], personality['percentile'])

for personality in profile['needs']:
    print(personality['name'], personality['percentile'])


# Visualise the Results
# Import matplotlib 
from matplotlib import pyplot as plt
# Import seaborn
import seaborn as sns

# Visualise profiles 
needs = profile['needs']
result = {need['name']:need['percentile'] for need in needs}
df = pd.DataFrame.from_dict(result, orient='index')
df.reset_index(inplace=True)
df.columns = ['need', 'percentile']
df.head()

# Create Plot
plt.figure(figsize=(15,5))
sns.barplot(y='percentile', x='need', data=df).set_title('Needs')
plt.show()

# Create plotting Function
def create_trait_plot(name, traits):
    result = {trait['name']:trait['percentile'] for trait in traits}
    df=pd.DataFrame.from_dict(result, orient='index')
    df.reset_index(inplace=True)
#When inplace = True , the data is modified in place, which means it will return nothing and the dataframe is now updated
#When inplace = False , which is the default, then the operation is performed and it returns a copy of the object
#You then need to save it to something.

    df.columns = ['need', 'percentile']
    plt.figure(figsize=(15,5))
    sns.barplot(y='percentile', x='need', data=df).set_title(name)
    plt.show()

[create_trait_plot(personality_trait['name'], personality_trait['children']) for personality_trait in profile['personality']]
