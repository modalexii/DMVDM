#!/usr/bin/env python
# -*- coding: utf-8 -*-

def merge_and_push(eventful_data,gcal_data):
	'''
	Merge new /w current event data and push results to Google Calendar, per 
	specifications:Data.Processing.Merging
	'''
	import gcal_api

	gcal_data = gcal_data["items"]
	gcal_event_ids = [e["id"] for e in gcal_data]

	# Lazy presentation 
	new_event_list = []
	known_event_count = 0

	for eventful_event in eventful_data:

		if not eventful_event["id"] in gcal_event_ids:
			# event has never been on the calendar

			new_event_list.append(eventful_event["summary"])

			n = gcal_api.calendarOperation()
			n.new_event(eventful_event)
			try:
				n.execute()
			except Exception as e:	
				print "Unable to process {s}: {e}".format(
					s = eventful_event["summary"],
					e = str(e)
				)

		else:
			# event is, or has been, on Google Calendar
			known_event_count += 1

		'''

			if gcal_data["id"]["status"] == "cancelled"
				# event was deleted through Google Calendar
				print "[i] Not adding event with id %s" % gcal_data["id"]
				print "    because it was deleted through Google Calendar."
				pass

			else:
				# event is currently on Google Calendar

				for v in eventful_event.values():
					if not v in gcal_data["id"].values():
		'''

	# Lazy presentation continued
	if new_event_list:
		print "Adding the following new events:"
		print "\n".join(new_event_list)
	else:
		print "No new events."

	if known_event_count:
		print "\nAlso found {n} known events.".format(n=known_event_count)
	else:
		print "\nDid not find any known events."

