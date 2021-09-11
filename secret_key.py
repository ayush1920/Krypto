import os

def init():
    '''Returns key for JWT token if key.txt file is present. Else creates a key and saves it in key.txt file'''

    filename = "key.txt"
    if os.path.isfile(filename):
        with open(filename) as f:
            key = f.read()
        if key:
            return key

    with open(filename, 'w') as f:
        key =  generate_key()
        f.write(key)
    return key


def generate_key():
    '''Function to generate key for JWT token'''
    return os.urandom(50).hex()
