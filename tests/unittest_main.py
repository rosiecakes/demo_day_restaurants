# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../restaurate')
from name_match import *
import unittest 
import logging

logging.basicConfig(filename='../logs/unittest.txt', level=logging.DEBUG, 
    filemode="w", format='%(asctime)s - %(levelname)s - %(message)s')

class NameMatchTestCase(unittest.TestCase):
    
    def test_restaurant_name_match1(self):
        restaurant1 = "Snuffer's"
        restaurant2 = "Snuffer's Restaurant & Bar"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))
   
    # def test_restaurant_name_match2(self):
    #     # We filter this with by checking address now
    #     restaurant1 = "Fogo de Chão Brazilian Steakhouse".decode("utf-8")
    #     restaurant2 = "Texas de Brazil"
    #     self.assertFalse(restaurant_name_split_match(restaurant1, restaurant2))

    def test_restaurant_name_match3(self):
        restaurant1 = "De Rice"
        restaurant2 = "Derice Thai Cuisine"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))
        
    def test_restaurant_name_match4(self):
        restaurant1 = "Yard House"
        restaurant2 = "Saffron House"
        self.assertFalse(restaurant_name_split_match(restaurant1, restaurant2))
        
    def test_restaurant_name_match5(self):
        restaurant1 = "Salata Addison"
        restaurant2 = "Addison Point"
        self.assertFalse(restaurant_name_split_match(restaurant1, restaurant2))
        
    def test_restaurant_name_match6(self):
        restaurant1 = "Fred's Philly Cheesesteaks"
        restaurant2 = "Fred's Downtown Philly"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))
        
    def test_restaurant_name_match7(self):
        restaurant1 = "Fillmore Pub"
        restaurant2 = "The Fillmore Pub"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))    

    def test_restaurant_name_match8(self):
        restaurant1 = "Zenna Thai & Japanese Restaurant"
        restaurant2 = "Zenna"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))   

    def test_restaurant_name_match9(self):
        restaurant1 = "BJ's Restaurant & Brewhouse"
        restaurant2 = "BJ's Restaurant and Brewhouse"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))

    def test_restaurant_name_match10(self):
        restaurant1 = "The Flying Saucer"
        restaurant2 = "Flying Saucer Draught Emporium"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))

    def test_restaurant_name_match11(self):
        restaurant1 = "Addis Ababa"
        restaurant2 = "ADDIS ABEBA ETHIOPIAN RESTAURANT"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))

    def test_restaurant_name_match12(self):
        restaurant1 = "Little Greek Restaurant"
        restaurant2 = "Little Greek Fresh Grill"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))

    def test_restaurant_name_match13(self):
        restaurant1 = "Mena's Grill Tex-Mex Cantina"
        restaurant2 = "Mena's Tex-Mex Grill"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))

    def test_restaurant_name_match14(self):
        restaurant1 = "Amigos Restaurant Comida Casera"
        restaurant2 = "Amigos Restaurant"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))
        
    def test_restaurant_name_match15(self):
        restaurant1 = "Mooyah"
        restaurant2 = "MOOYAH Burgers, Fries & Shakes"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))
        
    def test_restaurant_name_match16(self):
        restaurant1 = "Thai Box"
        restaurant2 = "ThaiBOX"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))   

    def test_restaurant_name_match17(self):
        restaurant1 = "Big Ray's BBQ"
        restaurant2 = "Big Rays Bar B Que"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))   

    def test_restaurant_name_match18(self):
        restaurant1 = "Baker's Drive In"
        restaurant2 = "BAKERS DRIVE IN"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))  

    def test_restaurant_name_match19(self):
        restaurant1 = "A&D Buffalo's"
        restaurant2 = "A & D Buffalos"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))        

    def test_restaurant_name_match20(self):
        restaurant1 = "Eclair Bistro"
        restaurant2 = "Gregory's Bistro"
        self.assertFalse(restaurant_name_split_match(restaurant1, restaurant2))  
              
    # def test_restaurant_name_match21(self):
    #     # This can pass if I can fit 80% of letters into the other for each word
    #     # However removing this isnt as bad as a false positive match
    #     # Less data is better than wrong data
    #     # I think this adds too much extra code for one specific case so leaving it out
    #     restaurant1 = "Luigi's Pasta & Pizzeria Restaurant"
    #     restaurant2 = "Luigi's Pizza"
    #     self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))    

    def test_restaurant_name_match22(self):
        restaurant1 = "Genghis Grill - The Mongolian Stir Fry"
        restaurant2 = "Genghis Grill - Build Your Own Stir Fry"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))  
              
    def test_restaurant_name_match23(self):
        restaurant1 = "Joe's NY Style Pizza & Pasta"
        restaurant2 = "Joe's Pizza & Pasta"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))            

    def test_restaurant_name_match24(self):
        restaurant1 = "Wes' Burger Shack"
        restaurant2 = "Wes's Burger Shack & More"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))  

    def test_restaurant_name_match25(self):
        restaurant1 = "Addison Cafe"
        restaurant2 = "Dream Cafe"
        self.assertFalse(restaurant_name_split_match(restaurant1, restaurant2))        

    def test_restaurant_name_match26(self):
        restaurant1 = "Cotton Café".decode("utf-8")
        restaurant2 = "Cotton Cafe"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))  
              
    def test_restaurant_name_match27(self):
        restaurant1 = "Nate'n Al Delicatessen"
        restaurant2 = "Nate 'n Al"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))  

    def test_restaurant_name_match28(self):
        restaurant1 = "Kogi Korean BBQ"
        restaurant2 = "Kogi BBQ Food Truck"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))         

    def test_restaurant_name_match29(self):
        restaurant1 = "The Point Restaurant & Reception Center"
        restaurant2 = "The Point Bistro"
        self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))  

     # def test_restaurant_name_match28(self):
     #    restaurant1 = "Cafe Amici Beverly Hills"
     #    restaurant2 = "Tratoria Amici"
     #    self.assertTrue(restaurant_name_split_match(restaurant1, restaurant2))  



