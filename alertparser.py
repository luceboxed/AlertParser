#modules
import requests
import json
import os

headers = {
    'User-Agent': 'https://github.com/spikeyscout/AlertParser, scout@spikeyscout.xyz',
}
url = "https://api.weather.gov/alerts/active?"

#clear console
def clearConsole():

    if os.name in ('nt', 'dos'):
        clearcommand = 'cls'
    else:
        clearcommand = 'clear'
    os.system(clearcommand)

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
id_data = open("state_id.json")
id_dict = json.load(id_data)
while True:
    location_option = input("Would you like to search by coordinate or by state? (c/s)\n> ")
    if location_option.lower() != "c" and location_option.lower() != "s":
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
                        state = key
                        break
        response_API = requests.get(url + "area=" + state.upper(), headers=headers)
        break
if location_option.lower() == "c":
    while True:
        lat = input("Please enter the latitude of your location.\n> ")
        lon = input("Please enter the longitude of your location.\n> ")
        response_API = requests.get(url + 'point=' + lat + ',' + lon, headers=headers)
        if isfloat(lat) == False or isfloat(lon) == False:
            print("One of your coordinates isn't a number. Please try again.")
        else:
            break
print("Reponse Code: " + str(response_API.status_code))
if response_API.status_code != 200:
    print("You got a reponse code other than 200. You either typed something in wrong, or the NWS API is down.")
    quit()
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
for i in range(id_list):
    choose_headline = parse_json['features'][int(i)]['properties']['headline']
    headline_list = [ ]
    headline_list.append(choose_headline)
    for item in headline_list:
        print(str(i) + " - " + str(item))
id_list = int(id_list) - 1
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
