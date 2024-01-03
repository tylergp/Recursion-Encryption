 # Problem Set 4C
# Name: Tyler Proctor
# Collaborators: N/A
# Time Spent: 2 hours
# Late Days Used: 3

import json
from ps4b import PlaintextMessage, EncryptedMessage # Importing your work from Part B

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    # inFile: file
    with open(file_name, 'r') as inFile:
        # wordlist: list of strings
        wordlist = []
        for line in inFile:
            wordlist.extend([word.lower() for word in line.split(' ')])
        return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"").lower()
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story[:-1]

def get_story_pads():
    """
    Returns: pads used to encrypt story. 
    """
    with open('pads.txt') as json_file:
        return json.load(json_file)

WORDLIST_FILENAME = 'words.txt'
### END HELPER CODE ###

def decrypt_message_try_pads(ciphertext, pads):
    '''
    Given a ciphertext and a list of possible pads used to create it, 
    find the pad used to create the ciphertext

    We will consider the pad used to create the ciphertext as the pad 
    that results in a plaintext with the most valid English words

    ciphertext (EncryptedMessage): The ciphertext
    pads (list of lists of ints): A list of pads which might 
        have been used to encrypt the ciphertext

    Returns: (PlaintextMessage) A message with the decrypted ciphertext and the best pad
    '''
    # load words
    realWords = load_words('words.txt')
    # wordCount = []
    # create best_pad and num_words_correct variables to be used in each iteration
    best_pad = []
    best_pad_score = 0
    # defined as the number of words it got right

    # iterate through pads
    for pad in pads:
        pad_score = 0
        # for each possible pad, run it against the ciphertext to decode
        decoded = ciphertext.decrypt_message(pad)
        # use decoded text from decode to create list of words within and count number of real words
        decoded_text = decoded.get_text()
        for word in decoded_text.split():
            if is_word(realWords, word):
                pad_score += 1

        # check if for this pad, the number of correct words is higher or equal to (in case of ties) than the best one so far
        if pad_score >= best_pad_score:
            # update best_pad_score and best_pad with the most recent pad and its score
            best_pad_score = pad_score
            best_pad.clear()
            best_pad = pad[:]
    
    # print(best_pad)
    Plain_text = ciphertext.decrypt_message(best_pad)
    return Plain_text
         
    # raise NotImplementedError  # delete this line and replace with your code here

def decode_story():
    '''
    Write your code here to decode Bob's story using a list of possible pads
    Hint: use the helper functions get_story_string and get_story_pads and your EncryptedMessage class.

    Returns: (string) the decoded story

    '''
    # store the encrypted story string and the possible pads
    encrypted_story = EncryptedMessage(get_story_string())
    possible_pads = get_story_pads()
    # run them through the decrypt_message_try_pads function to find the best pad and PlaintextMessage object
    decrypted_story = decrypt_message_try_pads(encrypted_story, possible_pads)
    # return the string of the decoded story
    return decrypted_story.get_text()
    # raise NotImplementedError  # delete this line and replace with your code here

if __name__ == '__main__':
    # Uncomment these lines to try running decode_story()
    story = decode_story()
    print("Decoded story: ", story)

    # Personal Test #1: Check encoding for an all uppercase string with punctuation at the end.
    plaintext = PlaintextMessage('RUN!!', [3, 2, 1, 0, 4])
    print('Expected Output: UWO!%')
    print('Actual Output:', plaintext.get_ciphertext())

    # Personal Test #2: Check encoding for an all special characters string with two spaces.
    plaintext = PlaintextMessage('6# &() ', [4, 2, 3, 0, 5, 2, 8])
    print('Expected Output: :%#&-+(')
    print('Actual Output:', plaintext.get_ciphertext())

    # Personal Test #3: Check decoding for an all upercase string with punctuation at the end.
    encrypted = EncryptedMessage('UWO!%')
    print('Expected Output: RUN!!')
    print('Actual Output:', encrypted.decrypt_message([3, 2, 1, 0, 4]).get_text())

    # Personal Test #4: Check decoding for an all special characters string with two spaces.
    encrypted = EncryptedMessage(':%#&-+(')
    print('Expected Output: 6# &() ')
    print('Actual Output:', encrypted.decrypt_message([4, 2, 3, 0, 5, 2, 8]).get_text())
