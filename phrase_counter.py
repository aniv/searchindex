import argparse, os, re, string, pprint, operator
import cPickle as pickle

def main():
	"""
	Parse command-line arguments and invoke appropriate search functions
	"""
	parser = argparse.ArgumentParser(description='Find occurances and average word distance of a phrase in a file')
	parser.add_argument('file', help='file name to search')
	parser.add_argument('phrase', help='a phrase to search for (in quotes)')
	parser.add_argument('--algorithm', choices=['search','index'], dest='algo', default='index', help='choice of algorithm: search (linear forward) or index (inverted)')
	parser.add_argument('--case-sensitive', dest='case_sensitive', action='store_true',
	                   help='apply case sensitivity when searching for phrase')
	parser.add_argument('--rebuild-index', dest='rebuild_index', action='store_true',
	                   help='force a rebuild of the inverted index')
	parser.add_argument('--index-stats', dest='index_stats', action='store_true',
	                   help='print out statistics of index files')
	args = parser.parse_args()

	document = args.file
	if (type(args.phrase) is list):  # if phrase is provided not in quotes
		phrase = string.join(args.phrase, ' ')
	else:
		phrase = args.phrase
	
	if (args.rebuild_index or not find_index(document)):
		build_all_indices(document)
	
	lookup_index = len(phrase.split())
	if (args.algo == 'search' or lookup_index > 5):
		results = linear_forward_search(phrase, document, args.case_sensitive)
	else:
		results = index_search(phrase, document, args.case_sensitive)

	if (results != None and len(results) > 0):
		print "%d occurences of '%s' in '%s'" % ( len(results), phrase, document )
		print "Word positions: " + str(results)
		print "Avg word distance: " + str( reduce(lambda x,y: x+y, results) / len(results) )
	else:
		print "No occurences of '%s' found in %s" % ( phrase, document )
		
	if (args.index_stats):
		compute_index_stats(document)


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
		return None;
	

def build_all_indices(document):
	"""
	Rebuild inverted index for phrases of length 1 to PHRASE_SIZE_INDEX inclusive
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
			
			line_terms = re.compile('\W+').split(line)  # aggressive removal of all punc's - improves matches
			#line_terms = map(lambda x: x.rstrip(",.:;'\"!?()-"), line.split())  # less aggressive removal of punc's - misses some matches

			if (ngram > 0):
				for i in xrange(0, len(line_terms)):
					window = i + ngram  # normally ngrams -1, but +1 for use in indices below
					if (window >= len(line_terms)):
						break
					terms.append(" ".join(line_terms[i:window]))
			else:
				break
		
		for i, t in enumerate(terms):
			if t in index:
				index[t].append(tc + i)
			else:
				index[t] = [tc + i]

		tc += len(line_terms)

	f.close()
	return index

def find_index(document):
	"""
	Find indices for document in current working directory
	"""
	return len(filter(lambda f: f.find(".idx")>0, os.listdir("."))) > 0

def compute_index_stats(document):
	"""
	Print interesting phrase statistics from index files
	"""
	for index_file in filter(lambda f: f.find(".idx")>0, os.listdir(".")):
		index = pickle.load(open(index_file, 'rb'))
		sized_index = {}
		for p in index:
			sized_index[p] = len(index[p])
			
		# Sorted rep of a dict: http://stackoverflow.com/questions/613183/python-sort-a-dictionary-by-value
		sized_index = sorted(sized_index.iteritems(), key=operator.itemgetter(1))
		print
		print "Most popular %s-length phrases (from %s)" % (index_file.split('.')[0].split('_')[1] , index_file)
		print sized_index[-5:-1]
		

def linear_search(phrase, document, case_sensitive=False):
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