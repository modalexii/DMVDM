#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main():

	#See Specifications:Data.Processing.Flow

	import eventful_api, gcal_api, transmogrify, merge, config

	# get events from Eventful
	a = eventful_api.eventfulQuery(
		"Future",
		config.eventful_pull_count
	)
	a = a.results()

	# make Eventful objects into Google Calendar objects
	for i,e in enumerate(a):
		e = transmogrify.blank_missing_values(e)
		e = transmogrify.googlify(e)
		a[i] = e

	# get current state of the calendar from Google
	b = gcal_api.calendarOperation()
	b.list_future_events()
	b.execute()
	b = b.response

	merge.merge_and_push(a,b)


if __name__ == "__main__":
	main()
	#dev_add_events()
