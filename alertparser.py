#modules
import requests
import json
import os
from os.path import exists

#stuff
config_exists = exists("config.json")
if config_exists == False:
  print("Please rename config_example.json to config.json and fill out the URL and email before proceeding.")
  quit()
headers_data = open("config.json")
headers = json.load(headers_data)
url = "https://api.weather.gov/alerts"

#clear console
def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

#check if float
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

#PRINT DETAILS
def parse_info(warning_id):
    #print info
    details = {}
    details["headline"] = parse_json['features'][int(warning_id)]['properties']['headline']
    details["location"] = parse_json['features'][int(warning_id)]['properties']['areaDesc']
    details["description"] = parse_json['features'][int(warning_id)]['properties']['description']
    details["severity"] = parse_json['features'][int(warning_id)]['properties']['severity']
    details["urgency"] = parse_json['features'][int(warning_id)]['properties']['urgency']
    details["instruction"] = parse_json['features'][int(warning_id)]['properties']['instruction']
    print(str(details["headline"]))
    print("AREAS/COUNTIES AFFECTED: " + str(details["location"]))
    print("__DESCRIPTION__\n" + str(details["description"]))
    print("SEVERITY: " + str(details["severity"]))
    print("URGENCY/TIMEFRAME: " + str(details["urgency"]))
    if str(details["instruction"]) != 'None':
        print("__INSTRUCTIONS__\n" + str(details["instruction"]))
    


#what area
debug_mode = False
id_data = open("state_id.json")
id_dict = json.load(id_data)
#state or coords
while True:
    #debug/verbose mode in case something goes wrong - type "d" to enter debug mode
    if debug_mode == True:
        print("----------------")
        print("DEBUG MODE")
        print(headers)
        print("----------------")
    location_option = input("Would you like to search by coordinate or by state? (c/s)\n> ")
    if location_option.lower() == "d":
        if debug_mode == True:
            print("Debug mode is already enabled.")
        if debug_mode == False:
            print("Debug mode is now enabled.")
        debug_mode = True
        continue
    if location_option.lower() != "c" and location_option.lower() != "s" and location_option.lower() != "d":
        print("Invalid input. Please try again.")
        continue
    else:
        break
if location_option.lower() == "s":
    while True:
        state = input("Please enter the name/ID of your state. \nFor a list of IDs and names, please type \"list\".\n> ")
        if state.lower() == "list":
            for key in id_dict:
                print(key + " - " + id_dict[key])
            continue
        if state.lower() != "list":
            for key in id_dict:
                    if id_dict[key] == state.capitalize():
                        #verbose mode
                        if debug_mode == True:
                            print("----------------")
                            print("DEBUG MODE")
                            print("Changed " + state + " to " + key)
                            print("----------------")
                        state = key
                        break
        response_API = requests.get(url + "area=" + state.upper(), headers=headers)
        break
if location_option.lower() == "c":
    while True:
        print("Please enter a latitude and longitude in the US.\nFor example, \"35.1561, -90.0514\"")
        lat = input("Please enter the latitude of your location.\n> ")
        lon = input("Please enter the longitude of your location.\n> ")
        response_API = requests.get(url + 'point=' + lat + ',' + lon, headers=headers)
        if isfloat(lat) == False or isfloat(lon) == False:
            print("One of your coordinates isn't a number. Please try again.")
        else:
            break
#historical or active
while True:
    print("Do you wish to see only active warnings or historical warnings?\nHistoircal warnings contain all alerts from the past 7 days. This list could get very long!\nActive warnings contain only alerts that are currently in effect or are going to go into effect.\n(a/h)")
    active_or_historical = input("> ")
    if active_or_historical.lower() == "h":
        if location_option.lower() == "c":
            response_API = requests.get(url + '?point=' + lat + ',' + lon, headers=headers)
        if location_option.lower() == "s":
            response_API = requests.get(url + '?area=' + state.upper(), headers=headers)
        break
    if active_or_historical.lower() == "a":
        if location_option.lower() == "c":
            response_API = requests.get(url + "/active" + '?point=' + lat + ',' + lon , headers=headers)
        if location_option.lower() == "s":
            response_API = requests.get(url + "/active" + '?area=' + state.upper(), headers=headers)
        break
    if active_or_historical.lower() != "a" and active_or_historical.lower() != "h":
        print("Invalid input. Please try again.")
        continue
#if debug mode is on, print the debug response
if debug_mode == True:
    print("----------------")
    print("DEBUG MODE")
    print("Reponse Code: " + str(response_API.status_code))
    #print url
    if location_option.lower() == "c":
        print(response_API.url)
    if location_option.lower() == "s":
        print(response_API.url)
    print("----------------")
if response_API.status_code != 200:
    print("You got a reponse code other than 200. You either typed something in wrong, or the NWS API is down. If the problem persists, please try again later.")
    quit()
#parse json
data = response_API.text
parse_json = json.loads(data)
parse_id = parse_json['features']
parse_area = parse_json['title']
print(parse_area)

#what alert do you want to see
id_list = len(parse_id)
if id_list == 0:
    print("There are no active alerts in this area.")
    quit()
#print id list
for i in range(id_list):
    choose_headline = parse_json['features'][int(i)]['properties']['headline']
    headline_list = [ ]
    headline_list.append(choose_headline)
    for item in headline_list:
        print(str(i) + " - " + str(item))
        print("Location(s): " + parse_json['features'][int(i)]['properties']['areaDesc'][0:60]  +"...")
id_list = int(id_list) - 1
#ask for id
while True:
    warning_id = input("What ID alert would you like to see?" + " (Please enter an ID from 0-" + str(id_list) + ") \n> ")
    if warning_id.isnumeric() == False:
        print("That's not a number!")
    if int(warning_id) > int(id_list):
        print("That alert does not exist!")
    else:
        break
parse_info(warning_id)
print('\n')
