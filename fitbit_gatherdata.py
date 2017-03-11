import fitbit, json

tokenfile = "user_settings.txt"

z = fitbit.Fitbit();

try:
    token = json.load(open(tokenfile))
except IOError:
    auth_url = z.GetAuthorizationUri()

    print "Please visit the link below and approve the app:\n %s" % auth_url

    access_code = raw_input("Please enter code (from the URL you were redirected to): ")

    token = z.GetAccessToken(access_code)

    json.dump(token, open(tokenfile,'w'))

# Sample API call
# response = z.ApiCall(token, '/1/user/-/profile.json')
response = z.ApiCall(token, '/1/user/-/activities/calories/date/today/1w.json')

# Token is part of the response. Note that the token pair can change when a refresh is necessary.
# So we replace the current token with the response one and save it.
token = response['token']
json.dump(token, open(tokenfile,'w'))

print response

# print "Welcome %s!" % response['user']['displayName']
