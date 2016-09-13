# -*- coding: utf-8 -*-

import logging

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import utility


def word_close_match(word1, word2):
    """Checks if two words are close but not an exact match as
    sometimes there are misspellings or special characters that don't match
    """
    letter_match_count = 0
    if len(word1) == len(word2):
        for idx in range(len(word1)):
            if word1[idx] == word2[idx]:
                letter_match_count += 1
        word_match_score = int((letter_match_count / float(len(word1))) * 100)
        if word_match_score >= 70:
            logging.debug("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            logging.debug(word1.encode('utf-8') + " was close match to "
                + word2.encode('utf-8') + " with score of " 
                + str(word_match_score))
            return True
    return False


def close_match_in_word_list(word_to_check, word_list):
    """Checks if there are any words that are closely matched against a list"""
    for word in word_list:
        if word_close_match(word_to_check, word):
            return True
    return False


def get_restaurant_name_match_score(restaurant1, restaurant2):
    """Checks percentage of words in restaurant1 that are in restaurant2"""
    rest1_words = restaurant1.split()
    rest2_words = restaurant2.split()
    rest1_words_match_count = 0
    for word in rest1_words:
        if word in restaurant2 or close_match_in_word_list(word, rest2_words):
            rest1_words_match_count += 1
    rest1_words_match_score = (
        int((rest1_words_match_count / float(len(rest1_words))) * 100))
    return rest1_words_match_score


def good_restaurant_name_match_score(restaurant1, restaurant2):
    """Checks word match percentage is above 60% between restaurant1
    and restaurant2
    """
    # Check if the words in the first restaurant are mostly a part of 
    # the second restaurant name
    rest1_words_match_score = get_restaurant_name_match_score(restaurant1, 
        restaurant2)
    if rest1_words_match_score >= 60:
        logging.info("Name score matched with score of "
            + str(rest1_words_match_score))
        return True
    # Check if the words in the second restaurant are mostly a part of 
    # the first restaurant name
    rest2_words_match_score = get_restaurant_name_match_score(restaurant2, 
        restaurant1) 
    if rest2_words_match_score >= 60:
        logging.info("Split restaurant2 name score matched with score of " 
            + str(rest2_words_match_score))
        return True
    # If it gets here the names do not match enough to satisfy what 
    # we're looking for
    logging.info("Split restaurant name matching did not pass with scores of " 
        + str(rest1_words_match_score) + " and " 
        + str(rest2_words_match_score))
    return False


def restaurant_name_split_match(restaurant1, restaurant2):
    """Checks for a match between two restaurant names"""
    logging.debug("****************")
    logging.debug("Restaurant 1: " + restaurant1.encode('utf-8'))
    logging.debug("Restaurant 2: " + restaurant2.encode('utf-8'))
    restaurant1 = utility.format_name(restaurant1).lower()
    restaurant2 = utility.format_name(restaurant2).lower()    
    # First do a fast check if one name is a part of the other but one is longer
    # This saves time so the other function doesn't need to be called as much
    if restaurant1 in restaurant2 or restaurant2 in restaurant1:
        logging.debug("Name of one of restaurant part of the other, same place")
        return True
    # If not obvious match, get restaurant name match score and see if it passes
    if good_restaurant_name_match_score(restaurant1, restaurant2):
        return True
    return False


def word_abbreviation_match(word1, word2):
    """Takes a word and checks if it is an abbreviation of another word 
    This is used for addresses
    Order matters in this case so had to write my own function
    """
    word1_index = 0
    word2_index = 0
    while (word1_index < len(word1) and word2_index < len(word2)):
        if word1[word1_index] == word2[word2_index]:
            word1_index += 1
            word2_index += 1
            if word1_index == len(word1):
                return True
        else:
            word2_index += 1
    return False


def abbreviation_match(word1, word2):
    """We don't know which address word will be abbreviation so must 
    check both ways
    """
    if (word_abbreviation_match(word1, word2) 
            or word_abbreviation_match(word2, word1)):
        return True
    return False


