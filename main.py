#!/usr/bin/python

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

	record = [doi, name, author.get('email'), orcid]

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

# connect to the database
cursor, con = db.connect_to_db()

# grab the journals and loop through them generating a csv for each
journals = db.multi_getter_where(cursor, table='journals', where='enabled=1')

for journal in journals:
	print journal.get('path')

	# grab this journal's published articles
	published_articles = db.get_published_articles(cursor, journal.get('journal_id'))
	get_csv_data(cursor, published_articles, journal.get('path'))


db.close(con)