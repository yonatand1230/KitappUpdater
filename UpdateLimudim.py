from dotenv import load_dotenv
from os import getenv
import sys,json,clipboard

from Shachaf import GetChanges
from Tehilim import GetTehilim
from Upload import Upload
from Limud import Limud

def addGershaim(s):
    if len(s) == 1:
        s += "'"
        return s
    else:
        s = s[:-1] + '"' + s[-1]
        return s


load_dotenv()
token = getenv('token')

def getTitles(ref=False):
    ## UPDATE LIMUD ##
    limudim = Limud.getLimudim(ref=ref)
    tehilim_avot = GetTehilim.main()

    start = list(tehilim_avot['tehilim'])[0].replace(':','').replace('פרק ','')
    ending = list(tehilim_avot['tehilim'])[-1].replace(':','').replace('פרק ','')

    start = addGershaim(start)
    ending = addGershaim(ending)

    if ref:
        limudim.append({
            "title": "פרק תהילים יומי",
            "value": "פרקים "+start+"-"+ending,
            "filename": "content/Tehilim.json",
            "ref":"",
            "enTitle": "Tehilim Yomi"
        })

        avot = list(tehilim_avot['avot'])[0].replace('פרק ','').replace('משנה ','').split(' ')

        limudim.append({
            "title": "פרק אבות יומי",
            "value": "אבות, " + addGershaim(avot[0]) + ", " + addGershaim(avot[1]),
            "filename": "content/Avot.json",
            "ref":"",
            "enTitle": "Avot Yomi"
        })
    else:
        limudim.append({
            "title": "פרק תהילים יומי",
            "value": "פרקים "+start+"-"+ending,
            "filename": "content/Tehilim.json"
        })

        avot = list(tehilim_avot['avot'])[0].replace('פרק ','').replace('משנה ','').split(' ')

        limudim.append({
            "title": "פרק אבות יומי",
            "value": "אבות, " + addGershaim(avot[0]) + ", " + addGershaim(avot[1]),
            "filename": "content/Avot.json"
        })

    return limudim


def main():
    # update titles
    titles = getTitles()
    Upload.upload_json(
            titles,
            file_path = "titles.json",
            repository = "KitappContent",
            username = "yonatand1230",
            msg = "Update Titles",
            token = token,
            )
    
    # update contents
    for limud in getTitles(ref=True):
        title = limud.get('title')
        value = limud.get('value')
        ref = limud.get('ref')
        en = limud.get('enTitle')
        
        if ref != "":
            txt, next = Limud.getLimud(ref)
        else:
            ref = ''
            if 'Avot' in en:
                d = GetTehilim.main(avot=True)
                txt = d.get(list(d)[0])
                next = ''
            elif 'Tehilim' in en:
                txt = GetTehilim.main(tehilim=True)
                next = ''
        
        final = {
            "txt": txt,
            "next": next
        }
        

        filename = en.replace(' ','') + '.json'
        print(filename)

        
        Upload.upload_json(
            final,
            file_path = filename,
            repository = "KitappContent",
            username = "yonatand1230",
            msg = "Update Contents",
            token = token,
            folder = "content"
            )



if __name__ == "__main__":
    main()