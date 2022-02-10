# Weather
A python script that scrapes the internet to create a weather report

This is my final project to complete the intro to python course from Udemy, https://www.udemy.com/share/101W8Q/

I wanted to do some web scraping work for practice. The script fetches Vancouver weather data from weather.gc.ca and displays it nicely for the user. For some aspects I took the advice of a tutorial which was scraping from google weather. The html on weather.gc.ca was quite different from google weather, so there was a lot of different techniques needed using Beautiful Soup 4 to get to the final state.

Not my most useful project, but fun to work on. I have some thoughts for expansion later on, or if anyone wants to collaborate with a pull request hit it up!

weather.gc.ca has a numerical index for each city for which weather is available. For example, Vancouver's weather (in metric and english) is https://weather.gc.ca/city/pages/bc-74_metric_e.html, #bc-74, and Lethbridge is https://weather.gc.ca/city/pages/ab-30_metric_e.html, #ab-30. It would be great to have a dictionary that maps city names to keys, and then have the city name be an argument for the function on the command line using argparse.

Another nice feature to add will be to have the script detect the user's external IP address and then determine the closest matching city entry. This could be an option specified by entering -1 as the cityname argument.
