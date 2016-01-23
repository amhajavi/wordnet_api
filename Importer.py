#!/usr/bin/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import progressbar
from libs.db import connect
if __name__ == "__main__":
	
	conn = connect()

	

	wordrepo = ET.parse('XMLFILES/words.xml')
	root = wordrepo.getroot()
	bar = progressbar.ProgressBar(maxval=len(root),
								  widgets=[
									    'Words Phase 1 [', progressbar.Timer(), '] ',
									    progressbar.Bar(),
									    ' (', progressbar.ETA(), ') ',
									])
	bar.start()
	for idx, word in enumerate(root):
		bar.update(idx)
		cur = conn.cursor()
		if word is not None:
			word_id = word.find("./WID")
			word_value = word.find("./WORDVALUE")
			pos = word.find("./POS")
			ava = word.find("./AVAINFO")
			if  word_id is not None and word_value is not None and pos is not None and ava is not None :
				cur.execute("INSERT INTO words (id, word_value, pos, ava) VALUES (%s, %s, %s, %s)",(word_id.text, word_value.text, pos.text, ava.text))
	conn.commit()

	print '\n'

	synrepo = ET.parse('XMLFILES/synsets.xml')
	root = synrepo.getroot()
	bar2 = progressbar.ProgressBar(maxval=len(root),
								  widgets=[
									    'Words Phase 2 [', progressbar.Timer(), '] ',
									    progressbar.Bar(),
									    ' (', progressbar.ETA(), ') ',
									])
	bar2.start()
	for idx, synset in enumerate(root):
		bar2.update(idx)
		if synset is not None:
			cur = conn.cursor()
			syn_id = synset.find("./ID")
			pos = synset.find("./POS")
			semcat = synset.find("./SemanticCategory")
			gloss = synset.find("./GLOSS")
			if  syn_id is not None and pos is not None and semcat is not None and gloss is not None :
			 	cur.execute("INSERT INTO synsets (id, pos, semcat, gloss) VALUES (%s, %s, %s, %s)",(syn_id.text, pos.text, semcat.text, gloss.text))
		for sense in synset.find("./SENSES"):
			word_id = sense.find('./WID')
			cur.execute("INSERT INTO syn_word (sid, wid) VALUES (%s, %s)",(syn_id.text, word_id.text))


	conn.commit()

	print '\n'

	synrepo = ET.parse('XMLFILES/sensesRelations.xml')
	root = synrepo.getroot()
	bar3 = progressbar.ProgressBar(maxval=len(root),
								  widgets=[
									    'Sense Relations [', progressbar.Timer(), '] ',
									    progressbar.Bar(),
									    ' (', progressbar.ETA(), ') ',
									])
	bar3.start()
	for idx, synset in enumerate(root):
		bar3.update(idx)
		if synset is not None:
			cur = conn.cursor()

			wid_1 = synset.find("./WID_1") 
			sid_1 =  synset.find("./SID_1") 
			wid_2 = synset.find("./WID_2")  
			sid_2 = synset.find("./SID_2")  
			relation = 	synset.find("./RELATION_TYPE")
			if  wid_1 is not None and sid_1 is not None and wid_2 is not None and sid_2 is not None and relation is not None :
			 	cur.execute("INSERT INTO word_word (wid_1, sid_1, wid_2, sid_2, relation) VALUES (%s, %s, %s, %s, %s)",(wid_1.text, sid_1.text, wid_2.text, sid_2.text, relation.text))
	conn.commit()

	print '\n'

	synrepo = ET.parse('XMLFILES/synsetsRelation.xml')
	root = synrepo.getroot()
	bar4 = progressbar.ProgressBar(maxval=len(root),
								  widgets=[
									    'Synset Relations [', progressbar.Timer(), '] ',
									    progressbar.Bar(),
									    ' (', progressbar.ETA(), ') ',
									])
	bar4.start()
	for idx, synset in enumerate(root):
		bar4.update(idx)
		if synset is not None:
			cur = conn.cursor()

			id_1 = synset.find("./ID_1") 
			id_2 =  synset.find("./ID_2")
			relation = 	synset.find("./RELATION_TYPE")
			if  id_1 is not None and id_2 is not None and relation is not None :
			 	cur.execute("INSERT INTO synset_synset (id_1, id_2, relation) VALUES (%s, %s, %s)",(id_1.text, id_2.text, relation.text))
	conn.commit()