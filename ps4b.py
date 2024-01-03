# Problem Set 4B
# Name: Tyler Proctor
# Collaborators: N/A
# Time Spent: 3 hours
# Late Days Used: 3

import random

class Message(object):
    def __init__(self, input_text):
        '''
        Initializes a Message object

        input_text (string): the message's text

        a Message object has one attribute:
            the message text
        '''
        # Initializes message text as the input text
        self.message_text = input_text

    def __repr__(self):
        '''
        Returns a human readable representation of the object

        Returns: (string) A representation of the object
        '''
        #DO NOT CHANGE
        return f'''Message('{self.get_text()}')'''

    def get_text(self):
        '''
        Used to access the message text outside of the class

        Returns: (string) the message text
        '''
        return self.message_text
    

    def shift_char(self, char, shift):
        '''
        Used to shift a character as described in the pset handout

        char (string): the single character to shift.
                    ASCII value in the range: 32<=ord(char)<=126
        shift (int): the amount to shift char ASCII value up by

        Returns: (string) the shifted character with ASCII value in the range [32, 126]
        '''
        # find the ASCII value for char
        char_ascii = ord(char)
        # add the shift value
        encryp_char = char_ascii + shift
        # print(encryp_char)
        # continuously check if it is over 126, if so use mod operater to find remainder over 127 and add 32
        while encryp_char > 126:
            encryp_char = (encryp_char % 127) + 32

        # check if it goes below 32, if so relate it to the same number below 126
        while encryp_char < 32:
            encryp_char = 127 + (encryp_char - 32)
        # return final encrypted character
        return chr(encryp_char)

    def apply_pad(self, pad):
        '''
        Used to calculate the ciphertext produced by applying a one time pad to the message text.
        For each character in the text at index i shift that character by
            the amount specified by pad[i]

        pad (list of ints): a list of integers used to encrypt the message text
                        len(pad) == len(the message text)

        Returns: (string) The ciphertext produced using the one time pad
        '''
        # create new string to house the ciphertext that will be returned at end
        cipher_text = ""
        # iterate through index for each character in message 
        for i in range(len(self.message_text)):
            # apply the pad for that index using shift_char
            # add encrypted char to ciphertext string
            cipher_text += self.shift_char(self.get_text()[i], pad[i])
        # return final string
        return cipher_text

class PlaintextMessage(Message):
    def __init__(self, input_text, pad=None):
        '''
        Initializes a PlaintextMessage object.

        input_text (string): the message's text
        pad (list of ints OR None): the pad to encrypt the input_text or None if left empty
            if pad!= None then len(pad) == len(self.input_text)
            save as a COPY

        A PlaintextMessage object inherits from Message. It has three attributes:
            the message text
            the pad (list of integers, determined by pad
                or generated randomly using self.generate_pad() if pad == None)
            the ciphertext (string, input_text encrypted using the pad)
        '''
        super().__init__(input_text)
        # check if pad != None and then either set pad or generate it
        if pad == None:
            self.pad = self.generate_pad()
        else:
            self.pad = pad.copy()
        self.ciphertext = self.get_ciphertext()
        # raise NotImplementedError  # delete this line and replace with your code here

    def __repr__(self):
        '''
        Returns a human readable representation of the object
        DO NOT CHANGE

        Returns: (string) A representation of the object
        '''
        return f'''PlaintextMessage('{self.get_text()}', {self.get_pad()})'''

    def generate_pad(self):
        '''
        Generates a one time pad which can be used to encrypt the message text.

        The pad should be generated as follows:
            Make a new list
            For each character in the message, choose a random number n in the range [0, 110)
            Add n to this new list    

        Returns: (list of integers) the new one time pad
                    len(pad) == len(message text)
        '''
        # make a new list
        pad_list = []
        # random num in range of [0,110) for each char in message and add to list
        for i in range(len(self.message_text)):
            n = random.randint(0, 109)
            pad_list.append(n)
        # return list
        return pad_list
        # raise NotImplementedError  # delete this line and replace with your code here

    def get_pad(self):
        '''
        Used to safely access your one time pad outside of the class

        Returns: (list of integers) a COPY of your pad
        '''
        copy_pad = self.pad.copy()
        return copy_pad

    def get_ciphertext(self):
        '''
        Used to access the ciphertext produced by applying the pad to the message text

        Returns: (string) the ciphertext
        '''
        ciphertext = self.apply_pad(self.get_pad())
        return ciphertext

    def change_pad(self, new_pad):
        '''
        Changes the pad used to encrypt the message text and updates any other
        attributes that are determined by the pad.

        new_pad (list of ints): the new one time pad that should be associated with this message.
            len(new_pad) == len(the message text)
            save as a COPY

        Returns: nothing
        '''
        # store new pad to self.pad
        self.pad = new_pad.copy() 
        # run ciphertext again with new pad
        self.ciphertext = self.apply_pad(self.get_pad())

class EncryptedMessage(Message):
    def __init__(self, input_text):
        '''
        Initializes an EncryptedMessage object

        input_text (string): the ciphertext of the message

        an EncryptedMessage object inherits from Message. It has one attribute:
            the message text (ciphertext)
        '''
        super().__init__(input_text)
        self.ciphertext = input_text

    def __repr__(self):
        '''
        Returns a human readable representation of the object
        DO NOT CHANGE

        Returns: (string) A representation of the object
        '''
        return f'''EncryptedMessage('{self.get_text()}')'''

    def decrypt_message(self, pad):
        '''
        Decrypts the message text that was encrypted with pad as described in the writeup

        pad (list of ints): the new one time pad used to encrypt the message.
            len(pad) == len(the message text)

        Returns: a PlaintextMessage intialized using the decrypted message and the pad
        '''
        # new string to store and return the decoded plain text
        message_text = ""
        # iterate through each character in the cyphertext and apply the negative pad to return back to normal text
        for i in range(len(self.ciphertext)):
            message_text += self.shift_char(self.ciphertext[i], -pad[i])

        return PlaintextMessage(message_text, pad)
