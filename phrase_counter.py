import argparse, os, re, string, pprint
import cPickle as pickle

def main():
	"""
	Parse command-line arguments and invoke appropriate search functions
	"""
	parser = argparse.ArgumentParser(description='Find occurances and average word distance of a phrase in a file')
	parser.add_argument('file', help='file name to search')
	parser.add_argument('phrase', help='a phrase to search for (in quotes)')
	parser.add_argument('--algorithm', choices=['search','index'], dest='algo', default='index', help='choice of algorithm: search (linear forward) or index (inverted forward)')
	parser.add_argument('--case-sensitive', dest='case_sensitive', action='store_true',
	                   help='apply case sensitivity when searching for phrase')
	parser.add_argument('--rebuild-index', dest='rebuild_index', action='store_true',
	                   help='force a rebuild of the forward index')
	args = parser.parse_args()

	document = args.file
	if (type(args.phrase) is list):  # if phrase is provided not in quotes
		phrase = string.join(args.phrase, ' ')
	else:
		phrase = args.phrase
	
	print args
	
	if (args.rebuild_index):
		build_all_indices(document)
	
	if (args.algo == 'search'):
		results = linear_forward_search(phrase, document, args.case_sensitive)
		if (len(results) > 0):
			print "Found %d occurances of '%s' in %s" % ( len(results), phrase, document )
			print "With an average word distance of %d" % ( reduce(lambda x,y: x+y, results)/len(results) )
		else:
			print "No occurances of '%s' found in %s" % ( phrase, document )
	else:
		lookup_index = len(phrase.split())
		if (lookup_index <= 5):
		#for i in xrange(1, 6):
		#	results = index_search(phrase, document, args.case_sensitive, 'pg2600_'+str(i)+'.idx')
			results = index_search(phrase, document, args.case_sensitive)
			print results
		else:
			results = linear_forward_search(phrase, document, args.case_sensitive)

	#print results


def index_search(phrase, document, case_sensitivity=False, doc_override=""):
	"""
	Search a pre-built index for phrase in document
	Running time: O(1) constant lookup
	"""
	if (doc_override):
		idx_name = doc_override
	else:
		idx_name = document.split('.')[0] + '_' + str(len(phrase.split())) + '.idx'
	
	print "Searching for '%s' in %s" % (phrase, idx_name)
	index = pickle.load(open(idx_name, 'rb'))
	
	if phrase in index:
		return index[phrase]
	else:
		return -1;
	

def build_all_indices(document):
	"""
	Rebuild forward index for phrases of length 1 to PHRASE_SIZE_INDEX inclusive
	"""
	PHRASE_SIZE_INDEX = 5 + 1
	
	for i in xrange(1, PHRASE_SIZE_INDEX):
		print "Building index for phrase length %d ... " % i
		idx = build_index(document, i)
		idx_name = document.split('.')[0] + '_' + str(i) + '.idx'
		pickle.dump(idx, open(idx_name,'wb'))
		print "Done"


def build_index(document, ngram=0, case_sensitive=False):
	"""
	Build an index of phrases in document of length ngram 
	"""
	
	f = open(document)
	
	tc = 0   # Term count across the document
	index = {}  # Index for an ngram length
		
	while True:
		line = f.readline()
		terms = []
		
		if not line:
			break
		else:
			if (not case_sensitive):
				line = line.lower()
				
			line_terms = map(lambda x: x.rstrip(",.:;'\"!?()-"), line.split())

			if (ngram > 0):
				for i in xrange(0, len(line_terms)):
					window = i + ngram  # normally ngrams -1, but +1 for use in indices below
					terms.append(" ".join(line_terms[i:window]))
					if (window >= len(line_terms)):
						break
			else:
				break
		
		for i, t in enumerate(terms):
			if t in index:
				# print "Appending %s to index with pos %d" % (t, tc+i)
				index[t].append(tc + i)
			else:
				# print 'Adding %s to index with pos %d' % (t, tc+i)
				index[t] = [tc + i]

		tc += len(line_terms)

	f.close()
	return index

def linear_forward_search(phrase, document, case_sensitive=False):
	"""
	Perform a linear search for phrase in document and
	returns a list of character positions and word distance
	Running time: O(n), where n is length of document in characters
	"""
	
	f = open(document)
	s = 0
	p = 0
	wc = 0
	
	matching_positions = []
	
	if (not case_sensitive):
		phrase = phrase.lower()
	
	while True:
		dc = f.read(1)		# Pull a char from file stream
		
		if (not case_sensitive):
			dc = dc.lower()
		p += 1
		
		pc = phrase[s:s+1]  # Pull a char from phrase

		if not dc: 			# Done scanning file
			break
		elif dc == pc: 		# Initial character match
			s += 1
		elif dc != pc: 		# Failed character match
			if (re.match('\s', dc) != None):
				wc += 1
			s = 0
		
		if s == len(phrase): 	# Completed a phrase
			# print "Match found for %s at %d at %d" % (phrase, p, wc)
			matching_positions.append(wc)
			s = 0
			wc = 0
	
	f.close()	
	return matching_positions
						
if __name__ == "__main__":
	main()