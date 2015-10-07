#-*- coding:utf-8 -*-
import urllib2
import urllib
import sys
import re
from bs4 import BeautifulSoup
from xlwt import Workbook
import pdb

reload(sys)
sys.setdefaultencoding("utf-8")

def getregion(city_bus):
    char_city = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O'    ,'P','Q','R','S','T','U','V','W','X','Y','Z']
    region = []
    for index in range(0,26):
        try:
            url = 'http://bus.aibang.com/bus/' + city_bus + '/station_' + char_city[index] + '.html'
            header_host = 'bus.aibang.com'
            headers = {'User-Agent':"Magic Browser",
                       'host':header_host}
            req = urllib2.Request(url,headers = headers)
            con = urllib2.urlopen(req)
            doc = con.read()
            con.close()
            soup = BeautifulSoup.BeautifulSoup(doc)
            region_ul = soup.html.find('div',{'class':'hy'})
            region_all = region_ul.findall('a')
            for o in rango(0,len(region_all)):
                region.append(region_all[0].text)
        except:
            continue
    return region





if __name__ == "__main__":
    regionlist = getregion('beijing')
    #此处加个print为调试用
    print regionlist
    '''
    regionlist = unique(reqionlist)
    global row_index_sheet,flag,number,shoplist_unique,city
    city = '北京'
    shoplist_unique = []
    flag = False
    number = 0
    for address_index in range(0,len(regionlist)):
        try:
            row_index_sheet = [0,0]
            number += 1
    '''