class AbbreviationMatchTestCase(unittest.TestCase):

    def test_abbreviation_match1(self):
        self.assertTrue(abbreviation_match('road', 'rd'))  

    def test_abbreviation_match2(self):
        self.assertTrue(abbreviation_match('rd', 'road'))  

    def test_abbreviation_match3(self):
        self.assertTrue(abbreviation_match('street', 'st'))  

    def test_abbreviation_match4(self):
        self.assertTrue(abbreviation_match('Expy', 'Expressway'))  

    def test_abbreviation_match5(self):
        self.assertTrue(abbreviation_match('Pkwy', 'Parkway'))  

    def test_abbreviation_match6(self):
        self.assertTrue(abbreviation_match('Blvd', 'Boulevard'))  

    def test_abbreviation_match7(self):
        self.assertFalse(abbreviation_match('Expy', 'Expresswa'))  

    def test_abbreviation_match8(self):
        self.assertFalse(abbreviation_match('Epxy', 'Expressway'))  


class AddressMatchTestCase(unittest.TestCase):

    def test_address_match1(self):
        address1 = "14920 Midway Rd, Addison, TX 75001, United States"
        address2 = "14920 Midway Road, Addison, TX 75001"
        self.assertTrue(address_match(address1, address2))  

    def test_address_match2(self):
        address1 = "14833 Midway Rd #100, Addison, TX 75001, United States"
        address2 = "14833 Midway Road, Unit 100, Addison, TX 75001"
        self.assertTrue(address_match(address1, address2))  

    def test_address_match3(self):
        address1 = "4152 W Spring Creek Pkwy, Plano, TX 75093, United States"
        address2 = "4152 West Spring Creek Pkwy, Unit 176, Plano, TX 75024"
        self.assertTrue(address_match(address1, address2))  

    def test_address_match4(self):
        address1 = "1004 E 15th St, Plano, TX 75074, United States"
        address2 = "1004 E 15th Street, TX 75074"
        self.assertTrue(address_match(address1, address2))  

    def test_address_match5(self):
        address1 = "2103 N Central Expy, Richardson, TX 75080, United States"
        address2 = "2103 N Central Expressway, Richardson, TX 75080"
        self.assertTrue(address_match(address1, address2))  

    def test_address_match6(self):
        address1 = "2701 Custer Pkwy, Richardson, TX 75080, United States"
        address2 = "2701 Custer Parkway, Suite 807, Richardson, TX 75080"
        self.assertTrue(address_match(address1, address2))  

    def test_address_match7(self):
        address1 = "1403 E Campbell Rd #110, Richardson, TX 75081, United States"
        address2 = "1403 E Campbell Road, Suite 110, Richardson, TX 75081"
        self.assertTrue(address_match(address1, address2))  

    def test_address_match8(self):
        address1 = "2150 N Collins Blvd, Richardson, TX 75080, United States"
        address2 = "2150 N Collins Boulevard, Richardson, TX 75080"
        self.assertTrue(address_match(address1, address2))  

    def test_address_match9(self):
        address1 = "101 Coit Rd #401, Richardson, TX 75080, United States"
        address2 = "101 S Coit Road, Suite 401, Richardson, TX 75080"
        self.assertTrue(address_match(address1, address2))  

    # def test_address_match10(self):
    #     # This match is good but google and zomato dont match
    #     # This will be caught with restaurant name
    #     address1 = "600 N Coit Rd #2050, Richardson, TX 75080, United States"
    #     address2 = "400 N Coit Road, Unit 2050, Richardson, TX 75080"
    #     self.assertTrue(address_match(address1, address2))  

    def test_address_match11(self):
        address1 = "730 E Campbell Rd Suite 330, Richardson, TX 75081, United States"
        address2 = "730 E Campbell Road, Suite 330, Richardson, TX 75081"
        self.assertTrue(address_match(address1, address2))  

    # def test_address_match12(self):
    #     address1 = "5100 Belt Line Rd #230, Addison, TX 75254, United States"
    #     address2 = "5100 Belt Line Road, Suite 728, Dallas, TX 75254"
    #     self.assertFalse(address_match(address1, address2))  




if __name__ == "__main__":
    unittest.main()