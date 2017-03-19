import fitbit, json, time
from datetime import date
from flask import Flask, Markup, render_template

app = Flask(__name__)

today = date.today()

today_formatted = today.strftime('%b %d, %Y')

weekday = (today.weekday()) + 1

@app.route("/")
def chart():
    total_labels = ["In","Out"]
    total_values = [total_calories_in,total_calories_out]
    total_diff = (total_calories_in - total_calories_out)
    total_weight_loss_est = abs(((total_diff / weekday) * 7) / 3500.0)

    if(total_diff < 0):
        in_weekly_deficit = True
    else:
        in_weekly_deficit = False

    today_labels = ["In","Out"]
    today_values = [calories_in_today,calories_out_today]
    today_diff = (calories_in_today - calories_out_today)

    if(today_diff < 0):
        in_daily_deficit = True
    else:
         in_daily_deficit = False

    return render_template('chart.html',
                total_values = total_values,
                total_labels = total_labels,
                today_values = today_values,
                today_labels = today_labels,
                total_diff = total_diff,
                today_diff = today_diff,
                username = username,
                today = today_formatted,
                weekday = weekday,
                in_weekly_deficit = in_weekly_deficit,
                in_daily_deficit = in_daily_deficit,
                total_weight_loss_est = total_weight_loss_est)

def calories_in():

    total_calories_in = 0

    for calories_in_item in caloriesin['foods-log-caloriesIn']:
        calories_in = calories_in_item['value']
        print "%s - %s" % (calories_in_item['dateTime'],calories_in)
        total_calories_in += int(calories_in)

    return total_calories_in


def calories_out():

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


while True:
    # Get user profile info, calories in and calories out json data from the past week.
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



    username = userprofile['user']['displayName']

    if __name__ == "__main__":
        app.run(host='localhost', port=5001,debug=True)

    time.sleep(60)
