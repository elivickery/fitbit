import fitbit, json

from datetime import date
today = date.today()


def calories_in():

    print "CALORIES CONSUMED"

    total_calories_in = 0

    for calories_in_item in caloriesin['foods-log-caloriesIn']:
        calories_in = calories_in_item['value']
        print "%s - %s" % (calories_in_item['dateTime'],calories_in_item['value'])
        total_calories_in += int(calories_in)

    return total_calories_in


def calories_out():

    print "CALORIES BURNED"

    total_calories_out = 0

    for calories_out_item in caloriesout['activities-calories']:
        calories_out = calories_out_item['value']
        print "%s - %s" % (calories_out_item['dateTime'],calories_out_item['value'])
        total_calories_out += int(calories_out)

    return total_calories_out


tokenfile = "user_settings.txt"

fitbitclass = fitbit.Fitbit();

try:
    token = json.load(open(tokenfile))
except IOError:
    auth_url = fitbitclass.GetAuthorizationUri()

    print "Please visit the link below and approve the app:\n %s" % auth_url

    access_code = raw_input("Enter code from the URL: ")

    token = fitbitclass.GetAccessToken(access_code)

    json.dump(token, open(tokenfile,'w'))

# Get user profile info, calories in and calories out data from the past week
userprofile = fitbitclass.ApiCall(token, '/1/user/-/profile.json')
caloriesout = fitbitclass.ApiCall(token, '/1/user/-/activities/calories/date/today/1w.json')
caloriesin = fitbitclass.ApiCall(token, '/1/user/-/foods/log/caloriesIn/date/today/1w.json')

# Replace the current token with the response one and save it in user_settings.txt.
token = userprofile['token']
json.dump(token, open(tokenfile,'w'))

calories_out_today = caloriesout['activities-calories'][-1]['value']
calories_in_today = caloriesin['foods-log-caloriesIn'][-1]['value']


print '-----------------------'

print "Welcome, %s!" % userprofile['user']['displayName']

print "Today is: %s." % today

print "Calories consumed so far today: %s" % calories_in_today
print "Calories burned so far today: %s" % calories_out_today

print '-----------------------'

print 'Calories consumed this week: %s' % calories_in()

print '-----------------------'

print 'Calories burned this week: %s' % calories_out()

