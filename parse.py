import snscrape.modules.telegram as parser
import WorkingWithDB as base


def getinfo(keyword: str):
    lst = []
    channels = base.DB.get_chnls()
    a = []
    p = parser.TelegramChannelScraper(channels[0])

    for channel in channels:
        p = parser.TelegramChannelScraper(channel)
        for el, tg in enumerate(p.get_items()):
            a.append({'link': tg.url, 'content': tg.content})
            print(el)
            if el > 100:
                break
    for el in a:
        try:
            if keyword.lower() in str(el['content']).lower():
                lst.append(el)
        except:
            pass
    return lst
