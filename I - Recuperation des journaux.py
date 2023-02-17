import urllib.request, urllib.error, urllib.parse
import re
import os
import json

# Initiating the function for retrieving the date id of gallica
def pressdate(year, month, day, rate, item):
    finallist = []
    monthbissex = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    monthunbissex = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    counting = 1
    curmonth = month - 1
    initialday = '%02d' % day
    initialmonth = curmonth + 1
    initialmonth = '%02d' % initialmonth
    initialresult = str(year) + str(initialmonth) + str(initialday)
    finallist.append(initialresult)
    if year % 4 == 0 and not year % 100 == 0:
        while counting < item:
            day += rate
            counting += 1
            if day > monthbissex[curmonth]:
                day = day - monthbissex[curmonth]
                curmonth += 1
            if curmonth == 12:
                year += 1
                curmonth = 0
            finalmonday = '%02d' % day
            finalmonth = curmonth + 1
            finalmonth = '%02d' % finalmonth
            finalresult = str(year) + str(finalmonth) + str(finalmonday)
            finallist.append(finalresult)
    else:
        while counting < item:
            day += rate
            counting += 1
            if day > monthunbissex[curmonth]:
                day = day - monthunbissex[curmonth]
                curmonth += 1
            if curmonth == 12:
                year += 1
                curmonth = 0
            finalmonday = '%02d' % day
            finalmonth = curmonth + 1
            finalmonth = '%02d' % finalmonth
            finalresult = str(year) + str(finalmonth) + str(finalmonday)
            finallist.append(finalresult)
    return finallist


def jpgpress(url, title="titre", year=1900, month=1, day=1, item=5, rate=1, firstpage=1, lastpage=1, resolution=5000, images_file_name="images"):
    firstdate = pressdate(year, month, day, rate, item)
    secondpage = firstpage + 1
    lastpage += 1
    listpage = range(secondpage, lastpage)

    
    dir = 'images/'
    extension = '.jpg'

    for date in firstdate:
        jpgfile = title + "_" + date + "_page_" + str(firstpage) + extension
        firsturl = url + date
        response = urllib.request.urlopen(firsturl)
        realurl = response.geturl()
        print(realurl)
        identifier = re.sub(r'https://gallica.bnf.fr/ark:', r'', realurl)
        identifier = re.sub(r'.item', r'', identifier)
        finalurl = 'https://gallica.bnf.fr/iiif/ark:' + identifier + '/f' + str(firstpage) + '/full/' + str(resolution) + '/0/native' + extension
        print(finalurl)
        try:
            urllib.request.urlopen(finalurl)
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
        else:
            urllib.request.urlretrieve(finalurl, images_file_name + '/' + jpgfile)
        if len(listpage) > 0:
            for page in listpage:
                jpgfile = title + "_" + date + "_page_" + str(page) + extension
                otherurl = 'https://gallica.bnf.fr/iiif/ark:' + identifier + '/f' + str(
                    page) + '/full/' + str(resolution) + '/0/native' + extension
                try:
                    urllib.request.urlopen(otherurl)
                except urllib.error.URLError as e:
                    if hasattr(e, 'reason'):
                        print('We failed to reach a server.')
                        print('Reason: ', e.reason)
                    elif hasattr(e, 'code'):
                        print('The server couldn\'t fulfill the request.')
                        print('Error code: ', e.code)
                else:
                    urllib.request.urlretrieve(otherurl, images_file_name + '/' + jpgfile)



with open('datas/journaux.json', encoding='utf-8') as d:
  journauxDict = json.load(d)


images_file_name = 'images'
try:
  os.makedirs('./' + images_file_name)
except: pass


for key in journauxDict:
  journal = journauxDict[key]
  jpgpress(url=journal['url'], title=journal['title'], year=journal['year'], month=journal['month'], day=journal['day'], item=journal['item'], rate=journal['rate'], firstpage=journal['firstpage'], lastpage=journal['lastpage'], resolution=journal['resolution'], images_file_name=images_file_name)
