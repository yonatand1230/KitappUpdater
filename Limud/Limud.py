import requests, re
from hebrew_numbers import int_to_gematria

base_url = "https://www.sefaria.org/api/"

def buildUrl(endpoint):
    return base_url+endpoint

def remove_tags(text):
    clean_text = re.sub('<.*?>', '', text)
    return clean_text


def getLimudim(ref=False):
    response = requests.get(buildUrl("calendars?timezone=Asia/Jerusalem"))
    calendars = response.json()

    items = calendars.get('calendar_items')

    allow = [
        '929',
        'משנה יומית',
        'הרמב"ם היומי',
        'הלכה יומית'
    ]

    limud = []
    limud_withref = []
    
    for i in items:
        if i.get('title').get('he') in allow:
            if ref:
                limud.append({
                    "title": i.get('title').get('he'),
                    "value": i.get('displayValue').get('he'),
                    "filename": "content/" + i.get('title').get('en').replace(' ','') + ".json",
                    "ref": i.get('ref'),
                    "enTitle": i.get('title').get('en')
                })
            else:
                limud.append({
                    "title": i.get('title').get('he'),
                    "value": i.get('displayValue').get('he'),
                    "filename": "content/" + i.get('title').get('en').replace(' ','') + ".json"
                })
            
    return limud

def getLimud(ref):
    response = requests.get(buildUrl(f'texts/{ref}'))
    
    if ':' in ref: # not the whole chapter!
        # find mishna
        num = int(ref.split(':')[-1].split('-')[0])
        l = response.json().get('he')
        print(len(l))
        mishna = l[num-1]
        
        # find next
        # check if another mishna in chapter

        if len(l) > num:
            next = ref.replace(str(num), str(num+1))
        else:
            next = response.json().get('next') + ":1"
        
        return mishna, next
    
    else:
        txt = response.json().get('he')
        final = ''
        for i in range(len(txt)):
            temp = f'({int_to_gematria(i+1)}) '
            temp += remove_tags(txt[i]).strip()
            temp = temp.replace(' ',' ').replace('}','}\n\n')
            if temp[-1] != "\n": temp+=" "
            final += temp
        
        next = response.json().get('next')
        
        return final, next

def getNextBook(ref):
    ## NEED TO WRITE THIS FUNCTION
    return 0
    
if __name__ == "__main__":
    import clipboard
    clipboard.copy(str(getLimud("Mishnah Sukkah 1:11")))