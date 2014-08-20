'''
def main():

	#See Specifications:Data.Processing.Flow

	import eventful_api, gcal_api, app_storage, transmogrify, merge, config

	# get events from Eventful
	a = eventful_api.eventfulQuery(
		"Future",
		config.eventful_pull_count
	)
	a = a.results()

	# make Eventful objects into Google Calendar objects
	for event in a:
		this_index = event.index(a)
		event = transmogrify.blank_missing_values(event)
		event = transmogrify.googlify(event)
		a[this_index] = event

	# get current state of the calendar from Google
	b = gcal_api.calendarOperation().list_future_events().results()


	c = app_storage.read(????)

	for i in a:
		try:
			merge.as_update(i,b[i])
		except (something????):
			merge.as_insert(i,b[i])

	e = set(b + c)
	app_storage.write(e)

#if __name__ == __main__:
#	main()
'''

import eventful_api, gcal_api, app_storage, transmogrify, merge
import pprint

e = gcal_api.calendarOperation()
e.list_future_events()
e.execute()
pprint.pprint(e.response)

'''
e = eventful_api.eventfulQuery("Future",3)
e = e.results()

for i in e:
	i = transmogrify.blank_missing_values(i)
	g = transmogrify.googlify(i)
	t = gcal_api.calendarOperation()
	t.new_event(g)
	r = t.execute()
	pprint.pprint(r.response)
'''