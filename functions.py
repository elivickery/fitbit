def chart():
    total_labels = ["Calories In","Calories Out"]
    total_values = [total_calories_in,total_calories_out]
    return render_template('chart.html', values=total_values, labels=total_labels)

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
