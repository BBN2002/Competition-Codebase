# The library needed to crawl data
import pandas as pd
from lxml import etree
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
import re
import pymysql

# Crawling data programs
def DingDianSpider(next_url):
    # Set up an empty list to store dictionaries of each rental information later
    count = list()
    # Use the Selenium library to emulate a browser and get the full source code of your rental website
    try:
        browser = webdriver.Chrome()
        try:
            browser.get(next_url)
            browser.maximize_window()
            js = 'document.documentElement.scrollTop=2000'
            browser.execute_script(js)
            time.sleep(20)
            wait = WebDriverWait(browser, 20)
            next = browser.page_source
        finally:
            browser.close()
            next_tree = etree.HTML(next)

        # Parse the website and transform the data
        title = next_tree.xpath('//*[@class="chakra-heading css-za1032-display32To40 e1k4it830"]/text()')
        print(title[0])

        location = next_tree.xpath('//*[@class="chakra-text css-1edh6hj e1k4it830"]/text()')

        detailed_location = next_tree.xpath('//*[@class="chakra-button css-1md3vsv e1k4it830"]/@href')

        latitude = re.findall('\d\d.\d+',detailed_location[0])

        longitude = re.findall('-\d\d.\d+',detailed_location[0])

        # Acquire data sets and classify them
        info = next_tree.xpath('//*[@id="amenities"]//text()')

        info = ",".join(info)

        if "Internet" in info:
            Wi_Fi = 'Internet'
        else:
            Wi_Fi = 'Not included'

        if 'Cats OK' and 'Dogs OK' in info:
            Pet_Friendly = 'Yes'
        elif 'Cats OK' or 'Dogs OK'in info:
            Pet_Friendly = 'Limited'
        else:
            Pet_Friendly = 'No'

        if 'Balcony' and 'Yard' in info:
            Outdoor_space = 'Yard Balcony'
        elif 'Balcony' in info:
            Outdoor_space = 'Balcony'
        elif 'Yard' in info:
            Outdoor_space = 'Yard'
        else:
            Outdoor_space = 'Not included'

        if 'Air Conditioning' in info:
            Air_conditioning = 'Yes'
        else:
            Air_conditioning = 'No'

        Move_In_Date = 'Unknown'

        if 'Appliances' and 'Apartment Amenities' in info:
            Furnished = 'Yes'
        else:
            Furnished = 'No'

        if 'In-Unit Laundry' and 'Dishwasher' in info:
            Appliances = 'Laundry (In Unit), Dishwasher'
        elif 'Onsite Laundry' and 'Dishwasher' in info:
            Appliances = 'Laundry (In Building), Dishwasher'
        elif 'Onsite Laundry' and 'Dishwasher' and 'In-Unit Laundry' in info:
            Appliances = 'Laundry (In Building), Laundry (In Unit), Dishwasher'
        elif 'Onsite Laundry' in info:
            Appliances = 'Laundry (In Building)'
        elif 'In-Unit Laundry' in info:
            Appliances = 'Laundry (In Unit)'

        if 'Heat' and 'Water' and 'Swimming Pool' in info:
            Utilities_Included = 'Yes: Hydro, Yes: Heat, Yes: Water'
        elif 'Heat' and 'Water' in info:
            Utilities_Included = 'No: Hydro, Yes: Heat, Yes: Water'
        elif 'Heat' and 'Swimming Pool' in info:
            Utilities_Included = 'Yes: Hydro, Yes: Heat, No: Water'
        elif 'Water' and 'Swimming Pool' in info:
            Utilities_Included = 'Yes: Hydro, No: Heat, Yes: Water'
        elif 'Water' in info:
            Utilities_Included = 'No: Hydro, No: Heat, Yes: Water'
        elif 'Swimming Pool' in info:
            Utilities_Included = 'Yes: Hydro, No: Heat, No: Water'
        elif 'Heat' in info:
            Utilities_Included = 'No: Hydro, Yes: Heat, No: Water'
        else:
            Utilities_Included = 'Not included'

        # Acquire other data sets and classify them
        detailed_info = next_tree.xpath('//*[@id="floor-plans"]//text()')

        Type1 = next_tree.xpath('//*[@class="chakra-button css-g12s8k"]/text()')

        Type1[0] = Type1[0].replace("Halifax ","")


        Agreement_Type = 'Month-to-month'

        if 'GROUNDS' and "Garage Parking" in info:
            Parking_Included = '1'
        elif 'GROUNDS' and "Assigned Parking" in info:
            Parking_Included = '1'
        elif 'GROUNDS' and "Assigned Parking" and "Garage Parking"  in info:
            Parking_Included = '2'
        else:
            Parking_Included = '0'

        Smoking = 'No'

        Time = next_tree.xpath("//*[@class='css-7qlyqh e1k4it830']/text()")

        info_list = []
        for item in detailed_info:
            if ' bed' in item or ' bath' in item or '$' in item or 'sqft' in item or 'Studio' in item :
                info_list.append(item)
        if info_list[0] == 'Studio':
            info_list.pop(0)

        # Determine how much data to store based on the number of rentals in a subpage
        if len(info_list) == 4:
            b1 = info_list[0].replace(' bed','')
            b2 = info_list[1].replace(' bath','')
            size = info_list[2].replace(' sqft','')
            price = info_list[3].replace('$','')
            price = price.replace(' /mo','')
            price = price.replace(',','')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)

        elif len(info_list) == 3:
            b1 = info_list[0].replace(' bed','')
            b2 = info_list[1].replace(' bath','')
            size = 'Not Available'
            price = info_list[3].replace('$','')
            price = price.replace(' /mo','')
            price = price.replace(',', '')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)

        elif len(info_list) == 5:
            info_list.pop(0)
            b1 = info_list[0].replace(' bed', '')
            b2 = info_list[1].replace(' bath', '')
            size = info_list[2].replace(' sqft', '')
            price = info_list[3].replace('$', '')
            price = price.replace(' /mo', '')
            price = price.replace(',', '')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)

        elif len(info_list) == 8:
            b1 = info_list[0].replace(' bed', '')
            b2 = info_list[1].replace(' bath', '')
            size = info_list[2].replace(' sqft', '')
            price = info_list[3].replace('$', '')
            price = price.replace(' /mo', '')
            price = price.replace(',', '')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)
            b1 = info_list[4].replace(' bed', '')
            b2 = info_list[5].replace(' bath', '')
            size = info_list[6].replace(' sqft', '')
            price = info_list[7].replace('$', '')
            price = price.replace(' /mo', '')
            price = price.replace(',', '')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)

        elif len(info_list) == 16:
            b1 = info_list[0].replace(' bed', '')
            b2 = info_list[1].replace(' bath', '')
            size = info_list[2].replace(' sqft', '')
            price = info_list[3].replace('$', '')
            price = price.replace(' /mo', '')
            price = price.replace(',', '')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)
            b1 = info_list[4].replace(' bed', '')
            b2 = info_list[5].replace(' bath', '')
            size = info_list[6].replace(' sqft', '')
            price = info_list[7].replace('$', '')
            price = price.replace(' /mo', '')
            price = price.replace(',', '')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)

        elif len(info_list) == 24:
            b1 = info_list[0].replace(' bed', '')
            b2 = info_list[1].replace(' bath', '')
            size = info_list[2].replace(' sqft', '')
            price = info_list[3].replace('$', '')
            price = price.replace(' /mo', '')
            price = price.replace(',', '')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)
            b1 = info_list[4].replace(' bed', '')
            b2 = info_list[5].replace(' bath', '')
            size = info_list[6].replace(' sqft', '')
            price = info_list[7].replace('$', '')
            price = price.replace(' /mo', '')
            price = price.replace(',', '')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)
            b1 = info_list[8].replace(' bed', '')
            b2 = info_list[9].replace(' bath', '')
            size = info_list[10].replace(' sqft', '')
            price = info_list[11].replace('$', '')
            price = price.replace(' /mo', '')
            price = price.replace(',', '')
            size = size.replace(',', '')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)

        elif len(info_list) == 32:
            b1 = info_list[0].replace(' bed', '')
            b2 = info_list[1].replace(' bath', '')
            size = info_list[2].replace(' sqft', '')
            price = info_list[3].replace('$', '')
            price = price.replace(' /mo', '')
            price = price.replace(',', '')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)
            b1 = info_list[4].replace(' bed', '')
            b2 = info_list[5].replace(' bath', '')
            size = info_list[6].replace(' sqft', '')
            price = info_list[7].replace('$', '')
            price = price.replace(' /mo', '')
            price = price.replace(',', '')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)
            b1 = info_list[8].replace(' bed', '')
            b2 = info_list[9].replace(' bath', '')
            size = info_list[10].replace(' sqft', '')
            price = info_list[11].replace('$', '')
            price = price.replace(' /mo', '')
            price = price.replace(',', '')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)
            b1 = info_list[12].replace(' bed', '')
            b2 = info_list[13].replace(' bath', '')
            size = info_list[14].replace(' sqft', '')
            price = info_list[15].replace('$', '')
            price = price.replace(' /mo', '')
            price = price.replace(',', '')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)

        elif len(info_list) == 34:
            info_list.pop(4)
            info_list.pop(20)
            b1 = info_list[0].replace(' bed', '')
            b2 = info_list[1].replace(' bath', '')
            size = info_list[2].replace(' sqft', '')
            price = info_list[3].replace('$', '')
            price = price.replace(' /mo', '')
            price = price.replace(',', '')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)
            b1 = info_list[4].replace(' bed', '')
            b2 = info_list[5].replace(' bath', '')
            size = info_list[6].replace(' sqft', '')
            price = info_list[7].replace('$', '')
            price = price.replace(' /mo', '')
            price = price.replace(',', '')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)
            b1 = info_list[8].replace(' bed', '')
            b2 = info_list[9].replace(' bath', '')
            size = info_list[10].replace(' sqft', '')
            price = info_list[11].replace('$', '')
            price = price.replace(' /mo', '')
            price = price.replace(',', '')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)
            b1 = info_list[12].replace(' bed', '')
            b2 = info_list[13].replace(' bath', '')
            size = info_list[14].replace(' sqft', '')
            price = info_list[15].replace('$', '')
            price = price.replace(' /mo', '')
            price = price.replace(',', '')
            size = size.replace(',', '')
            price_per_sqft = f"{float(float(price) / float(size))}"
            dic = {"Title": title[0], "Website": next_url, "Price": price, "Price per square foot": price_per_sqft,
                   "Type": Type1[0], "Post Time": Time[0], "Location": location[0], "Latitude": latitude[0],
                   "Longitude": longitude[0], "Bedroom": b1, "Bathroom": b2,
                   "Utilities Included": Utilities_Included,
                   "Wi Fi and More": Wi_Fi, "Parking Included": Parking_Included,
                   "Agreement Type": Agreement_Type, "Move In Date": Move_In_Date, "Pet Friendly": Pet_Friendly,
                   "Size(sqft)": size, "Furnished": Furnished, "Appliances": Appliances,
                   "Air Conditioning": Air_conditioning,
                   "Personal Outdoor Space": Outdoor_space, "Smoking Permitted": Smoking}
            count.append(dic)

    except Exception:
        print('Done')
    return count

