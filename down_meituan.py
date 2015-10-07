__author__ = 'IanHwang'
# coding:utf-8
import urllib2
import sys
from xlwt import Workbook
import BeautifulSoup
import re
import pdb

reload(sys)
sys.setdefaultencoding( "utf-8" )

def getregion(city_bus):
    char_city = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    region = []
    for index in range(0,26):
        try:
            url = 'http://bus.aibang.com/bus/' + city_bus + '/station_' + char_city[index] +  '.html'
            header_host = 'bus.aibang.com'
            headers={'User-Agent' : "Magic Browser"}
            req = urllib2.Request(url, headers=headers)
            con = urllib2.urlopen( req )
            doc = con.read()
            con.close()
            soup = BeautifulSoup.BeautifulSoup(doc)
            region_ul = soup.html.find('div',{'class' : 'hy'})
            region_all = region_ul.findAll('a')
            for o in range(0,len(region_all)):
                region.append(region_all[o].text)
        except:
            continue
    return region

def getLngLat(address, city):
    address = address.replace(' ','')
    # url = 'http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&pcevaname=pc2&da_par=direct&from=webmap&qt=s&da_src=pcmappg.searchBox.button&wd=' + address + '&c=131&src=0&wd2=&sug=0&l=19&b=(12966842.24,4838593.5;12967466.74,4838806)&from=webmap&tn=B_NORMAL_MAP&nn=0&ie=utf-8&t=1428205978194'
    url = 'http://api.map.baidu.com/geocoder/v2/?address=' + address + '&output=json&ak=HGjEx6p8fGZ6REbUPmAZQ43U&callback=showLocation&city="北京市"'
    header_host = 'api.map.baidu.com'
    header = {'Host' : header_host}
    req = urllib2.Request(url, headers=header)
    con = urllib2.urlopen( req )
    doc = con.read()
    con.close()
    soup = BeautifulSoup.BeautifulSoup(doc)
    lng = lat = ''
    pattern = re.compile("(?<=lng\":)(.*?)(,)")
    lng = pattern.findall(soup.__str__())
    pattern = re.compile("(?<=lat\":)(.*?)(})")
    lat = pattern.findall(soup.__str__())
    param = [0,0]
    if(lng!=[] and lat != []):
        param[0] = lng[0][0]
        param[1] = lat[0][0]
    return param

def getList(param):
    url = 'http://waimai.meituan.com/geo/geohash?lat=' + param[1] + '&lng=' + param[0] + '&addr=1&from=m'
    header_host = 'waimai.meituan.com'
    header = {'Host' : header_host}
    req = urllib2.Request(url, headers= header)
    con = urllib2.urlopen( req )
    doc = con.read()
    con.close()
    soup = BeautifulSoup.BeautifulSoup(doc)
    data_a = soup.findAll('a', {'class' : 'un-favorite j-save-up'})
    list = []
    for index_data_a in range(0, len(data_a)):
        list.append(data_a[index_data_a].get('data-poiid'))
    return list

def getRecipe(name):
    url = 'http://www.haodou.com/search/recipe/' + name
    header_host = 'www.haodou.com'
    header = {'Host' : header_host}
    req = urllib2.Request(url, headers= header)
    con = urllib2.urlopen( req )
    doc = con.read()
    con.close()
    soup = BeautifulSoup.BeautifulSoup(doc)
    try:
        recipe_url_0 = soup.find('ul', {'class' : 'showList clearfix'}).findAll('span', {'class' : 'img'})[0].find('a').get('href')
        recipe_name_0 = soup.find('ul', {'class' : 'showList clearfix'}).findAll('span', {'class' : 'img'})[0].find('a').get('title')
        recipe_url_1 = soup.find('ul', {'class' : 'showList clearfix'}).findAll('span', {'class' : 'img'})[1].find('a').get('href')
        recipe_name_1 = soup.find('ul', {'class' : 'showList clearfix'}).findAll('span', {'class' : 'img'})[1].find('a').get('title')
        recipe_url_2 = soup.find('ul', {'class' : 'showList clearfix'}).findAll('span', {'class' : 'img'})[2].find('a').get('href')
        recipe_name_2 = soup.find('ul', {'class' : 'showList clearfix'}).findAll('span', {'class' : 'img'})[2].find('a').get('title')
        recipe = [[recipe_name_0,recipe_url_0],[recipe_name_1,recipe_url_1],[recipe_name_2,recipe_url_2]]
    except:
        recipe = [['',''],['',''],['','']]
    return recipe

