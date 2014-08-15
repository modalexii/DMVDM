#!/usr/bin/env python

import httplib2
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
from gcal_api_secrets import *

# API Docs: https://developers.google.com/api-client-library/python/apis/calendar/v3

credentials = SignedJwtAssertionCredentials(
	service_email,
	get_p12(),
	scope='https://www.googleapis.com/auth/calendar',
)

http = httplib2.Http()
http = credentials.authorize(http)

service = build(serviceName = 'calendar', version = 'v3', http = http,
	developerKey = developer_key)


 
event = {
 "end": {
  "dateTime": "2014-08-17T01:31:16.0",
  "timeZone": "America/New_York"
 },
 "start": {
  "dateTime": "2014-08-16T09:31:16.0",
  "timeZone": "America/New_York"
 },
 "description": "Here is a description!",
 "summary": "API Test @ dev.g.com",
 "location": "Echostage DUH"
}



book = service.events().insert(calendarId = gcal_id, body = event)
result = book.execute()

import pprint
pprint.pprint(result)