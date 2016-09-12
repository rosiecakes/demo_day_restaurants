import logging
import time

from flask import render_template, redirect, request, flash, url_for, Markup
from geopy.geocoders import Nominatim

from restaurate import app
from utility import *
from database import *
from api_data import get_restaurant_data_from_apis

# from library.config import LOGLEVEL   
# import markdown


@app.route('/', methods=['POST', 'GET'])
def index():
    """Displays index page for web application
    POST redirects to show_restaurants function and renders table
    GET loads basic layout page for input
    """
    if request.method == 'POST':
        # Get location name from form
        location = utility.format_name(request.form['location'])
        return redirect(url_for('show_restaurants', location_name=location))
    return render_template('layout.html')


@app.route('/places/<location_name>', methods=['POST', 'GET'])
def show_restaurants(location_name):
    """Displays restaurant information table for web application
    POST redirects back to this function to show table for new inputted 
        restaurant
    GET shows table for restaurant passed in URL
    """
    if request.method == 'POST':
        # Get location name from form
        location = utility.format_name(request.form['location'])
        return redirect(url_for('show_restaurants', location_name=location))
    else:
        # Set up timer to time everything
        start = time.time()
        # Parse location to remove non-alphanumeric characters
        location = utility.format_name(location_name)
        # Use geopy to get coordinates for location and address
        geolocator = Nominatim()
        place = geolocator.geocode(location)
        coordinates = (place.latitude, place.longitude)
        rest_dict = {}

        # Set up logging file for specific location
        file='logs\{}.txt'.format(location.title())
        log = logging.getLogger()  # root logger
        for hdlr in log.handlers[:]:  # remove all old handlers
            log.removeHandler(hdlr)
        logging.basicConfig(filename=file, filemode="w", level=logging.DEBUG, 
            format='%(asctime)s - %(levelname)s - %(message)s')

        # Check if we can get data from database 
        # or if we need new data from APIs
        if (check_table_exists(location) 
                and time_stamp_exists(location) 
                and check_time_stamp(location)):
            # If table exists, time stamp exists, and time stamp is up to date
            # read from table
            get_table(location, rest_dict)
        else:
            # If table exists but time stamp does not exist (incomplete)
            # or is older than 30 days, delete the table
            if (check_table_exists(location) 
                    and (not time_stamp_exists(location) 
                            or not check_time_stamp(location))):
                delete_table(location)

            # Get data from APIs and create new table
            get_restaurant_data_from_apis(location, coordinates, 
                rest_dict)
            remove_duplicate_restaurants(rest_dict)
            calculate_statistics(rest_dict)
            create_table(location, rest_dict)
        # Calculate time of search
        end = time.time()
        elapsed = end - start
        elapsed = "%.2f" % elapsed
        return render_template('table.html', 
                                location=place.address, 
                                elapsed_time=elapsed, 
                                rest_dict=rest_dict)


# @app.route('/about')
# def show_about():
#     with open('README.md') as f:
#         readme = Markup(markdown.markdown(f.read()))
#     return render_template('about.html', readme=readme)