def getComponents(recipe_url):
    url = recipe_url.__str__()
    header_host = 'www.haodou.com'
    header = {'Host' : header_host}
    req = urllib2.Request(url, headers= header)
    con = urllib2.urlopen( req )
    doc = con.read()
    con.close()
    soup = BeautifulSoup.BeautifulSoup(doc)
    main_Components = soup.findAll('li', {'class' : 'ingtmgr'})
    main_Co = ass_Co = ''
    for index_main in range(0, len(main_Components)):
        main_Co += main_Components[index_main].find('a').text
        main_Co += '|'
        main_Co += main_Components[index_main].find('span').text
        main_Co += ';'
    ass_Components = soup.findAll('li', {'class' : 'ingtbur'})
    for index_ass in range(0, len(ass_Components)):
        ass_Co += ass_Components[index_ass].find('p').text
        ass_Co += '|'
        ass_Co += ass_Components[index_ass].find('span').text
        ass_Co += ';'
    output = [main_Co,ass_Co]
    return output

def writeSheet1(row_index_sheet, write_sheet1):
    try:
        for index_sheet1_first in range(22):
            sheet1.write(row_index_sheet[0], index_sheet1_first, write_sheet1[index_sheet1_first])
        for index_sheet1_end in range(22, 32):
            sheet1.write(row_index_sheet[0], index_sheet1_end, write_sheet1[22][index_sheet1_end - 22])
        book.save('%s.xls' % number)
        row_index_sheet[0] += 1
    except:
        print('error1')
    return row_index_sheet

def writeSheet2(row_index_sheet, food_id, food_name, food_img, food_price, food_praise, food_detail, food_count, rid):
    try:
        flag_Co = flag_Filter = True
        flag_Name_Filter = ['套餐','+']
        for flag_index in range(0,len(flag_Name_Filter)):
            if(food_name.encode('utf-8').find(flag_Name_Filter[flag_index]) != -1):
                flag_Co = False
        flag_Name_Number_First = ['一','二','三','四','五','六','七','八','九','十','1','2','3','4','5','6','7','8','9']
        flag_Name_Number_Second = ['丁','只','双','份','条','个','根','片','卷','颗','斤']
        for flag_index_first in range(0,len(flag_Name_Number_First)):
            if(food_name.encode('utf-8').find(flag_Name_Number_First[flag_index_first]) != -1):
                for flag_index_second in range(0, len(flag_Name_Number_Second)):
                    if(food_name.encode('utf-8').find(flag_Name_Number_Second[flag_index_second]) != -1):
                        flag_Filter = False
            if(flag_Filter == False):
                food_name = (food_name[0:food_name.encode('utf-8').find(flag_Name_Number_First[flag_index_first])] + food_name[food_name.encode('utf-8').find(flag_Name_Number_First[flag_index_first])+2 :])
                break
        flag_Name_Slash = ['/', '(']
        for flag_index_slash in range(0, len(flag_Name_Slash)):
            if(food_name.find(flag_Name_Slash[flag_index_slash]) != -1):
                food_name = food_name[0:food_name.find(flag_Name_Slash[flag_index_slash])]
                break
        food_iscom = '1'
        main_Co = ass_Co = ''
        if flag_Co == True:
            food_iscom = ''
            try:
                recipe = getRecipe(food_name.encode('utf-8'))
                if(recipe[0][0] == food_name):
                    main_Co = getComponents(recipe[0][1])[0]
                    ass_Co = getComponents(recipe[0][1])[1]
                elif(recipe[1][0] == food_name):
                    main_Co = getComponents(recipe[1][1])[0]
                    ass_Co = getComponents(recipe[1][1])[1]
                elif(recipe[2][0] == food_name):
                    main_Co = getComponents(recipe[2][1])[0]
                    ass_Co = getComponents(recipe[2][1])[1]
            except:
                main_Co = ass_Co = ''
        sheet2.write(row_index_sheet[1],0,food_id)
        sheet2.write(row_index_sheet[1],1,food_name)
        sheet2.write(row_index_sheet[1],2,food_img)
        sheet2.write(row_index_sheet[1],3,food_price)
        sheet2.write(row_index_sheet[1],4,food_praise)
        sheet2.write(row_index_sheet[1],5,food_detail)
        sheet2.write(row_index_sheet[1],6,food_count)
        sheet2.write(row_index_sheet[1],7,rid)
        sheet2.write(row_index_sheet[1],8,main_Co)
        sheet2.write(row_index_sheet[1],9,ass_Co)
        sheet2.write(row_index_sheet[1],10,food_iscom)
        book.save('%s.xls' % number)
        row_index_sheet[1] += 1
        print(row_index_sheet[1])
    except:
        print('error2')
    return row_index_sheet