def direction_word(word):
    """Some addresses have or lack a direction, so I'm letting it skip 
    this if it doesn't match
    This isn't a good solution for multiple languages
    """
    directions =['N', 'S', 'E', 'W', 'NORTH', 'SOUTH', 'EAST', 'WEST']
    if word.upper() in directions:
        return True
    return False


def address_match(address1, address2):
    """Addresses are formatted differently in the APIs so need to try and 
    match them dynamically 
    Address word order matters in this case so had to write my own function
    """
    logging.debug("Address 1: " + address1.encode('utf-8'))
    logging.debug("Address 2: " + address2.encode('utf-8'))
    address1_words = address1.lower().split(',')[0].split()
    address2_words = address2.lower().split(',')[0].split()
    addr1_index = 0
    addr2_index = 0
    while (addr1_index < len(address1_words) 
            and addr2_index < len(address2_words)):
        if address1_words[addr1_index] == address2_words[addr2_index]:
            addr1_index += 1
            addr2_index += 1
            if addr1_index == len(address1_words) :
                logging.debug("+++++++++++++++++++++++")
                logging.debug("Address match! Same place!?")           
                return True
        elif direction_word(address1_words[addr1_index]):
            addr1_index += 1            
        elif direction_word(address2_words[addr2_index]):
            addr2_index += 1         
        elif abbreviation_match(address1_words[addr1_index], 
                address2_words[addr2_index]):
            # The address suffix has the abbreviation and if matches is the 
            # last thing we care about
            logging.debug("+++++++++++++++++++++++")
            logging.debug("Address match! Same place!?")           
            return True
        else:
            break
    return False


def restaurant_name_fuzzy_match(restaurant1, restaurant2):
    """Checks for a match between two restaurant names
    This is actually slower than my own matching method so not using it for now
    """
    logging.debug("****************")
    logging.debug("Restaurant 1: " + restaurant1.encode('utf-8'))
    logging.debug("Restaurant 2: " + restaurant2.encode('utf-8'))
    restaurant1 = utility.format_name(restaurant1).lower()
    restaurant2 = utility.format_name(restaurant2).lower()    
    # First do a fast check if one name is a part of the other but one is longer
    # This saves time so the other function doesn't need to be called as much
    if restaurant1 in restaurant2 or restaurant2 in restaurant1:
        logging.debug("Name of one of restaurant part of the other, same place")
        return True
    # Use fuzzy wuzzy to see score
    # simple_ratio_score = fuzz.ratio(restaurant1, restaurant2)
    # logging.debug("Simple Ratio: " + str(simple_ratio_score))
    partial_ratio_score = fuzz.partial_ratio(restaurant1, restaurant2)
    logging.debug("Partial Ratio: " + str(partial_ratio_score))
    # token_sort_ratio_score = fuzz.token_sort_ratio(restaurant1, restaurant2)
    # logging.debug("Token Sort Ratio: " + str(token_sort_ratio_score))
    token_set_ratio_score = fuzz.token_set_ratio(restaurant1, restaurant2)
    logging.debug("Token Set Ratio: " + str(token_set_ratio_score))
    # fuzzy_average_4 = ((float(simple_ratio_score) + partial_ratio_score 
    #             + token_sort_ratio_score + token_set_ratio_score) / 4)
    # logging.debug("Fuzzy Average 4: " + str(fuzzy_average_4))
    fuzzy_average_2 = ((float(partial_ratio_score)  
                    + token_set_ratio_score) / 2)
    logging.debug("Fuzzy Average 2: " + str(fuzzy_average_2))
    fuzzy_max_2 = max(partial_ratio_score, token_set_ratio_score)
    # fuzzy_max_4 = max(simple_ratio_score, partial_ratio_score, 
    #             token_sort_ratio_score, token_set_ratio_score)    
    logging.debug("Fuzzy Max: " + str(fuzzy_max_2))
    if (fuzzy_max_2 >= 80
            or (fuzzy_max_2 > 70 and fuzzy_average_2 > 70)):
        return True
    return False

