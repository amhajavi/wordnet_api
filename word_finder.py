
from libs.db import connect

def find_relatives(word):
	conn = connect()
	word_id = None
	syn_id = None
	word_relatives = {}
	cur = conn.cursor()
	cur.execute( "Select id from words where word_value = %s" ,[str(word)])
	result = cur.fetchone()
	if result is not None:
		word_id = result[0]
	if word_id:
		word_relatives['word'] = word
		cur.execute( "Select wid_2,sid_2,relation from word_word where wid_1 = %s" ,[word_id])
		result = cur.fetchall()
		cur.execute( "Select wid_1,sid_1,relation from word_word where wid_2 = %s" ,[word_id])
		result += cur.fetchall()
		word_relatives['direct_relations'] = []
		for record in result:
			cur.execute( "Select word_value from words where id = %s" ,[str(record[0])])
			related = cur.fetchone()
			if related:
				relation = {'word':related[0], 'sense_id':record[1], 'relation':record[2]}
				word_relatives['direct_relations'].append(relation)

		word_relatives['synsets'] = []
		cur.execute( "Select sid from syn_word where wid = %s" ,[word_id])
		result = cur.fetchall()
		for record in result:
			synset_id = record[0]
			synset = {'id':synset_id,'relations':[]}
			cur.execute( "Select id_2,relation from synset_synset where id_1 = %s" ,[synset_id])
			relatives = cur.fetchall()
			cur.execute( "Select id_1,relation from synset_synset where id_2 = %s" ,[synset_id])
			relatives += cur.fetchall()
			for relative in relatives:
				synset_id = relative[0]
				cur.execute( "Select word_value from syn_word join words on syn_word.wid = words.id where sid = %s" ,[synset_id])
				relation = {'words':[],'relation':relative[1]}
				for word in cur.fetchall():
					relation['words'].append(word[0])
				synset['relations'].append(relation)
			word_relatives['synsets'].append(synset)
	if len(word_relatives) > 0:
		return word_relatives
	else:
		print "theres nothing found"
		return None
