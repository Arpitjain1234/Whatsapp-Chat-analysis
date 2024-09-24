import streamlit as st
import preprocessor
import helper
import pandas as pd
import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp Chat Analyser")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue() ## here the data will in fron of bits
    data  = bytes_data.decode('utf-8')
    df = preprocessor.preprocessor(data)

    user_list = df['user'].unique().tolist() ## to convert the list to dropdown
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("Choose a user",user_list)
    if st.sidebar.button("Show Analysis"):
        col1, col2, col3, col4 = st.columns(4)
        words, num,media_num,links = helper.fetch_stats(selected_user, df)
        with col1:
            st.header('Messages')
            st.title(num)
        with col2:
            st.header('Total Words')
            total_words = len(words)
            st.title(total_words)
        with col3:
            st.header('Total Media')
            st.title(media_num)
        with col4:
            st.header('Total Links')
            st.title(len(links))

    ## timeline
    st.title('Monthly Timeline')
    timeline  = helper.monthly_timeline(selected_user,df)
    fig,ax = plt.subplots()
    ax.plot(timeline['time'],timeline['message'])
    plt.xticks(rotation = 'vertical')
    st.pyplot(fig)
    ## weekluy  and monthly activity map
    st.title('Activity Maps')
    col1,col2  =  st.columns(2)
    with col1:
        st.title('Busy Days')
        activity_map = helper.week_activity_map(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(activity_map.index,activity_map.values,color='green')
        st.pyplot(fig)
    with col2:
        st.title('Busy Months')
        activity_map = helper.month_activity_map(selected_user,df)
        fig,ax = plt.subplots()
        plt.xticks(rotation= 'vertical')
        ax.bar(activity_map.index,activity_map.values,color='orange')
        st.pyplot(fig)


    if selected_user=='Overall':
        st.title('Most Busy Users')
    if selected_user=='Overall':
        x,percent = helper.most_busy_users(df)

        fig,ax = plt.subplots()
        col1,col2 = st.columns(2)

        with col1:
            ax.bar(x.index,x.values)
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        with col2:
            st.text(pd.DataFrame(percent))

    st.title('Word Cloud')
    wc_image = helper.create_word_cloud(selected_user,df)
    fig,ax = plt.subplots()
    ax.imshow(wc_image)
    st.pyplot(fig)


    #plt.imshow(wc_image)
     # most common words
    st.title('Most Common Words')
    most_common_wr = helper.most_common_words(selected_user,df)
    fig,ax = plt.subplots()
    ax.barh(most_common_wr[0],most_common_wr[1])
    plt.xticks(rotation = 'vertical')
    st.pyplot(fig)

    ## analysing the emojis in the chats
    st.title('Emoji Analysis')
    emojis = helper.emoji_helper(selected_user,df)
    col1,col2 = st.columns(2)
    ax.pie(emojis[1],labels = emojis[0])
    st.pyplot(fig)



