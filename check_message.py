import WorkingWithDB as base

keywords = base.DB.get_keywords_parse()


def check_message(message):

    for phrase in keywords:
        a = []
        for word in phrase.split(' '):
            if word.lower() in message.lower():
                a.append(1)
            else:
                a.append(0)
        if (a.count(1)/len(a)) > 0.5:
            return True
    return False
