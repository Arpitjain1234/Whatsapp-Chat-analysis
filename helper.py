
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import  pandas as pd
import emoji
import matplotlib.pyplot as plt
extract  = URLExtract()
def fetch_stats(selected_user,df):
     ## 1 number of messages
    links = []
    if selected_user=='Overall':

      num_mess = df.shape[0]
      words = []
      media_number = df[df['message']=='<Media omitted>\n'].shape[0]
      for msg in df['message']:
           words.extend(msg.split())

      for mess in df['message']:
         links.extend(extract.find_urls(mess))

      return words,num_mess,media_number,links
    else:
        new_df = df[df['user']==selected_user]
        num_mess = new_df.shape[0]
        words = []
        media_number = new_df[new_df['message'] == '<Media omitted>\n'].shape[0]
        for msg in new_df['message']:
            words.extend(msg.split())
        for mess in df['message']:
            links.extend(extract.find_urls(mess))
        return  words , num_mess,media_number,links



def most_busy_users(df):
    x = df['user'].value_counts().head() ## this will return the top 5 most busy users
    percent_msg = round((df['user'].value_counts()/df['user'].shape[0])*100,2).reset_index()

    return x,percent_msg


def create_word_cloud(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]

    wc = WordCloud(height=500,width=500,min_font_size=10,background_color='black')
    wc_image = wc.generate(df['message'].str.cat(sep = " "))
    return  wc_image

def most_common_words(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    hinglish = open('stop_hinglish.txt', 'r')
    stopwords = hinglish.read()
    # finding all the words of a user
    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    # finding the most frequent words

    most_common_wr = pd.DataFrame(Counter(words).most_common(20))
    return most_common_wr

def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend(c for c in message if emoji.is_emoji(c))

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(emojis)))
    return  emoji_df


def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    timeline = df.groupby(['Year', 'Month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + '-' + str(timeline['Year'][i]))

    timeline['time'] = time
    #plt.xticks(rotation='vertical')
    #plt.plot(timeline['time'], timeline['message'])
    return timeline

def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    return  df['day_name'].value_counts()


def month_activity_map(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    return  df['Month'].value_counts()
