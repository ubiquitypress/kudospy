#!/usr/bin/python

import datetime
import csv
import os

import db
import settings
from pprint import pprint

def build_csv_row(doi, author):
	if author.get('middle_name'):
		name = '{first_name} {middle_name} {last_name}'.format(**author)
	else:
		name = '{first_name} {last_name}'.format(**author)

	if author['settings'].get('orcid'):
		parts = author['settings'].get('orcid').split('http://orcid.org/')
		orcid = parts[1]
	else:
		orcid = ''

	return [doi, name, author.get('email'), orcid]

def get_csv_data(cursor, published_articles, journal_code):

	records = []
	
	for pub_article in published_articles:
		article = db.get_article(cursor, pub_article.get('article_id'))

		doi = article['settings'].get('pub-id::doi')

		if doi:
			authors = db.get_authors(cursor, pub_article.get('article_id'))

			author_emails = []
			for author in authors:
				if not author.get('email') in settings.EXCLUDED_EMAILS and not author.get('email') in author_emails:
					author_emails.append(author.get('email'))
					row = build_csv_row(doi, author)
					records.append(row)

	return records

def generate_csv(journal, records):

	date = datetime.date.today()

	year = date.year
	month = date.month
	day = date.day

	file_name = "{0}-doi-{1}-{2}-{3}.csv".format(journal.get('path'), year, month, day)

	pprint(records)
	with open(os.path.join(settings.BASE_DIR, 'csv', file_name), 'w') as fp:
	    a = csv.writer(fp, delimiter=',')
	    for row in records:
	    	print row
	    	a.writerow(row)

# connect to the database
cursor, con = db.connect_to_db()

# grab the journals and loop through them generating a csv for each
journals = db.multi_getter_where(cursor, table='journals', where='enabled=1')

for journal in journals:
	print "Generating CSV for {0}".format(journal.get('path'))

	# grab this journal's published articles
	published_articles = db.get_published_articles(cursor, journal.get('journal_id'))

	# get csv record rows for each author
	records = get_csv_data(cursor, published_articles, journal.get('path'))
	print "{0} records found".format(len(records))

	# export a csv for these records
	generate_csv(journal, records)


db.close(con)