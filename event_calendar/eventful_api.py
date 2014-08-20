#!/usr/bin/env python

def list_to_search_expr(l,bool_op = "||"):
	'''
	Convert list L to search expression for eventful: add BOOL_OP operators
	between each term, and return as unicode. Everything after "#" on a line
	is removed (i.e. "#" = start comment).
	'''
	for p, w in enumerate(l):
		w = w.split("#")[0]
		w = w.replace('\n','')
		w = w.strip()
		l[p] = w

	search_expr = (" {bool_op} ".format(**locals())).join(l)

	return search_expr

def print_for_humans(events):
	'''
	Print the event list for inspection by a person
	'''
	for e in events["events"]["event"]:
		e = blank_missing_attribs(e)
		print "Summary: %s @ %s" % (e["title"], e["venue_name"])
		if e["all_day"] != "0":
			print "All Day Event"
		else:
			print "Start: %s, Stop: %s" % (e["start_time"], e["stop_time"])
		print "Location: %s, %s, %s, %s" % (
			e["venue_name"],
			e["venue_address"], 
			e["city_name"], 
			e["region_abbr"]
			)
		print "Price: %s" % e["price"]
		try:
			for l in e["links"]["link"]:
				print "%s %s" % (l["description"], l["url"])
		except TypeError:
			print "%s %s" % (
				e["links"]["link"]["description"], 
				e["links"]["link"]["url"],
			)
		print "\n"

		#import pprint
		#pprint.pprint(e)

class eventfulQuery():
	'''
	A query to the Eventful API, including hard-coded whitelist and
	blacklist content to filter potential results based on tag & venue.
	'''

	def __init__(self, date, size):

		self.date = date
		self.size = size

		# process wordlists

		with open("./wl_whitelist_keywords.txt") as f:
			wl_whitelist_keywords = f.readlines()
		
		wl_whitelist_keywords = list_to_search_expr(wl_whitelist_keywords)

		with open("./wl_blacklist_keywords.txt") as f:
			wl_blacklist_keywords = f.readlines()

		wl_blacklist_keywords = list_to_search_expr(wl_blacklist_keywords)

		with open("./wl_whitelist_venues.txt") as f:
			wl_whitelist_venues = f.readlines()

		wl_whitelist_venues = list_to_search_expr(wl_whitelist_venues)

		# form the query expressions

		self.keyword_query = "(tag:({wl_whitelist_keywords})) && \
						  (-tag:({wl_blacklist_keywords}))\
						 ".format(**locals())

		self.location_query = wl_whitelist_venues

	def results(self):

		'''
		Send the request to Eventful. API Docs: https://api.eventful.com
		'''

		import eventful

		api = eventful.API("FrX2dpPfjNW5V5hv")

		self.events = api.call("/events/search",
			keywords = self.keyword_query,
			category = "music",
			location = self.location_query, 
			date = self.date,
			include = "price,links,categories",
			page_size = self.size,
			sort_order = "date", # for humans only. remove later.
		)

		return self.events["events"]["event"]


if __name__ == '__main__':
	request = eventfulQuery(date="Future", size=5)
	events = request.results()
	print_for_humans(events)