import MySQLdb
import MySQLdb.cursors

import settings

def connect_to_db():

	con = MySQLdb.connect(
		host=settings.SERVER_ADDRESS, 
		user=settings.USERNAME, 
		passwd=settings.PASSWORD, 
		db=settings.DB_NAME,
		cursorclass=MySQLdb.cursors.DictCursor)

	# prepare a cursor object using cursor() method
	return con.cursor(), con

def close(con):
	# disconnect from server
	con.close()

def dict_ojs_settings_results(settings_results):
	results_dict = {}

	for row in settings_results:
		results_dict[row['setting_name']] = row['setting_value']

	return results_dict

def get_mysql_version(cursor):
	# execute SQL query using execute() method.
	cursor.execute("SELECT VERSION()")

	# Fetch a single row using fetchone() method.
	data = cursor.fetchone()

	print "Database version : %s " % data

def multi_getter(cur, table):
	sql = "SELECT * FROM %s" % table
	cur.execute(sql)
	results = cur.fetchall()
	return results

def multi_getter_where(cur, table, where):
	sql = "SELECT * FROM %s WHERE %s" % (table, where)
	cur.execute(sql)
	results = cur.fetchall()
	return results

def get_published_articles(cur, journal_id):
	sql = '''
	SELECT pa.* FROM published_articles pa
	JOIN issues i ON i.issue_id = pa.issue_id
	WHERE i.journal_id = %s
	''' % journal_id
	cur.execute(sql)
	results = cur.fetchall()
	return results

def get_settings(cur, article_id, table):
	sql = '''
	SELECT * FROM %s
	WHERE article_id = %s
	''' % (table, article_id)
	cur.execute(sql)
	results = cur.fetchall()

	return results

def get_article(cur, article_id):
	sql = '''
	SELECT * FROM articles
	WHERE article_id = %s
	''' % article_id
	cur.execute(sql)
	results = cur.fetchall()

	for result in results:
		result['settings'] = dict_ojs_settings_results(get_settings(cur, article_id, table='article_settings'))

	return results

def get_authors(cur, article_id):
	sql = '''
	SELECT * FROM authors
	WHERE article_id = %s
	''' % article_id
	cur.execute(sql)
	results = cur.fetchall()

	for result in results:
		result['settings'] = dict_ojs_settings_results(get_settings(cur, article_id, table='author_settings'))

	return results