def getData(city, shopid, row_index_sheet, poi, address):
    try:
        url = 'http://waimai.meituan.com/restaurant/' + shopid
        header_host = 'waimai.meituan.com'
        header = {'Host': header_host}
        req = urllib2.Request(url, headers = header)
        con = urllib2.urlopen( req )
        doc = con.read()
        con.close()
        soup = BeautifulSoup.BeautifulSoup(doc)
        name = soup.find('div', {'class' : 'shopping-cart clearfix'}).get('data-poiname')               # 名称
        rid = soup.find('div', {'class' : 'shopping-cart clearfix'}).get('data-poiid')                  # 餐馆ID
        region = address                                                                                # 地域
        img = soup.find('div', {'class' : 'avatar fl'}).find('img').get('src')                          # 餐厅缩略图
        score = soup.find('div', {'class' : 'rest-info'}).find('div', {'class' : 'fl ack-ti'}).find('div', {'class' :'nu'}).text # 评分
        deliver_time = soup.find('div', {'class' : 'rest-info'}).find('div', {'class' : 'fl average-speed'}).find('div', {'class' :'nu'}).text # 平均送餐时间
        try:
            deliver_text1 = soup.find('div', {'class' : 'rest-info'}).find('div', {'class' : 'fl average-speed'}).find('p').text  # 餐厅大约在42分钟内将美食送达
            deliver_text2 = soup.find('div', {'class' : 'rest-info'}).find('div', {'class' : 'fl average-speed'}).find('p', {'class' :'ct-red red-text'}).text # 快于周边34%的餐厅
        except:
            deliver_text1 = ''
            deliver_text2 = ''
        deliver_rate = soup.find('div', {'class' : 'rest-info'}).find('div', {'class' : 'fl in-ti'}).find('div', {'class' :'nu'}).text # 及时送餐率
        try:
            deliver_text3 = soup.find('div', {'class' : 'rest-info'}).find('div', {'class' : 'fl in-ti'}).find('p').text # 75%的订单会在45分钟内送达
            deliver_text4 = soup.find('div', {'class' : 'rest-info'}).find('div', {'class' : 'fl in-ti'}).find('p', {'class' : 'ct-red red-text'}).text # 高于周边30%的餐厅
        except:
            deliver_text3 = ''
            deliver_text4 = ''
        fee = soup.find('div', {'class' : 'rest-info-thirdpart'})
        pattern = re.compile("(?<=<span>)(.*?)(元起送)")
        fee_delivermin = pattern.findall(fee.__str__())[0][0] # 起送费
        try:
            pattern = re.compile("(?<=nbsp;)(.*?)(元配送费)")
            fee_deliver = pattern.findall(fee.__str__())[0][0] # 配送费
        except:
            fee_deliver = 0
        try:
            pattern = re.compile("(?<=配送&nbsp;)(.*?)(<)")
            deliver_type = pattern.findall(fee.__str__())[0][0] # 配送方式 ex：由餐厅配送
        except:
            pattern = re.compile("(?<=配送费&nbsp;)(.*?)(<)")
            deliver_type = pattern.findall(fee.__str__())[0][0] # 配送方式 ex：由餐厅配送
        addr = soup.find('div', {'class' : 'location fl'}).find('span', {'class' : 'fl info-detail'}).text # 餐厅地址
        timestamp = soup.find('div', {'class' :'delivery-time fl'}).find('span', {'class' : 'fl info-detail'}).text # 营业时间
        try:
            tips = soup.find('div', {'class' : 'widgets fr'}).find('div', {'class': 'loading'}).text # 订餐必读&商家公告
        except:
            tips = ''
        savecount = soup.find('p', {'class' : 'cc-lightred-new j-save-up-people'}).text
        savecount = savecount.replace('(', '')
        savecount = savecount.replace(')', '')
        # icon = ['i-zero','i-free','i-delivery','i-pay', 'i-cheque', 'i-free-gift', 'i-first', 'i-minus','i-ph17x17','i-ding', 'i-reimbursement'] # 零，免，送，付，票，赠，首，减，饮，订，赔
        icon = ['','','','','','','','','','','']
        discount_all = soup.find('div',{'class' : 'widget discount'}).findAll('p')
        for discount_index in range(len(discount_all)):
            if(discount_all[discount_index].find('i',{'class' : 'icon i-zero'}) != None):
                icon[0] = '零起送价'
            elif(discount_all[discount_index].find('i',{'class' : 'icon i-free'}) != None):
                icon[1] = '免配送费'
            elif(discount_all[discount_index].find('i',{'class' : 'icon i-delivery'}) != None):
                icon[2] = discount_all[discount_index].find('span',{'class' : 'discount-desc'}).text
            elif(discount_all[discount_index].find('i',{'class' : 'icon i-pay'}) != None):
                icon[3] = discount_all[discount_index].find('span',{'class' : 'discount-desc'}).text
            elif(discount_all[discount_index].find('i',{'class' : 'icon i-cheque'}) != None):
                icon[4] = discount_all[discount_index].find('span',{'class' : 'discount-desc'}).text
            elif(discount_all[discount_index].find('i',{'class' : 'icon i-free-gift'}) != None):
                icon[5] = discount_all[discount_index].find('span',{'class' : 'discount-desc'}).text
            elif(discount_all[discount_index].find('i',{'class' : 'icon i-first'}) != None):
                icon[6] = discount_all[discount_index].find('span',{'class' : 'discount-desc'}).text
            elif(discount_all[discount_index].find('i',{'class' : 'icon i-minus'}) != None):
                icon[7] = discount_all[discount_index].find('span',{'class' : 'discount-desc'}).text
            elif(discount_all[discount_index].find('i',{'class' : 'icon i-ph17x17'}) != None):
                icon[8] = discount_all[discount_index].find('span',{'class' : 'discount-desc'}).text
            elif(discount_all[discount_index].find('i',{'class' : 'icon i-ding'}) != None):
                icon[9] = discount_all[discount_index].find('span',{'class' : 'discount-desc'}).text
            elif(discount_all[discount_index].find('i',{'class' : 'icon i-reimbursement'}) != None):
                icon[10] = discount_all[discount_index].find('span',{'class' : 'discount-desc'}).text
        param = getLngLat(addr, city)
        if(param[0] == 0):
            param[0] = param[1] = ''
        write_sheet1 = [city, region, rid ,url,name,img,score,timestamp,addr,param[0],param[1],deliver_time,deliver_text1,deliver_text2,deliver_rate,deliver_text3,deliver_text4,fee_delivermin,fee_deliver,deliver_type,savecount,tips,icon]
        row_index_sheet = writeSheet1(row_index_sheet,write_sheet1)
        arr = [[],[],[],[],[]]
        arr[0] = soup.findAll('div',{'class' : 'j-pic-food pic-food  '})
        arr[1] = soup.findAll('div',{'class' : 'j-pic-food pic-food pic-food-col2 '})
        arr[2] = soup.findAll('div',{'class' : 'j-pic-food pic-food  pic-food-rowlast'})
        arr[3] = soup.findAll('div',{'class' : 'j-pic-food pic-food pic-food-col2 pic-food-rowlast'})
        arr[4] = soup.findAll('div',{'class' : 'j-text-food text-food clearfix'})
        for food_index in range(4):
            if(arr[food_index] != []):
                for arr0_index in range(len(arr[food_index])):
                    food_id = arr[food_index][arr0_index].get('id')
                    food_name = arr[food_index][arr0_index].find('span',{'class' : 'name fl'}).get('title')
                    try:
                        food_detail = arr[food_index][arr0_index].find('div',{'class' : 'description'}).text
                    except:
                        food_detail = ''
                    food_img = arr[food_index][arr0_index].find('img').get('data-src')
                    food_price = arr[food_index][arr0_index].find('div',{'class':'price fl'}).text
                    food_price = food_price.replace('&yen;','')
                    try:
                        food_praise = arr[food_index][arr0_index].find('span',{'class' : 'cc-lightred-new'}).text
                        food_praise = food_praise.replace('(','')
                        food_praise = food_praise.replace(')','')
                    except:
                        food_praise = '0'
                    food_count = arr[food_index][arr0_index].find('div',{'class':'sold-count ct-middlegrey'}).text
                    row_index_sheet = writeSheet2(row_index_sheet, food_id, food_name, food_img, food_price, food_praise, food_detail, food_count, rid)
        if(arr[4] != []):
            for arr1_index in range(len(arr[4])):
                food_id = arr[4][arr1_index].get('id')
                try:
                    food_name = arr[4][arr1_index].find('div', {'class' : 'na nodesc'}).get('title')
                except:
                    food_name = arr[4][arr1_index].find('div', {'class' : 'na '}).get('title')
                try:
                    food_detail = arr[4][arr1_index].find('div', {'class' : 'desc ct-lightgrey'}).get('title')
                except:
                    food_detail = ''
                food_img = ''
                food_price = arr[4][arr1_index].find('div', {'class' : 'fr unit-price'}).text
                food_price = food_price.replace('&yen;', '')
                try:
                    food_praise = arr[4][arr1_index].find('span', {'class': 'cc-lightred-new'}).text
                    food_praise = food_praise.replace('(', '')
                    food_praise = food_praise.replace(')', '')
                except:
                    food_praise = '0'
                try:
                    food_count = arr[4][arr1_index].find('div',{'class': 'count ct-middlegrey '}).text
                except:
                    food_count = arr[4][arr1_index].find('div',{'class': 'count ct-middlegrey no-zan'}).text
                row_index_sheet = writeSheet2(row_index_sheet, food_id, food_name, food_img, food_price, food_praise, food_detail, food_count, rid)
    except:
        print('error')
    return row_index_sheet

def unique(old_list):
    newList = []
    for x in old_list:
        if x not in newList :
            newList.append(x)
    return newList

if __name__ == "__main__":
    regionlist = getregion('beijing')
    regionlist = unique(regionlist)
    global row_index_sheet,flag,number,shoplist_unique,city
    city = '北京'
    shoplist_unique = []
    flag = False
    number = 0
    for address_index in range(0, len(regionlist)):
        try:
            row_index_sheet = [0,0]
            number += 1
            book = Workbook(encoding='utf-8') # 如果采集数据有中文，需要添加这个
            sheet1 = book.add_sheet('餐馆') # 表格缓存
            sheet2 = book.add_sheet('菜品') # 表格缓存
            address = regionlist[address_index]
            print(address)
            poi = getLngLat(address, city)
            list = getList(poi)
            print(list)
            # getdata(list[51], 0, poi, region)
            for list_index in range (0,len(list)):
                try:
                    if(list[list_index] not in shoplist_unique):
                        shoplist_unique.append(list[list_index])
                        row_index_sheet = getData(city, list[list_index], row_index_sheet, poi, address)
                except:
                    print(list_index)
        except:
            address_index = address_index