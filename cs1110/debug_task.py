'''
This program reads text files
(such as might be downloaded from http://www.gutenberg.org/ebooks/13)
and reports pairs of words that appear together with unusually high probability.

This program relies on two global dicts:

    master_list[word1][word2]
        is the number of times word1 and word2 appear together

    frequencies[word1]
        is the number of times word1 appears
'''



def phrases(etext):
    '''returns a list of "phrases", which is text separated by lines or sentence-terminating punctuation.
    Implemented by replacing all such terminators with "." and using split(".").'''
    etext.replace('\n', '.')
    etext.replace('!', '.')
    etext.replace('?', '.')
    return etext.split('.')


def words(phrase):
    '''Finds the words in a phrase and returns them.
    Removes any multi-letter all-caps words; lower-cases all other words.
    Removes word-boundary punctuation other than apostrophes.'''
    raw_words = phrase.split()
    answer = []
    for word in raw_words:
        if word != word.upper():
            word = word.lower()
            word = word.strip(',;:-"[](){}<>/“”‘’_*') # this line contains no bugs
            if len(word) > 0:
                answer.append(word)
    return answer

def populate_list(etext):
    '''Adds the frequencies from one text to the master_list'''
    global master_list, frequencies

    master_list = {}  
    frequencies = {}

    for phrase in phrases(etext):
        for word1 in words(phrase):
            if word1 in frequencies:
                frequencies[word1] += 1
            else:
                frequencies[word1] = 1
            for word2 in words(phrase):
                if word1 == word2:
                    continue
                if word1 not in master_list:
                    master_list[word1] = {word2:1}
                elif word2 not in master_list[word1]:
                    master_list[word1][word2] = 1
                else:
                    master_list[word1][word2] += 1


def most_commonly_with(target):
    '''Returns the words that is most often associated with the given word.
    Association is determined by (times together) / (times alone + fuzz)
    The +fuzz is a hack to prevent overly rare words from being the answer too often'''
    global master_list, frequencies
    
    counts = master_list[target]
    words = list(counts.keys())
    
    def bycount(e):
        '''A sort-by function for use in the key= argument of the sort function;
        should put the most-frequent word in the last place,
        where we measure frequency_together / frequency_apart,
        where frequency_apart is the sum of the frequency of each word.
                
        The idea of a key function is "sort as if the values were the results of this function";
        for example, sort(key=abs) puts -3 after 2 and before 4'''
        return counts[e]/frequencies[e] + frequencies[target]
    
    words.sort(key=bycount) # this line contains no bugs
    return words[-1]
        

### The following code uses the above methods; code below this line does not contain bugs

text = open('snark.txt').read()
populate_list(text)

text = open('alice.txt').read()
populate_list(text)

# At this point we've populated the global master_list and frequencies dicts,
# which will be used in all future code

word = input('What word are you interested in? ')
while len(word) > 0:
    word = word.lower()
    result = most_commonly_with(word)
    if result is not None:
        print('"'+word+'"', 'often appears with', '"'+result+'"')
    else:
        print('"'+word+'"', 'does not appear in our corpus')
    print()
    word = input('What word are you interested in? ')

