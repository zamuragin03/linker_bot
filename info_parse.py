import datetime
import pandas as pd
import numpy as np
import WorkingWithDB as base
import check_message as cm


def get_data(a):
    df1 = pd.DataFrame.from_dict(a['messages'])
    df2 = df1[['message', 'date']].copy()
    df3 = pd.DataFrame.from_dict(a['users'])
    df2['username'] = df3['username']
    df4 = pd.DataFrame.from_dict(a['chats'])
    df2['link'] = df4['username'].iloc[0]
    res = df2.to_dict(orient='records')
    res2 = []
    for el in res:
        now = datetime.datetime.now(tz=el['date'].tzinfo)
        secs = (now.minute - el['date'].minute) * \
            60+(now.second-el['date'].second)
        if abs(secs) < 60 and now.hour == el['date'].hour:
            flag = cm.check_message(el['message'])
            # print((flag, el['message'], el['link'],secs))
            if flag:
                res2.append(
                    {'message': el['message'], 'username': el['username'], 'link': el['link'], 'date': el['date']})
    return res2
