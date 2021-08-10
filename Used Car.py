import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}
data = open('used_car.html', 'r')
souped = BeautifulSoup(data, 'lxml')

tags = souped.find_all(class_='gsc_col-md-4 gsc_col-sm-6 gsc_col-xs-12')

used_car_name = []
used_car_url = []

for tag in tags:
    name = tag.find(href=True)['title']
    url = tag.find(href=True)['href']

    if url not in used_car_url:
        used_car_name.append(name)
        used_car_url.append(url)

# print(len(used_car_name))

# print(used_car_url)


# -------------------------------------------------------------------------#

missing_values = []
cardekho = 'https://www.cardekho.com'


selling_prices = []
current_values = []
year = []
seller = []
kms = []
owner = []
fuel = []
transmission = []
mileage = []
engine = []
max_power = []
seating_capacity = []
gear_box = []
driver = []

for i in range(len(used_car_url)):
    url = cardekho + used_car_url[i]
    page = requests.get(url, headers=headers)
    souped = BeautifulSoup(page.content, "lxml")

    tags = souped.find_all(class_='gsc_col-xs-6')

    selling_prices.append(souped.find(class_='pricewrapper posR').span.text)

    try:
        curr_val = souped.find(class_='bold').text
        nonBreakSpace = u'\xa0'
        curr_val = curr_val.replace(nonBreakSpace, ' ')

        current_values.append(curr_val)
    except:
        current_values.append(None)
        missing_values.append(used_car_url[i])

    year.append(tags[0].text)
    seller.append(tags[1].text)
    kms.append(tags[2].text)
    owner.append(tags[3].text)
    fuel.append(tags[4].text)
    transmission.append(tags[5].text)

    small = souped.find_all(class_='smallSpec')
    large = souped.find_all(class_='largeSpec')

    specs = {}
    for num, m in enumerate(small):
        specs[m.text] = large[num].text

    if 'Mileage' not in specs.keys():
        mileage.append(None)
    else:
        mileage.append(specs['Mileage'])

    if 'Engine' not in specs.keys():
        engine.append(None)
    else:
        engine.append(specs['Engine'])

    if 'Seats' not in specs.keys():
        seating_capacity.append(None)
    else:
        seating_capacity.append(specs['Seats'])

    if 'Gear Box' not in specs.keys():
        gear_box.append(None)
    else:
        gear_box.append(specs['Gear Box'])

    if 'Drive Type' not in specs.keys():
        driver.append(None)
    else:
        driver.append(specs['Drive Type'])

    if 'Max Power' not in specs.keys():
        max_power.append(None)
    else:
        max_power.append(specs['Max Power'])

# print(missing_values)

df_dict = {'Car Name': used_car_name, 'Car url': used_car_url, 'Year': year, 'Selling Price': selling_prices,
           'Current Value': current_values, 'KMs Driven': kms, 'Fuel': fuel, 'Seller Type': seller, 'max_power':max_power,
           'Transmission': transmission, 'Owner': owner, 'Mileage': mileage, 'Engine': engine, 'Drive Type': driver,
           'Seats': seating_capacity, 'Gear Box': gear_box}

df = pd.DataFrame(df_dict)
df.to_csv('Cardekho-Used-Car-Data.csv')
