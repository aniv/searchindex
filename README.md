# GA Dev Code Challenge

## Prompt:
Using a language of your choice write a program which takes in the input of a plaintext data file and a search string. The program returns both a count of the times the string appears in the file and the average number of words between each instance of the search string.
Run the program using this sample input file of War and Peace in text version using the search string: peace.

## Files:
* phrase_counter.py: Python program
* README.md: Readme (this file)
* pg2600.txt: Source document (War and Peace from Project Gutenberg)
* pg2600_1.idx: Inverted index file for phrases of length 1 (provided pre-built, can be regenerated using program) from pg2600.txt
* pg2600_2.idx: Inverted index file for phrases of length 2 (provided pre-built, can be regenerated using program) from pg2600.txt
* pg2600_3.idx: Inverted index file for phrases of length 3 (provided pre-built, can be regenerated using program) from pg2600.txt
* pg2600_4.idx: Inverted index file for phrases of length 4 (provided pre-built, can be regenerated using program) from pg2600.txt
* pg2600_5.idx: Inverted index file for phrases of length 5 (provided pre-built, can be regenerated using program) from pg2600.txt


## Output:
    charlie:Dev aniv$ python phrase_counter.py pg2600.txt peace
    Searching for 'peace' in pg2600_1.idx
    115 occurences of 'peace' in 'pg2600.txt'
    Word positions: [8, 73, 121, 147, 3697, 10898, 31776, 43747, 45915, 46679, 54504, 76825, 81627, 81630, 85281, 86767, 88604, 88653, 89320, 135870, 142590, 149110, 156127, 170661, 184785, 190459, 205408, 206130, 209734, 210870, 218442, 219514, 222703, 222718, 236890, 256021, 256030, 256037, 263601, 289264, 293280, 293372, 294823, 296761, 322037, 327122, 327193, 327623, 330294, 330564, 330926, 334251, 334444, 334631, 335039, 335153, 335168, 335224, 335598, 335927, 342583, 342632, 343109, 347984, 357467, 357503, 358941, 360504, 364757, 364994, 374154, 374559, 382097, 382105, 382230, 382571, 382733, 382940, 388796, 388807, 391893, 403823, 403843, 403904, 417365, 458088, 473177, 473217, 496094, 508779, 513215, 513218, 515709, 517015, 535448, 541339, 542112, 547237, 547832, 551719, 551765, 587307, 587314, 594644, 594656, 594674, 615477, 616479, 622550, 631879, 635385, 636569, 639052, 657758, 657774]
    Avg word distance: 331725

	charlie:GenAssemblyFair aniv$ python phrase_counter.py --help
	usage: phrase_counter.py [-h] [--algorithm {search,index}] [--case-sensitive]
	                         [--rebuild-index] [--index-stats]
	                         file phrase

	Find occurances and average word distance of a phrase in a file

	positional arguments:
	  file                  file name to search
	  phrase                a phrase to search for (in quotes)

	optional arguments:
	  -h, --help            show this help message and exit
	  --algorithm {search,index}
	                        choice of algorithm: search (linear forward) or index
	                        (inverted)
	  --case-sensitive      apply case sensitivity when searching for phrase
	  --rebuild-index       force a rebuild of the inverted index
	  --index-stats         print out statistics of index files


	charlie:Dev aniv$ python phrase_counter.py --index-stats pg2600.txt foo
	Searching for 'foo' in pg2600_1.idx
	1 occurences of 'foo' in 'pg2600.txt'
	Word positions: [298904]
	Avg word distance: 298904

	Most popular 1-length phrases (from pg2600_1.idx)
	[('of', 15007), ('to', 16753), ('', 20183), ('and', 22300)]

	Most popular 2-length phrases (from pg2600_2.idx)
	[('at the', 1288), ('and the', 1406), ('in the', 2213), ('to the', 2226)]

	Most popular 3-length phrases (from pg2600_3.idx)
	[('that he was', 146), ('out of the', 164), ('one of the', 166), ('i don t', 196)]

	Most popular 4-length phrases (from pg2600_4.idx)
	[('at the same time', 50), ('i don t know', 51), ('for the first time', 61), ('for a long time', 72)]

	Most popular 5-length phrases (from pg2600_5.idx)
	[('up and down the room', 13), ('the middle of the room', 14), ('that s it come on', 15), ('it seemed to him that', 16)]
	
	
## Solution:
I solved this by building an app that generates a series of inverted indices of phrases found in the source document. I consider a phrase to be a series of words separated by spaces. The inverted index allows for a constant-time (i.e. O(1)) lookup of a phrase within a document. Aside from the performance benefit, an inverted index yields itself nicely to answering questions such the number of occurrences of a phrase or the average distance between occurrences of a phrase within a document. This is because of the structure of an inverted index - by definition, it is a mapping of a terms or phrases to their respective position(s) within a document.

The program operates by parsing a set of command line arguments (run `python phrase_counter.py --help` to see all options) and then invoking a search within an appropriate index file (via index_search()). If indices are unavailable, they're constructed (via build_all_indices). 

As a program option, a linear search (string matching, character by character) can also be conducted in the document. This method (via linear_search()) isn't as fast as the indexed search option, and will run in O(n) time.

## Assumptions and Limitations:
I have assumed a rather simple definition of a phrase. As such, there are phrases in War and Peace that have words that are not separated by spaces, but rather, with ellipses (...) or hyphenations (---). My app does not handle these situations. I've also assumed that the maximum length of phrases we might be interested in for this exercise is five, and therefore preset my index generators to build indexes for phrases of length five.

## Possible Improvements:
Given the scope of this assignment and time constraints, there remain a couple of enhancements that I've contemplated but not got around to implementing. First, the phrase search could also be improved if we allowed words to be 'stemmed' (removal of common endings such as plurals, -ings and more). Second, the indices are persisted using Python's cPickle persistence package. While it provides a really easy to use API, there are probably more sophisticated persistence structures that could be used to speed up index lookups, given the very alphabetical/lexical nature of the queries.