# -*- coding: utf-8 -*-

import logging
import itertools
import collections
import time
import name_match

def format_name(name):
    """Remove non alphanumeric/whitespace characers from user input or restaurant data"""
    return ''.join( chr for chr in name if chr.isalnum() or chr.isspace())


def format_address(address):
    """Remove non alphanumeric/whitespace characers from restaurant address but allows for commas"""
    return ''.join( chr for chr in address if chr.isalnum() or chr.isspace()) or chr == ","


def scrub_tablename(tablename):
    """Removes whitespace characters from location so can save table name, 
    adds _ before name if all numbers
    """
    table = ''.join( chr for chr in tablename if chr.isalnum() )
    if table[0].isdigit():
        table = "_" + table
    return table.upper()


def get_potential_duplicates(restaurant_dict):
    """We want to check for duplicates in the restaurant dictionary.
    Review count is usually unique so we want to check for matching 
    review count numbers and then compare them for any name matches
    """

    # Create a temporary dictionary of just restaurant names and review count as value
    # because that is all we care about here
    temp_dict = {}
    for restaurant in restaurant_dict:
        temp_dict[restaurant] = restaurant_dict[restaurant]['zomato_review_count']

    # Count occurrences of each review count 
    review_count_occurrences = collections.Counter(temp_dict.values())

    # Get a list of the occurrences that happen more than once
    potential_duplicates = list(set([value for key, value in temp_dict.items()
                            if review_count_occurrences[value] > 1]))

    # Pull out lists of the restaurant names that have matching review counts 
    # in separate lists for each so they only check against same review count
    restaurants_to_check = [[key for key, value in temp_dict.items() if value == num] 
                             for num in potential_duplicates]    
    return restaurants_to_check


def check_duplicate_restaurant(restaurant_dict, restaurant1, restaurant2):
    """Checks to see if two restaurants are duplicates """
    # I can tweak this to use address matching as well
    if restaurant_dict[restaurant1]['google_rating'] == restaurant_dict[restaurant2]['google_rating'] \
    and restaurant_dict[restaurant1]['zomato_rating'] == restaurant_dict[restaurant2]['zomato_rating'] \
    and name_match.restaurant_name_split_match(restaurant1, restaurant2):
        logging.debug("Duplicate restaurants found: " + restaurant1.encode('utf-8') \
            + " and " + restaurant2.encode('utf-8'))
        return True
    logging.debug("Potential duplicate restaurants that failed test: " + restaurant1.encode('utf-8')  \
        + " and " + restaurant2.encode('utf-8'))
    return False


def find_duplicate_restaurants(restaurant_dict):
    """Checks all combinations of potential duplicates and adds
    duplicates to a list as a pair
    """
    logging.debug("Checking for potential duplicate restaurants...")
    duplicate_pairs = []
    restaurants_to_check = get_potential_duplicates(restaurant_dict)
    for potential_duplicates_list in restaurants_to_check:
        # Check all combinations of restaurants that have matching review counts
        for rest1, rest2 in itertools.combinations(potential_duplicates_list, 2):
            if check_duplicate_restaurant(restaurant_dict, rest1, rest2):
                duplicate_pairs.append([rest1, rest2])
    return duplicate_pairs


def remove_duplicate_restaurants(restaurant_dict):
    """Removes duplicate restaurants from restaurant dict"""
    duplicate_pairs = find_duplicate_restaurants(restaurant_dict)
    for duplicate_pair in duplicate_pairs:
        logging.debug("Removing duplicate restaurant: " + duplicate_pair[0].encode('utf-8'))
        restaurant_dict.pop(duplicate_pair[0], None)                       


def calculate_statistics(restaurant_dict):
    """Calculates average rating and Restaurate ranking for each restaurant"""
    # Calcu
    for restaurant in restaurant_dict.keys():
        if 'zomato_rating' in restaurant_dict[restaurant].keys() and 'google_rating' in restaurant_dict[restaurant].keys():
            restaurant_dict[restaurant]['average_rating'] = (float(restaurant_dict[restaurant]['google_rating']) + float(restaurant_dict[restaurant]['zomato_rating'])) / 2
            restaurant_dict[restaurant]['total_reviews'] = int(restaurant_dict[restaurant]['zomato_review_count'])
        else:
            logging.error("This place got to calculate_statistics without all its rating data: ", restaurant)
            logging.error(restaurant_dict[restaurant])
            break
    sorted_rating = sorted(restaurant_dict, key=lambda x: (restaurant_dict[x]['average_rating']), reverse=True)
    sorted_popularity = sorted(restaurant_dict, key=lambda x: (restaurant_dict[x]['total_reviews']), reverse=True)
    #
    for restaurant in restaurant_dict:
        restaurant_dict[restaurant]['rating_rank'] = sorted_rating.index(restaurant) + 1
        restaurant_dict[restaurant]['popularity_rank'] = sorted_popularity.index(restaurant) + 1
        restaurant_dict[restaurant]['combined_score'] = float(restaurant_dict[restaurant]['popularity_rank']) * 0.3 + float(restaurant_dict[restaurant]['rating_rank']) * 0.7
    # 
    sorted_score = sorted(restaurant_dict, key=lambda x: (restaurant_dict[x]['combined_score']))
    for restaurant in restaurant_dict:
        restaurant_dict[restaurant]['restaurate_rank'] = sorted_score.index(restaurant) + 1


def elasped_time(original_function):
    """Times functions for debug purposes """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = original_function(*args, **kwargs)
        end = time.time()
        elapsed = end - start
        logging.debug(original_function.__name__ + " took " + str(elapsed) + " seconds.")     
        return result   
    return wrapper
