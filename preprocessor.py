
import pandas as pd
import re
def preprocessor(data):
    pattern = "\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s-\s"
    messages = re.split(pattern, data)[1:]  ## the above pattern is a regex pattern to split chats into
    ## dates and the useer name and the message content
    dates = re.findall(pattern, data)
    # dates

    df = pd.DataFrame({'user_messages': messages, 'message_date': dates})
    ## column for the messages and the dates
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')
    df.rename(columns={'message_date': 'dates'}, inplace=True)
    users = []
    messages = []

    for record in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', record)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df['Year'] = df['dates'].dt.year

    df['Month'] = df['dates'].dt.month_name()
    df['day_name'] = df['dates'].dt.day_name()
    df['Day'] = df['dates'].dt.day
    df['Hour'] = df['dates'].dt.hour
    df['Minute'] = df['dates'].dt.minute

    return df

