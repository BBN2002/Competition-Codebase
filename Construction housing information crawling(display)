# The library needed to crawl data
import requests
import pandas as pd
from lxml import etree
import pymysql
import time
import schedule

def crawl_and_store_data():
    # The library needed to crawl data
    count=list()

    url = "https://www.apartments.com/apartments/halifax-ns/?kw=New"

    # The library needed to crawl data
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'}
    response = requests.get(url=url, headers=headers).text
    tree = etree.HTML(response)

    i = 0

    try:
        while i <= 12:
            # Get the information and links of each rental label on the main page
            li_List = tree.xpath("//*[@id='placardContainer']/ul/li")[i]
            title = li_List.xpath("./article/section/div/div[2]/div/div/a/p/span/text()")
            print(f'Main Title: {title[0]}')

            location = li_List.xpath("./article/section/div/div[2]/div/div/a/p[2]/text()")

            link = li_List.xpath("./article/section/div/div[2]/div/div/a/@href")
            next_link = link[0]
            # Go into the Properties label page for more detailed information
            next_response = requests.get(url=next_link, headers=headers).text
            next_tree = etree.HTML(next_response)

            # Parse the website and transform the data
            detailed_location_A = next_tree.xpath('//*[@property="place:location:latitude"]/@content')

            detailed_location_B = next_tree.xpath('//*[@property="place:location:longitude"]/@content')

            a = 0
            try:
                while a <= 2:
                    info_list = next_tree.xpath('//*[@data-tab-content-id="all"]/div')[a]

                    bedroom = info_list.xpath('./div/div/div/div/h4/span/span[1]/text()')
                    # print(bedroom[0])

                    bathroom = info_list.xpath('./div/div/div/div/h4/span/span[2]/text()')
                    # print(bathroom[0])

                    b = 0
                    try:
                        while b <= 5:
                            next_info_list = info_list.xpath('./div[2]/div/ul/li')[b]
                            price = next_info_list.xpath('./div/div[2]/span[2]/text()')

                            space = next_info_list.xpath('./div/div[3]/span[2]/text()')
                            if space[0] == '':
                                space[0] = "None"

                            Available_time = next_info_list.xpath('./div/div[4]/div/span/text()')
                            dic = {"title": title[0], "link": next_link, "location": location[0],
                                   'latitude': detailed_location_A[0], "longitude": detailed_location_B[0], "price": price[0],"bedroom": bedroom[0], 'bathroom': bathroom[0],
                                   "space": space[0],"available time": 'Please contact'
                                }

                            count.append(dic)
                            b = b + 1
                    except Exception:
                        print(" ")
                    a = a + 1
            except Exception:
                print(" ")
                c = 0
            try:
                if c == 0:
                    price = next_tree.xpath('//*[@class="priceBedRangeInfoContainer"]/ul/li[1]/div/p[2]/text()')

                    bedroom = next_tree.xpath('//*[@class="priceBedRangeInfoContainer"]/ul/li[2]/div/p[2]/text()')

                    bathroom = next_tree.xpath('//*[@class="priceBedRangeInfoContainer"]/ul/li[3]/div/p[2]/text()')

                    space = next_tree.xpath('//*[@class="priceBedRangeInfoContainer"]/ul/li[4]/div/p[2]/text()')
                    if space == []:
                        space = "None"
                    # Store rental information in dictionary
                    dic = {"title": title[0], "link": next_link, "location": location[0],
                           'latitude': detailed_location_A[0], "longitude": detailed_location_B[0], "price": price[0],
                           "bedroom": bedroom[0], 'bathroom': bathroom[0],
                           "space": space[0], "available time": 'Please contact'
                           }
                    count.append(dic)
            except Exception:
                print(' ')
            i = i + 1
    except Exception:
        print(' ')

    url = "https://killamreit.com/apartments/halifax-ns/5206-tobin-street"

    # Get the main page of the rental site and convert
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'}
    response = requests.get(url=url, headers=headers).text
    tree = etree.HTML(response)

    i = 0

    while i <= 14:
        # Get the information and links of each rental label on the main page
        li_List = tree.xpath(
            "//*[@class='uk-slider-items uk-child-width-1 uk-child-width-1-2@m uk-child-width-1-3@l uk-grid']/li")[i]
        title = li_List.xpath("./div/a/div/div[1]/text()")
        print(f'Main Title: {title[0]}')

        location = li_List.xpath("./div/a/div/div[2]/text()")
        location[0] = location[0].replace('  ', '')

        link = li_List.xpath("./div/a/@href")[0]

        # Go into the Properties label page for more detailed information
        next_link = f'https://killamreit.com{link}'
        next_response = requests.get(url=next_link, headers=headers).text
        next_tree = etree.HTML(next_response)

        a = 0

        try:
            while a <= 6:
                # Parse the website and transform the data
                next_li = next_tree.xpath(
                    "//*[@class='views-element-container c-all-apartments block block-views block-views-blockunits-all-units']/div/div/div/div")[
                    a]
                info = next_li.xpath('./div/div/div[2]/text()')
                info[0] = info[0].replace('$', '')
                info[3] = info[3].replace(' Ft', '')

                detailed_location_A = next_tree.xpath("//*[@id='killam-property-page-map']/@data-lat")
                detailed_location_B = next_tree.xpath("//*[@id='killam-property-page-map']/@data-lng")

                dic = {"title": title[0], "link": next_link, "location": location[0],
                       "latitude": detailed_location_A[0], "longitude": detailed_location_B[0], "price": info[0],
                       'bedroom': info[1], "bathroom": info[2], "space": info[3],
                       "available time": info[4]}
                count.append(dic)

                a = a + 1
        except Exception:
            # print("That's all")

            # Store rental information in dictionary
            dic = {"title": title[0], "link": next_link, 'location': location[0], 'latitude': detailed_location_A[0],
                   'longitude': detailed_location_B[0], "price": 'Please contact', 'bedroom': 'Please contact', "bathroom": 'Please contact', "space": 'Please contact',
                   "available time": 'Please contact'}
            count.append(dic)

        i = i + 1

    # convert data to Dataframe format
    data=pd.DataFrame(count)

    # Connect to server database
    db_config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'Kingho325',
        'db': '租房数据',
        'charset': 'utf8'
    }

    conn = pymysql.connect(**db_config)

    cursor = conn.cursor()

    # create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS 在建房数据 (
                           title TEXT,
                           link TEXT,
                           location TEXT,
                           latitude TEXT,
                           longitude TEXT,
                           price TEXT,
                           bedroom TEXT,
                           bathroom TEXT,
                           space TEXT,
                           available_time TEXT
                           )''')

    conn.commit()

    # clean the data in the previous table
    cursor.execute('''TRUNCATE TABLE 在建房数据''')

    # update the data
    for index, row in data.iterrows():
        cursor.execute('''INSERT INTO 在建房数据 (title, link, location, latitude, longitude, price, bedroom, bathroom, space, available_time)
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (
        row['title'], row['link'], row['location'], row['latitude'], row['longitude'], row['price'], row['bedroom'],
        row['bathroom'], row['space'], row['available time']))

    conn.commit()

    cursor.close()
    conn.close()
    # print(data)

    print('Done')
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

# Set the scheduled tasks
schedule.every().minute.do(crawl_and_store_data)

while True:
    schedule.run_pending()
    time.sleep(1)
