# The library needed to crawl data
import time
import requests
import re
import pandas as pd
from lxml import etree
from multiprocessing import Pool
import pymysql


# Crawling data programs
def DingDianSpider(url):
    # Set up an empty list to store dictionaries of each rental information later
    count = list()

    # Get the main page of the rental site and convert
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'}
    response = requests.get(url=url, headers=headers).text
    tree = etree.HTML(response)

    i = 0
    try:
        while i <= 39:
            try:
                # Get the information and links of each rental label on the main page
                li_List = tree.xpath("//*[@class='sc-63c588db-0 fEeWHy']/div[3]/ul/li")[i]
                title = li_List.xpath('./section/div/div/div/h3/a/text()')
                # print(f'Title: {title}')
                price = li_List.xpath('./section/div/div/div/div/p/text()')
                p = price[0].replace('$', '')

                link = li_List.xpath('./section/div/div[2]/div/h3/a/@href')[0]

                # Go into the Properties label page for more detailed information
                next_url = f'https://www.kijiji.ca{link}'
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'}
                next_response = requests.get(url=next_url, headers=headers).text
                next_tree = etree.HTML(next_response)

                map_url = f"{next_url}#map"

                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'}
                map_response = requests.get(url=map_url, headers=headers).text
                map_tree = etree.HTML(map_response)

                # Parse the website and transform the data
                latitude = map_tree.xpath('//*[@property="og:latitude"]/@content')

                longitude = map_tree.xpath('//*[@property="og:longitude"]/@content')

                # Detailed information
                Type1 = next_tree.xpath('//*[@id="vip-body"]/div[2]/div[3]/div[1]/li[1]/span/text()')

                Time = next_tree.xpath('//*[@id="vip-body"]/div[2]/div[2]/div[2]/time/text()')
                if Time != []:
                    pass
                else:
                    Time = ["Over a month ago"]

                location = next_tree.xpath('//*[@id="vip-body"]/div[2]/div[2]/div[1]/span/text()')

                bedroom = next_tree.xpath('//*[@id="vip-body"]/div[2]/div[3]/div[1]/li[2]/span/text()')
                x = bedroom[0]
                b1 = x.replace('Bedrooms: ', '')
                if "Den" in b1:
                    b1 = b1.replace(" + Den", '')
                    b1 = int(b1) + 0.5
                    b1 = str(b1)
                if b1 == 'Bachelor/Studio':
                    b1 = '0'

                bathroom = next_tree.xpath('//*[@id="vip-body"]/div[2]/div[3]/div[1]/li[3]/span/text()')
                y = bathroom[0]
                b2 = y.replace('Bathrooms: ', '')

                Utilities_Included = next_tree.xpath(
                    '//*[@id="vip-body"]/div[3]/div[2]/div[1]/div[1]/div[1]/ul/li/div/ul/li/svg/@aria-label')
                if Utilities_Included != []:
                    pass
                else:
                    Utilities_Included = ["Not included"]

                Wi_Fi = next_tree.xpath('//*[@id="vip-body"]/div[3]/div[2]/div[1]/div[1]/div[1]/ul/li[2]/div/ul/text()')
                if Wi_Fi == []:
                    Wi_Fi = next_tree.xpath(
                        '//*[@id="vip-body"]/div[3]/div[2]/div[1]/div[1]/div[1]/ul/li[2]/div/ul/li/text()')
                else:
                    Wi_Fi = ["Not included"]

                Parking_Included = next_tree.xpath(
                    '//*[@id="vip-body"]/div[3]/div[2]/div[1]/div[1]/div[1]/ul/li[3]/dl/dd/text()')

                Agreement_Type = next_tree.xpath(
                    '//*[@id="vip-body"]/div[3]/div[2]/div[1]/div[1]/div[1]/ul/li[4]/dl/dd/text()')

                Move_In_Date = next_tree.xpath(
                    '//*[@id="vip-body"]/div[3]/div[2]/div[1]/div[1]/div[1]/ul/li[5]/dl/dd/span/text()')
                if Move_In_Date == []:
                    Move_In_Date = ["Unknown"]

                    Pet_Friendly = next_tree.xpath(
                        '//*[@id="vip-body"]/div[3]/div[2]/div[1]/div[1]/div[1]/ul/li[5]/dl/dd/text()')
                else:
                    Pet_Friendly = next_tree.xpath(
                        '//*[@id="vip-body"]/div[3]/div[2]/div[1]/div[1]/div[1]/ul/li[6]/dl/dd/text()')

                Size = next_tree.xpath('//*[@id="vip-body"]/div[3]/div[2]/div[1]/div[1]/div[2]/ul/li[1]/dl/dd/text()')

                Furnished = next_tree.xpath(
                    '//*[@id="vip-body"]/div[3]/div[2]/div[1]/div[1]/div[2]/ul/li[2]/dl/dd/text()')

                appliance1 = next_tree.xpath(
                    f'//*[@id="vip-body"]/div[3]/div[2]/div[1]/div[1]/div[2]/ul/li[3]/div/ul/li[1]/text()')
                appliance2 = next_tree.xpath(
                    f'//*[@id="vip-body"]/div[3]/div[2]/div[1]/div[1]/div[2]/ul/li[3]/div/ul/li[2]/text()')
                appliance3 = next_tree.xpath(
                    f'//*[@id="vip-body"]/div[3]/div[2]/div[1]/div[1]/div[2]/ul/li[3]/div/ul/li[3]/text()')

                Appliances = []
                Appliances = Appliances + appliance1 + appliance2 + appliance3
                if Appliances != []:
                    pass
                else:
                    Appliances = ["Not included"]

                Air_conditioning = next_tree.xpath(
                    '//*[@id="vip-body"]/div[3]/div[2]/div[1]/div[1]/div[2]/ul/li[4]/dl/dd/text()')

                Outdoor_space = next_tree.xpath(
                    '//*[@id="vip-body"]/div[3]/div[2]/div[1]/div[1]/div[2]/ul/li[5]/div/ul/li/text()')
                if Outdoor_space != []:
                    pass
                else:
                    Outdoor_space = ["Not included"]

                Smoking = next_tree.xpath(
                    '//*[@id="vip-body"]/div[3]/div[2]/div[1]/div[1]/div[2]/ul/li[6]/dl/dd/text()')

                if price[0] == 'Please Contact' or Size[0] == 'Not Available':
                    price_per_sqft = 'Please Contact'
                else:
                    compute_price = re.findall("\d*", price[0])
                    b = "".join(compute_price)
                    compute_size = re.findall("\d*", Size[0])
                    c = "".join(compute_size)
                    price_per_sqft = f"{float(float(b) / float(c) / 100)}"

                # Store rental information in dictionary
                dic = {"Title": title[0], "Website": next_url, "Price": p, "Price per square foot": price_per_sqft,
                       "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                       "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                       "Utilities Included": (", ".join(Utilities_Included)),
                       "Wi Fi and More": (", ".join(Wi_Fi)), "Parking Included": Parking_Included[0],
                       "Agreement Type": Agreement_Type[0], "Move In Date": Move_In_Date[0],
                       "Pet Friendly": Pet_Friendly[0],
                       "Size(sqft)": Size[0], "Furnished": (", ".join(Furnished)),
                       "Appliances": (", ".join(Appliances)), "Air Conditioning": Air_conditioning[0],
                       "Personal Outdoor Space": (" ".join(Outdoor_space)), "Smoking Permitted": Smoking[0]}

                count.append(dic)
            except Exception:
                print("Error")
            i = i + 1
    except Exception:
        print("That's all")
    return count