# Set up parallel processing to improve crawling speed, and convert data to Dataframe format and export to Excel
if __name__ == '__main__':
        url = f'https://www.zumper.com/apartments-for-rent/halifax-ns'
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'}
        try:
            browser = webdriver.Chrome()
            browser.get(url)
            browser.maximize_window()
            js = 'document.documentElement.scrollTop=1000'
            browser.execute_script(js)
            time.sleep(10)
            js = 'document.documentElement.scrollTop=2000'
            browser.execute_script(js)
            time.sleep(10)
            js = 'document.documentElement.scrollTop=3000'
            browser.execute_script(js)
            wait = WebDriverWait(browser, 10)
            next = browser.page_source
        finally:
            browser.close()
            next_tree = etree.HTML(next)

        li_List = next_tree.xpath("//*[@class='css-9ulpxd']/div")[0]
        link = li_List.xpath('//*[@class="chakra-link DetailPageLink css-jdbqfd e1k4it830"]/@href')
        next_url = [f'https://www.zumper.com{g}' for g in link]
        pool = Pool(processes=5)
        results = pool.map(DingDianSpider,next_url)
        pool.close()
        pool.join()
        flattened_results = [item for sublist in results for item in sublist]
        data = pd.DataFrame(flattened_results)
        # data.to_excel('Canada Rental House 2.xlsx', index=False)
        # data.to_excel('Canada Rental House.xlsx', index=False)
        db_config = {
            'host': '123.57.92.58',
            'port': 3306,
            'user': '租房数据',
            'password': 'Kingho325',
            'db': '租房数据',
            'charset': 'utf8'
        }

        try:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()

            # cursor.execute('''TRUNCATE TABLE rental_data_tab_fixed''')

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
