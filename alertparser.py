#modules
import requests
import json
import os


#clear console
def clearConsole():

    if os.name in ('nt', 'dos'):
        clearcommand = 'cls'
    else:
        clearcommand = 'clear'
    os.system(clearcommand)

clearConsole()

#what area
state = input("Please enter your two letter state/territory ID in ALL CAPITALS. \n>")
response_API = requests.get('https://api.weather.gov/alerts/active?area=' + state)
print("Reponse Code: " + str(response_API.status_code))
if response_API.status_code != 200:
    print("You got a reponse code other than 200. You either typed in your code wrong/in lowercase, or the NWS API is down.")
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
warning_id = input("What ID alert would you like to see?" + " (Please enter an ID from 0-" + str(id_list) + ") \n>")

if int(warning_id) > int(id_list):
    print("That alert does not exist!")
    quit()


#PRINT DETAILS
def parse_info():
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




clearConsole()
parse_info()
print('\n')
