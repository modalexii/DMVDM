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
		eventful_event["venue_name"]
	)
	google_event["summary"] = display_title,

	# start time: RFC3339-format string
	start_datetime = eventful_event["start_time"].replace(" ", "T")
	google_event["start"] = {
		"dateTime" : start_datetime,
		"timeZone" : "America/New_York",
	}

	# end time: RFC3339-format string
	try:
		end_datetime = eventful_event["stop_time"].replace(" ", "T")
	except AttributeError:
		# no end time was given, but Google requires one, so add some minutes
		# to the start time.
		end_datetime = add_minutes(start_datetime,240)
	finally:
		google_event["end"] = {
			"dateTime" : end_datetime,
			"timeZone" : "America/New_York",
		}
		end_time_disclaimer = "*** End time not specified, so we guessed ***\n"

	# location: venue + street + city + region/state
	full_location = "%s, %s, %s, %s" % (
		eventful_event["venue_name"], eventful_event["venue_address"], 
		eventful_event["city_name"],  eventful_event["region_abbr"]
	)
	google_event["location"] = full_location

	# performers: name, bio
	performers = ""

	try:
		for p in eventful_event["performers"]:
			if p:
				performers = "%s%s  ::\n%s\n" % (
					performers,
					eventful_event["performers"]["performer"]["name"],
					eventful_event["performers"]["performer"]["short_bio"],
				)
	except TypeError:
		# performers = None (was not filled out)
		import pprint
		pprint.pprint(eventful_event["performers"])
		performers = "-"

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
		for n,l in enumerate(eventful_event["links"]["link"]):
			links = "%s\n%s\n%s" % (
				links,
				eventful_event["links"]["link"]["description"],
				eventful_event["links"]["link"]["url"],
			)		
	#except:
		# give up
	#	raise
	#	links = "-"

	# description: performers, price, links
	description = '''\
{end_time_disclaimer}\
{performers}\n
Price: {price}\n
{links}\n

Events by Eventful
http://eventful.com
	'''.format(**locals())

	google_event["description"]	= description
	
	return google_event