## [1] Overview
This project was an assignment in Knowledge Technology taken in 2019 in the University of Melbourne.

Received 18.5/20

This project is to detect lexical blending using similarity by 1) approximate string matching and 2) word vectors
* For Initial system where Jaro-Winkler similarity was used alone:
        refer to initial_system.py (replace the function in detect_blends with this code)
* For the Updated system where Jaro-Winkler similarity was used with word vectors:
	refer to detect_blends.py 


## [2] Result (UPDATED):
* For some record of results, read "result.txt"
* For sample output file, read "output/output_example.txt"


## [3] Requirement:
I used two libraries(pyjarowinkler, gensim).
```bash
pip install pyjarowinkler
pip install gensim
```

## [4] Codes
Dictionary was stored in dictionary in python with a key of each alphabet.
Binary search was used to set start index and end index of where to find element.
In the final code, many of original code was removed from initial system sacrificing correctness to reduce the time that is taken to run the second system below. 


## [5] How it works? see below

**[Initial system - Jaro-Winkler]**
1. The prefix of the candidate which passed the threshold of Jaro-Winkler similarity, 
indexed to (i)th position of the blend word will be stored in (i)th array.

2. The suffix of the candidate which passed the threshold of Jaro-Winkler similarity, 
indexed from (i+1)th position will be compared to (i)th prefix of the candidate 
and update the highest sum of Jaro-Winkler similarity in (i)th array. 

3. When finishing checking one blend word, iterating the array that has index as the position of the blend word characters, 
find the highest sum of Jaro-Winkler similarity.


**[Combined system - Jaro-Winkler and Word vecor Similarity]**
1. Jaro-Winkler similarity is now used only for threshold 
whereas its total sum was critical key to determining blend words in the previous system. 

2. The suffix of the candidate which passed the threshold of Jaro-Winkler similarity 
indexed from (i+1)th position will be compared to prefix of the candidate indexed to (i)th position, 
which also passed the threshold of Jaro-Winkler similarity, to calculate word vector similarity.

3. Comparing the best value per position per word, the best value that pass both Jaro-Winkler and word vector similarity will be returned.
