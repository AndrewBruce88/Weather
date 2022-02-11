''' This script written by AN on 2022-02-09 and 2022-02-10, fetches Vancouver weather
    data from weather.gc.ca and displays it nicely for the user. For some aspects I 
    took the advice of a tutorial which was scraping from google weather. The purpose
    of this exercise was to work on web scraping.
    In the future it would be great to add an argument that will allow the user to 
    input a city or check their own IP address to determine more localized weather.
    Pylint score of 8.61 / 10
    '''

from bs4 import BeautifulSoup as bs
import requests

# use this user agent to make the request as a web browser to avoid scraping issues
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36"
# check this website for latest user-agent version:
# https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome
LANGUAGE = "en-US,en;q=0.5"

USE_LOCAL_DATA = False
STORE_DATA = True

def make_request(our_url):
    ''' Function that makes the request from the URL and gets the html of the page
        This function uses USER_AGENT and LANGUAGE headers to act as a browser making the request
    '''
    my_session = requests.Session()
    my_session.headers["User-Agent"] = USER_AGENT
    my_session.headers["Accept-Language"] = LANGUAGE
    my_session.headers["Content-Language"] = LANGUAGE
    # make request:
    full_html = my_session.get(our_url)
    print("========== Got full html ==========")

    # normally will return full_html; for now will save html as a text file
    return full_html.text

def parse_data(html_text):
    ''' Function that parses html text using beautiful soup and finds all desired weather info '''
    my_soup = bs(html_text,"lxml")
    data_dict = {}
    
    for item in my_soup.find_all("dl",attrs={"class":"dl-horizontal wxo-conds-xs"}):
        if item.dt is not None:
            if item.dt.text == "Temperature:":
                data_dict['current_temp'] = item.dt.parent.dd.text.strip()
            if item.dt.text == "Wind:":
                data_dict['current_wind'] = item.dt.parent.dd.text.strip()
            if item.dt.text == "Pressure:":
                data_dict['current_pressure'] = item.dt.parent.dd.text.strip()
            if item.dt.text == "Dew point:":
                data_dict['current_dewpoint'] = item.dt.parent.dd.text.strip()
            if item.dt.text == "Visibility:":
                data_dict['current_visibility'] = item.dt.parent.dd.text.strip()
            if item.dt.text == "Humidity:":
                data_dict['current_humidity'] = item.dt.parent.dd.text.strip()
        
    # find current condition
    item = my_soup.find("dl",attrs={"class":"dl-horizontal wxo-conds-col1"})
    for tag in item.find_all():
        if tag.text == "Condition:":
            data_dict['current_conditions'] = tag.findNext('dd').text.strip()

    # find observation location & datetime
    for item in my_soup.find_all("dl",attrs={"class":"dl-horizontal mrgn-bttm-0 hidden-xs wxo-conds-tmp mrgn-tp-sm"}):
        for tag in item.find_all():
            if tag.text.strip() == "Observed at:":
                data_dict['observation_location'] = tag.findNext('dd').text.strip()
            if tag.text.strip() == "Date:":
                data_dict['latest_datetime'] = tag.findNext('dd').text.strip()

    # find next day forecasts
    upcoming_data = []
    for column in my_soup.find_all("div",attrs={"class":"div-column"}):
        daily_dict = {}
        try:
            daily_dict['date'] = column.find("div",attrs={"class":"div-row div-row1 div-row-head"}).text.strip()
        except AttributeError:
            pass
        
        for tag in column.find_all("span"):
            
            if tag['title'] == "max" and "wxo-metric-hide" in tag['class']:
                # high
                daily_dict['high'] = tag.text.strip()

                for p_tag in tag.parent.find_next_siblings("p"):
                    # conditions
                    if p_tag['class'] == ['mrgn-bttm-0']:
                        daily_dict['day_conditions'] = p_tag.text.strip()
                    # chance of precip
                    if p_tag['class'] == ['mrgn-bttm-0','pop','text-center']:
                        daily_dict['day_cop'] = p_tag.text.strip()

            if tag['title'] == "min" and "wxo-metric-hide" in tag['class']:
                # low
                daily_dict['low'] = tag.text.strip()

                for p_tag in tag.parent.find_next_siblings("p"):
                    # conditions
                    if p_tag['class'] == ['mrgn-bttm-0']:
                        daily_dict['night_conditions'] = p_tag.text.strip()
                    # chance of precip
                    if p_tag['class'] == ['mrgn-bttm-0','pop','text-center']:
                        daily_dict['night_cop'] = p_tag.text.strip()
        
        upcoming_data.append(daily_dict)

    data_dict['upcoming_days'] = upcoming_data

    return data_dict

def display_data(data):
    ''' Function that displays our dictionary of data, including the next-X day data '''
    print("="*10 , f"Weather report for {data['observation_location']}" , "="*10)
    print(f"Date and time: {data['latest_datetime']}")
    print()
    print(f"Current temperature: {data['current_temp']}")
    print(f"Current conditions: {data['current_conditions']}")
    print(f"Wind: {data['current_wind']}")
    print(f"Pressure: {data['current_pressure']}")
    print(f"Dew point: {data['current_dewpoint']}")
    print(f"Humidity: {data['current_humidity']}")
    print()
    for day in data['upcoming_days']:
        try:
            date = day['date'][0:3] + ' ' + day['date'][3:]
            print("="*10, f"Weather for {date}: ", "="*10)
            print(f"Daytime high: {day['high']}")
            print(f"Daytime conditions: {day['day_conditions']}")
            if day['day_cop'] == '':
                if day['day_conditions'] == "Rain":
                    day_cop = "100%"
                else:
                    day_cop = "0%"
            else:
                day_cop = day['day_cop']
            print(f"Chance of precip: {day_cop}")
        except KeyError:
            pass

        try:
            print(f"Nighttime low: {day['low']}")
            print(f"Nighttime conditions: {day['night_conditions']}")
            if day['night_cop'] == '':
                if day['night_conditions'] == "Rain":
                    night_cop = "100%"
                else:
                    night_cop = "0%"
            else:
                night_cop = day['night_cop']
            print(f"Chance of precip: {night_cop}")
        except KeyError:
            pass
        print()

def store_html(html_text,name="my_html.txt"):
    ''' Function that stores html_text information into .txt file locally '''
    f = open(name,"w",encoding="UTF-8")
    f.write(html_text)
    f.close()

def get_local_data(name):
    ''' Function that retrieves html_text information from local .txt file '''
    f = open(name,"r",encoding="UTF-8")
    data = f.read()
    f.close()
    return data

def main():
    ''' Main function: uses functions to acquire data, parse it, and display it '''

    # for now, only search Vancouver weather. Later can make lookup dictionary and use arg
    URL = "https://weather.gc.ca/city/pages/bc-74_metric_e.html"
    # file where we will store data if we want to
    local_filename = "my_html_file.txt"

    # If want to scrape, keep "USE_LOCAL_DATA" as False. This makes the request
    # and stores that data in a local text file
    if not USE_LOCAL_DATA:
        print("Acquiring data from URL...")
        my_data = make_request(URL)
        if STORE_DATA:  store_html(my_data,local_filename)


    # If want to play around and troubleshoot locally, make "USE_LOCAL_DATA" True.
    # This loads data from the local text file
    if USE_LOCAL_DATA:
        print(f"Acquiring data from local {local_filename}...")
        my_data = get_local_data(local_filename) 

    print("About to parse data....")
    parsed_data = parse_data(my_data)

    # output data from weather_dict
    display_data(parsed_data)

if __name__ == "__main__":
    main()

