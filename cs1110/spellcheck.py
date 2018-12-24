import urllib.request

words = urllib.request.urlopen("http://cs1110.cs.virginia.edu/files/words.txt").read().decode('utf-8')
words = words.lower()

print("Type text; enter a blank line to end.")
user_input = None
while user_input != "":
    user_input = input()
    user_text = user_input.split()
    for word in user_text:
        word = word.strip(".?!,()\"\'")
        if word.lower() not in words:
            print('  MISSPELLED:', word)
