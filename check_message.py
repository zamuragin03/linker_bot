import WorkingWithDB as base

keywords = base.DB.get_keywords_parse()
banwords = base.DB.get_banwords()

def check_message(message):
    for phrase in keywords:
        a = []
        for word in phrase.split(' '):
            if word.lower() in message.lower():
                a.append(1)
            else:
                a.append(0)
        accuracy = a.count(1)/len(a)
        if accuracy>= 0.6:
            for word in banwords:
                if word.lower() in message.lower():
                    return False
            return True
    return False
