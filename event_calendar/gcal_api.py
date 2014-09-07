#!/usr/bin/env python
# -*- coding: utf-8 -*-

class calendarOperation():
	'''
	Do things with the Google Calendar by wrapping the APIv3 service object.
	See developers.google.com/api-client-library/python/apis/calendar/v3
	'''

	def __init__(self):
		'''
		Authorize to Google and create a Service object that can read and
		write to the calendar
		'''
		import httplib2
		from apiclient.discovery import build
		from oauth2client.client import SignedJwtAssertionCredentials
		import gcal_api_secrets

		credentials = SignedJwtAssertionCredentials(
			gcal_api_secrets.service_email,
			gcal_api_secrets.get_p12(),
			scope='https://www.googleapis.com/auth/calendar',
		)

		http = httplib2.Http()
		http = credentials.authorize(http)

		self.service = build(
			serviceName = 'calendar',
			version = 'v3',
			http = http,
			developerKey = gcal_api_secrets.developer_key
		)

		self.gcal_id = gcal_api_secrets.gcal_id

	def execute(self):
		'''
		Send staged transactions
		'''
		self.response = self.staged_transaction.execute()

	def new_event(self,event_data):
		'''
		Add new event(s) to the calendar.
		'''
		self.staged_transaction = self.service.events().insert(
			calendarId = self.gcal_id, 
			body = event_data
		)

	def update_event(self,event_data,event_id):
		'''
		Update existing event(s) on the calendar.
		'''
		event_data["sequence"] += 1
		self.staged_transaction = self.service.events().update(
			calendarId = self.gcal_id, 
			eventId = event_id,
			body = event_data,
		)

	def get_event_by_id(self,event_id):
		'''
		Return the event object with the given ID 
		'''
		self.staged_transaction = self.service.events().get(
			calendarId = self.gcal_id, 
			eventId = event_id,
		)

	def list_future_events(self):
		from datetime import datetime
		today = datetime.now()
		today = today.strftime("%Y-%m-%dT00:00:00+04:00")
		# TODAY will be off by an hour during EDT. NBD.

		self.staged_transaction = self.service.events().list(
			calendarId = self.gcal_id, 
			timeMin = today,
			showDeleted = True,
		)
		


