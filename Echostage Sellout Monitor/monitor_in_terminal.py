from bs4 import BeautifulSoup 
from datetime import datetime
from time import sleep
import urllib2

url ="http://echostage.wantickets.com/Events/168594/Cash-Cash-Tritonal/"
wait_between_checks = 60

def get_soup_from_url(url):
	usock = urllib2.urlopen(url)
	data = usock.read()
	usock.close()
	soup = BeautifulSoup(data)
	return soup

def is_echo_ticket_page(soup):
	if soup.find('div', {'id':'divEventMainInfo'}):
		return True
	else:
		return False

def get_sellout_risk(soup):
	try:
		sellout_risk = soup.find('div', {'class':'SelloutRiskText'}).text
	except AttributeError:
		sellout_risk = None
	return sellout_risk

def get_time():
	return datetime.now().strftime("%I:%M:%S")

def main():

	print
	print "[i] Now monitoring Sellout Risk. ^C to stop." 
	print

	while True:

		now = get_time()
		soup = get_soup_from_url(url)

		if not soup:
			print "[!] No content from URL"
			exit(10)

		if not is_echo_ticket_page(soup):
			print "[!] Content from URL does not appear to be an Echostage ticket page - check URL"
			exit(20)

		sellout_risk = get_sellout_risk(soup)

		if not sellout_risk:
			print "[i] [%s] No Sellout Risk meter yet" % now
		else:
			print "[i] [%s] Sellout Risk: %s" % (now, sellout_risk)

		sleep(wait_between_checks)

if __name__ == "__main__":
	main()