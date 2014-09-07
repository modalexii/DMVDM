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

	for eventful_event in eventful_data:

		if not eventful_event["id"] in gcal_event_ids:
			# event has never been on the calendar

			print "[+] Adding event ID %s" % eventful_event["id"]

			n = gcal_api.calendarOperation()
			n.new_event(eventful_event)
			n.execute()

		else:
			# event is, or has been, on Google Calendar
			print "[-] Not adding event with id %s" % eventful_event["id"]

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


