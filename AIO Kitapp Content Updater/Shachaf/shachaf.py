import requests, bs4, re, json
from clipboard import copy



### FIND NUMBER IN STRING ###
def get_numbers(txt):
    # GETS: string with numbers
    # RETURNS: numbers only, as string
    numbers = re.findall(r'\d+\.\d+', txt)
    return numbers[0]

### FIND COMMON SUBSTRING ###
def find_common(strings):
    # GETS: list of strings
    # RETURNS: common substring
    dup = strings
    strings = []
    for i in dup:
        strings.append(str(i))
    if len(strings) == 0:
        return ""
    substring = ""
    for i in range(len(strings[0])):
        for j in range(i+1, len(strings[0])+1):
            if all(strings[0][i:j] in s for s in strings):
                if len(strings[0][i:j]) > len(substring):
                    substring = strings[0][i:j]
    return substring

### STRIP TAG FROM HTML ###
def xstrip(s, tag, cla):
    # GETS: html code, tag+class to look for
    # RETURNS: looks for the tag+class in the code and returns it.
    soup = bs4.BeautifulSoup(str(s), features="lxml")
    td_tag = soup.find(tag, {'class':cla})
    return td_tag.get_text()

class Shachaf:
    ### GET HOLIDAYS AS DICT: ###
    def get_holidays(html):
        holidays = {}

        page = bs4.BeautifulSoup(html, features="lxml")
        l = page.find('table', class_='TTTable').find_all('td', class_='CTitle')

        for i in l:
            current_page = bs4.BeautifulSoup(str(i), features='lxml')
            if current_page.find('span', {'class':'Holiday'}) != None:
                # save holiday name
                holiday_name = current_page.find('span', {'class':'Holiday'}).get_text()
                
                # save holiday date
                date = current_page.find('span').get_text().replace('   ','') # we get a string like "sunday 01.02"
                date_num = get_numbers(date) # we extract the numbers and get: "01.02"        
                
                holidays.update({date_num:holiday_name})
        return holidays

    ### GET CHANGES IN SCHEDULE ###
    def get_changes(html):
        all_changes = []
        page = bs4.BeautifulSoup(html, features="lxml")
        hours = page.find_all('tr', {'bgcolor':"#ffffff"}) # get list of all hours
        hours.pop()

        for hour in hours: # loop through hours
            h_text = hour.find('span', {'class':'hour-time'})
            if h_text != None:
                hour_text = h_text.get_text()
            cells = hour.find_all('td', {'class':'TTCell'}) # cells for current hour
            #print(cells)
            for c in cells:
                tr = c.find_all('tr')
                if len(tr) != 0:
                    if len(tr) == 1:
                        element = tr[0].find('td')
                        change_txt = element.get_text(separator='\n')
                        change_class = element['class'][0]
                        
                        finalChange = change_txt + "&&" + change_class # CHANGE - txt and class, both strings
                    elif len(tr)>1:
                        finalChange=[]
                        for i in tr:
                            one_change_element = i.find('td')
                            one_change_txt = one_change_element.get_text(separator='\n')
                            one_change_class = one_change_element['class'][0]
                            
                            
                            one_change = one_change_txt + "&&" + one_change_class # only one change - txt and class, string
                            finalChange.append(one_change)
                    finalHour = hour_text # HOUR
                    finalDay = cells.index(c) # DAY
                    myChange = {'day':finalDay, 'hour':finalHour, 'body':finalChange}
                    all_changes.append(myChange)
                
        return all_changes

