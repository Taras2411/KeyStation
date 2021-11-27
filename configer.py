import configparser
config = configparser.ConfigParser()
config.read('config.ini')
dictionary = {}
for section in config.sections():
    dictionary[section] = {}
    for option in config.options(section):
        dictionary[section][option] = config.get(section, option)

print(dictionary['OTHER']['biperpin'])

testDict = dictionary['ROOMS_TO_PINS']
for i in testDict:   
    testDict[i] = int(testDict[i])
print(testDict)

testDict2 = dictionary['ROOMS_TO_LEDS']
for i in testDict2:   
    testDict2[i] = int(testDict2[i])
print(testDict2)