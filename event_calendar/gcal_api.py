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

def rfc3339(eventful_time_string):
	d = eventful_time_string.replace(" ", "T")
	return d

def create_end_time(start_time,mins):
	from datetime import datetime, timedelta
	d = datetime.strptime(start_time,"%Y-%m-%dT%H:%M:%S")
	d = d + timedelta(minutes=mins)
	d = d.strftime("%Y-%m-%dT%H:%M:%S")
	return d

def googlify(event):
	'''
	Convert an event object from eventful to an event object as expected
	by the Google Calendar API
	'''

	google_event = {}

	display_title = "%s @ %s" % (event["title"], event["venue_name"])
	google_event["summary"] = display_title,

	start_datetime = rfc3339(event["start_time"])
	google_event["start"] = {
		"dateTime" : start_datetime,
		"timeZone" : "America/New_York",
	}

	try:
		end_datetime = rfc3339(event["stop_time"])
	except AttributeError:
		# no end time given, but Google requires one, so 
		# add some minutes to the start time
		end_datetime = create_end_time(start_datetime,240)
	finally:
		google_event["end"] = {
			"dateTime" : end_datetime,
			"timeZone" : "America/New_York",
		}
		end_time_disclaimer = "*** End time not specified, so we guessed ***\n"

	full_location = "%s, %s, %s, %s" % (
		event["venue_name"], event["venue_address"], 
		event["city_name"],  event["region_abbr"]
	)
	google_event["location"] = full_location

	performers = ""
	try:
		for l in event["performers"]["performer"]:
			performers = "%s%s  ::\n%s\n" % (
				performers,
				l["name"],
				l["short_bio"],
			)
	except TypeError:
		performers = "%s\n\n%s\n%s" % (
			performers,
			event["performers"]["performer"]["name"], 
			event["performers"]["performer"]["short_bio"],
		)

	if event["price"]:
		price = event["price"]
	else:
		price = "Unknown"

	links = ""
	try:
		for l in event["links"]["link"]:
			links = "%s\n\n%s\n%s" % (links, l["description"], l["url"])
	except TypeError:
		links = "%s\n\n%s\n%s" % (
			links,
			event["links"]["link"]["description"], 
			event["links"]["link"]["url"],
		)

	description = '''{end_time_disclaimer}{performers}
Price: {price}
{links}
	'''.format(**locals())

	google_event["description"]	= description
	
	return google_event

import pprint
import eventful_api
request = eventful_api.eventfulQuery(date="Future", size=3)
events = request.results()

for e in events:
	e = googlify(e)
	pprint.pprint(e)
	book = service.events().insert(calendarId = gcal_id, body = e)
	result = book.execute()
	pprint.pprint(result)