# Set up parallel processing to improve crawling speed, and convert data to Dataframe format and export to Excel

if __name__ == '__main__':
    urls = [f'https://www.kijiji.ca/b-apartments-condos/halifax/page-{a}/c37l80010' for a in range(1, 20)]
    pool = Pool(processes=20)
    results = pool.map(DingDianSpider, urls)
    pool.close()
    pool.join()
    flattened_results = [item for sublist in results for item in sublist]
    data = pd.DataFrame(flattened_results)
    # data.to_excel('Canada Rental House.xlsx', index=False)
    db_config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'Kingho325',
        'db': '租房数据',
        'charset': 'utf8'
    }

    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('''TRUNCATE TABLE 租房数据''')

        # Create a table to store rental data if it doesn't exist
        create_table_query = '''CREATE TABLE IF NOT EXISTS 租房数据
                     (Title TEXT, Location TEXT, Price TEXT, Size_sqft TEXT, Price_per_square_foot TEXT, Agreement_Type TEXT, Type TEXT, Website TEXT, 
                      Post_Time TEXT, Latitude TEXT, Longitude TEXT, Bedroom TEXT, Bathroom TEXT, Utilities_Included TEXT, Wi_Fi_and_More TEXT, 
                      Parking_Included TEXT, Move_In_Date TEXT, Pet_Friendly TEXT, Furnished TEXT, Appliances TEXT, Air_Conditioning TEXT, 
                      Personal_Outdoor_Space TEXT, Smoking_Permitted TEXT)'''

        cursor.execute(create_table_query)
        conn.commit()

        # Insert data into the database
        insert_query = '''INSERT INTO 租房数据 (Title, Location, Price, Size_sqft, Price_per_square_foot, Agreement_Type, Type, Website, 
                                Post_Time, Latitude, Longitude, Bedroom, Bathroom, Utilities_Included, Wi_Fi_and_More, Parking_Included, 
                                Move_In_Date, Pet_Friendly, Furnished, Appliances, Air_Conditioning, Personal_Outdoor_Space, Smoking_Permitted) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        for item in flattened_results:
            cursor.execute(insert_query, (
                item['Title'], item['Location'], item['Price'], item['Size(sqft)'], item['Price per square foot'],
                item['Agreement Type'], item['Type'], item['Website'], item['Post Time'], item['Latitude'],
                item['Longitude'],
                item['Bedroom'], item['Bathroom'], item['Utilities Included'], item['Wi Fi and More'],
                item['Parking Included'],
                item['Move In Date'], item['Pet Friendly'], item['Furnished'], item['Appliances'],
                item['Air Conditioning'],
                item['Personal Outdoor Space'], item['Smoking Permitted']))

        conn.commit()
        print("Data inserted successfully.")
        # Set the scheduled tasks
        delay = 3600
        time.sleep(delay)
        print('Next')

    except pymysql.Error as e:
        print("Error inserting data into MySQL table:", e)

    finally:
        if conn:
            conn.close()



