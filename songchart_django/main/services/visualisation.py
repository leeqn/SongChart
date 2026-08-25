import pandas as pd
import seaborn as sns
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def get_info(engine,days=None,module=None):
    with engine.connect() as connection:
        songspd = pd.read_sql('''SELECT title, artist, tag, time
                               FROM songs''', connection)

        if days:
            songspd['time']=pd.to_datetime(songspd['time'])
            songspd=songspd.loc[songspd['time'].between(datetime.now()-timedelta(days=days),datetime.now())]
            if songspd.empty:
                print('There is no songs for these days')
                return 0

        if module=='track':
            songspd = (songspd.groupby(['title', 'artist'])['time']
                       .count()
                       .reset_index(name='listened_count')
                       .sort_values('listened_count', ascending=False)
                       .head(5))
            sns.barplot(songspd,x='title',y='listened_count',hue='title',legend='brief').set_title('Songs by listened times')
            plt.gca().set_xticklabels([])
            plt.show()

        if module=='tag':
            songspd=(songspd.groupby('tag')['time']
                     .count()
                     .reset_index(name='listened_count')
                     .sort_values('listened_count', ascending=False)
                     .head(5))
            sns.barplot(songspd, y='tag',x='listened_count', hue='tag', legend='brief').set_title('Top tags')
            plt.show()

        if module=='hour':
            songspd['hour'] = pd.to_datetime(songspd['time']).dt.hour
            sns.histplot(data=songspd, x='hour', bins=24, kde=True).set_title('Songs by hour')
            plt.show()

        else:
            return 0