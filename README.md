# GA Dev Code Challenge

## Prompt:
Using a language of your choice write a program which takes in the input of a plaintext data file and a search string. The program returns both a count of the times the string appears in the file and the average number of words between each instance of the search string.
Run the program using this sample input file of War and Peace in text version using the search string: peace.

## Output:
    Searching for 'peace' in pg2600_1.idx
    113 occurances of 'peace' in 'pg2600.txt'
    Word positions: [7, 58, 89, 96, 3125, 9174, 26693, 36845, 38709, 39368, 46056, 64552, 68691, 68694, 71694, 72925, 74461, 74504, 75059, 115163, 120934, 126568, 132594, 144941, 156765, 161668, 174587, 175193, 178192, 179165, 185658, 186559, 189249, 189263, 201496, 217929, 217937, 217944, 224508, 246272, 249808, 249889, 251120, 252710, 274081, 278370, 278433, 278803, 281136, 281370, 281678, 284521, 284682, 284845, 285203, 285298, 285353, 285685, 285977, 291791, 291834, 292259, 296545, 304871, 304897, 306194, 307545, 311062, 311275, 319168, 319513, 325966, 325973, 326087, 326383, 326528, 326712, 331746, 331756, 334436, 344503, 344522, 344579, 356001, 391085, 403884, 403921, 423524, 434407, 438201, 440397, 441530, 457454, 462514, 463211, 467638, 468165, 471523, 471566, 501907, 501914, 508057, 508068, 508084, 525960, 526839, 532071, 540018, 543016, 544019, 546144, 562540, 562553]
    Avg word distance: 281457

    ...

    Most popular 3-length phrases (from pg2600_3.idx)
    [('as soon as', 135), ('that he was', 144), ('out of the', 164), ('one of the', 164)]

## Solution:
I solved this by building an app that generates a series of inverted indices of phrases found in the source document. I consider a phrase to be a series of words separated by spaces. The inverted index allows for a constant-time (i.e. O(1)) lookup of a phrase within a document. Aside from the performance benefit, an inverted index yields itself nicely to answering questions such the number of occurrences of a phrase or the average distance between occurrences of a phrase within a document. This is because of the structure of an inverted index - by definition, it is a mapping of a terms or phrases to their respective position(s) within a document.

The program operates by parsing a set of command line arguments (run `python phrase_counter.py --help` to see all options) and then invoking a search within an appropriate index file (via index_search()). If indices are unavailable, they're constructed (via build_all_indices). 

As a program option, a linear search (string matching, character by character) can also be conducted in the document. This method (via linear_search()) isn't as fast as the indexed search option, and will run in O(n) time.

## Assumptions and Limitations:
I have assumed a rather simple definition of a phrase. As such, there are phrases in War and Peace that have words that are not separated by spaces, but rather, with ellipses (...) or hyphenations (---). My app does not handle these situations. I've also assumed that the maximum length of phrases we might be interested in for this exercise is five, and therefore preset my index generators to build indexes for phrases of length five.

## Possible Improvements:
Given the scope of this assignment and time constraints, there remain a couple of enhancements that I've contemplated but not got around to implementing. First, the phrase search could also be improved if we allowed words to be 'stemmed' (removal of common endings such as plurals, -ings and more). Second, the indices are persisted using Python's cPickle persistence package. While it provides a really easy to use API, there are probably more sophisticated persistence structures that could be used to speed up index lookups, given the very alphabetical/lexical nature of the queries.