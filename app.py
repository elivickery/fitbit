import fitbit, json
from datetime import date
from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template
app = Flask(__name__)

today = date.today()
 
@app.route("/")

def chart():
    total_labels = ["Calories In This Week","Calories Out This Week"]
    total_values = [total_calories_in,total_calories_out]
    total_diff = (total_calories_in - total_calories_out)
    today_labels = ["Calories In Today","Calories Out Today"]
    today_values = [calories_in_today,calories_out_today]
    today_diff = (calories_in_today - calories_out_today)
    return render_template('chart.html', total_values=total_values, total_labels=total_labels,today_values=today_values,today_labels=today_labels,total_diff=total_diff,today_diff=today_diff)

def calories_in():

    print "CALORIES CONSUMED"

    total_calories_in = 0

    for calories_in_item in caloriesin['foods-log-caloriesIn']:
        calories_in = calories_in_item['value']
        print "%s - %s" % (calories_in_item['dateTime'],calories_in)
        total_calories_in += int(calories_in)

    return total_calories_in


def calories_out():

    print "CALORIES BURNED"

    total_calories_out = 0

    for calories_out_item in caloriesout['activities-calories']:
        calories_out = calories_out_item['value']
        print "%s - %s" % (calories_out_item['dateTime'],calories_out)
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

calories_out_today = int(caloriesout['activities-calories'][-1]['value'])
calories_in_today = int(caloriesin['foods-log-caloriesIn'][-1]['value'])

total_calories_in = calories_in()
total_calories_out = calories_out()

print '-----------------------'

print "Welcome, %s!" % userprofile['user']['displayName']

print "Today is: %s." % today

print "Calories consumed so far today: %s" % calories_in_today
print "Calories burned so far today: %s" % calories_out_today

print '-----------------------'

print 'Calories consumed this week: %s' % total_calories_in

print '-----------------------'

print 'Calories burned this week: %s' % total_calories_out




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)