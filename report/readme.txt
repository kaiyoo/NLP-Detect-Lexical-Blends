I used two libraries(pyjarowinkler, gensim). To run, open terminal execute the folling command:
>> pip install pyjarowinkler
>> pip install gensim

Source codes will be uploaded to my github by 16/09/2019 midnight:
https://github.com/rubyyoo
I will put all the codes into a single file so that if you are interested, you can easily copy and past in your editor and run.

Dictionary was stored in dictionary in python with a key of each alphabet
Binary search was used to set start index and end index of where to find element.
In the final code, many of original code was removed from initial system sacrificing correctness to reduce the time that is taken to run the second system below. 


How it works? see below

[Initial system - Jaro-Winkler]
1. The prefix of the candidate which passed the threshold of Jaro-Winkler similarity, 
indexed to (i)th position of the blend word will be stored in (i)th array.

2. The suffix of the candidate which passed the threshold of Jaro-Winkler similarity, 
indexed from (i+1)th position will be compared to (i)th prefix of the candidate 
and update the highest sum of Jaro-Winkler similarity in (i)th array. 

3. When finishing checking one blend word, iterating the array that has index as the position of the blend word characters, 
find the highest sum of Jaro-Winkler similarity.



[Combined system - Jaro-Winkler and Word vecor Similarity]
1. Jaro-Winkler similarity is now used only for threshold 
whereas its total sum was critical key to determining blend words in the previous system. 

2. The suffix of the candidate which passed the threshold of Jaro-Winkler similarity 
indexed from (i+1)th position will be compared to prefix of the candidate indexed to (i)th position, 
which also passed the threshold of Jaro-Winkler similarity, to calculate word vector similarity.

3. Comparing the best value per position per word, the best value that pass both Jaro-Winkler and word vector similarity will be returned.