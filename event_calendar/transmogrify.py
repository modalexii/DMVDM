#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Convert cbjects for interoperability between interfaces
'''

def add_minutes(start_time,mins):
	'''
	Add MINS minutes to RFC3339-format time string start_time
	'''
	from datetime import datetime, timedelta
	d = datetime.strptime(start_time,"%Y-%m-%dT%H:%M:%S")
	d = d + timedelta(minutes=mins)
	d = d.strftime("%Y-%m-%dT%H:%M:%S")
	return d

def strip_punctuation(in_string):
	'''
	Remove punctuation from a string
	'''
	import re, string
	e = re.compile('[%s]' % re.escape(string.punctuation))
	s = e.sub('', in_string)
	return s

def blank_missing_values(event):
	'''
	If any of the items listed in REQUIRED_KEYS are missing from dictionary
	EVENT, add them as empty strings.
	Do not list attribs that Google doesn't want blank, e.g., dates & times.
	'''

	required_keys = [ 
		"title",
		"description",
		"venue_name",
		"performers",
		"links",
		"price",
	]

	for a in required_keys:
		try:
			event[a]
		except KeyError:
			event[a] = ""

	return event

def googlify(eventful_event):
	'''
	Convert an event object from Eventful into something that we can
	send to the Google Calendar API
	'''

	google_event = {}

	# title: event @ venue
	display_title = "%s @ %s" % (
		eventful_event["title"],
		eventful_event["venue_name"],
	)

	google_event["summary"] = display_title

	# start time: RFC3339-format string
	start_datetime = eventful_event["start_time"].replace(" ", "T")
	google_event["start"] = {
		"dateTime" : start_datetime,
		"timeZone" : "America/New_York",
	}


	end_time_disclaimer = ""
	# end time: RFC3339-format string
	try:
		end_datetime = eventful_event["stop_time"].replace(" ", "T")
	except AttributeError:
		# no end time was given, but Google requires one, so add some minutes
		# to the start time.
		end_datetime = add_minutes(start_datetime,240)
		end_time_disclaimer = "*** End time not specified, so we guessed ***\n"
	finally:
		google_event["end"] = {
			"dateTime" : end_datetime,
			"timeZone" : "America/New_York",
		}
		

	# location: venue + street + city + region/state
	full_location = "%s, %s, %s, %s" % (
		eventful_event["venue_name"],
		eventful_event["venue_address"], 
		eventful_event["city_name"],
		eventful_event["region_abbr"],
	)
	google_event["location"] = full_location

	# performers: name, bio
	performers = ""

	try:
		for p in eventful_event["performers"]:
			if p:
				n = eventful_event["performers"]["performer"]["name"]
				b = eventful_event["performers"]["performer"]["short_bio"]
				if n and b:
					performers = "%s%s: %s\n\n" % (
						performers,
						n,
						b,
					)
	except TypeError:
		# performers = None (was not filled out)
		#import pprint
		#pprint.pprint(eventful_event["performers"])
		try:
			for p in eventful_event["performers"]["performer"]:
				if p:
					n = p["name"]
					b = p["short_bio"]
					if n and b:
						performers = "%s%s: %s\n\n" % (
							performers,
							n,
							b,
						)
		except AttributeError:
			# no performers listed
			pass
		except Exception, e:
			#print "[!] Error processing performers for {s}: {e}".format(
			#	s = google_event["summary"],
			#	e = str(e)
			#)
			performers = ""

	# price
	if eventful_event["price"]:
		price = eventful_event["price"]
	else:
		price = "Unknown"

	# links: type of link, url
	# inconsistent packaging
	links = ""
	#try:
		# assume dict of dicts
	try:
		for l in eventful_event["links"]["link"]:
			if l["description"]:
				links = "%s%s\n%s\n\n" % (
					links,
					l["description"],
					l["url"],
				)
	except TypeError:
		try:
			for n,l in enumerate(eventful_event["links"]["link"]):
				links = "%s\n%s\n%s" % (
					links,
					eventful_event["links"]["link"]["description"],
					eventful_event["links"]["link"]["url"],
				)
		except:
			# arbitrary data ia hard and I quit
			links = ""

	# description: performers, price, links
	description = '''\
%s\
%s\n
Price: %s\n
%s

Events by Eventful
http://eventful.com
	''' % (
			end_time_disclaimer,
			performers,
			price,
			links,
		)

	google_event["description"]	= description

	event_id = eventful_event["id"]
	event_id = strip_punctuation(event_id)
	event_id = event_id.lower()
	google_event["id"] = event_id
	
	return google_event