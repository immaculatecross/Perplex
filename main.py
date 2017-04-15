from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import getpass


# convert from decimal to base 62 (def from Stack Overflow, credit to Mark Borgerding)

def int2base(x,b,alphabet='0123456789abcdefghijklmnopqrstuvwxyz'):
    'convert an integer to its string representation in a given base'
    if b<2 or b>len(alphabet):
        if b==62: # assume base64 rather than raise error
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        else:
            raise AssertionError("int2base base out of range")
    if isinstance(x,complex): # return a tuple
        return ( int2base(x.real,b,alphabet) , int2base(x.imag,b,alphabet) )
    if x<=0:
        if x==0:
            return alphabet[0]
        else:
            return  '-' + int2base(-x,b,alphabet)
    # else x is non-negative real
    rets=''
    while x>0:
        x,idx = divmod(x,b)
        rets = alphabet[idx] + rets
    return rets


# check to see if cipher2's sequences contains at least one number, one upper-case letter, and one lower-case letter

def Works (string):
    digit = 0
    upper = 0
    lower = 0
    for i in range (0,12):
        character = string[i:i+1]
        if character.isdigit():
            digit = 1
        elif character.isupper():
            upper = 1
        elif character.islower():
            lower = 1
    if digit == 1 and upper == 1 and lower == 1:
        return True
    else:
        return False


# return the password from the name, the masterkey and the website

def Password (name, masterkey, website):

    # hash input data

    m = SHA256.new()
    m.update(name)
    name=m.hexdigest()

    m = SHA256.new()
    m.update(masterkey)
    masterkey=m.hexdigest()

    m = SHA256.new()
    m.update(website)
    website=m.hexdigest()


    # fix key hash length (must be 32), moreover, plaintext must be a multiple of 16, but a SHA256 hash is always 64 character long

    masterkey=masterkey[0:32]


    # encrypt plain with key and a constant IV ("thisisaninitvect"), then hash ciph1

    obj1=AES.new(masterkey, AES.MODE_CBC, 'thisisaninitvect')
    ciph1 = obj1.encrypt(name)

    m = SHA256.new()
    m.update(ciph1)
    ciph1=m.hexdigest()


    # fix key hash length (must be 32), moreover, plaintext must be a multiple of 16, but a SHA256 hash is always 64 character long

    ciph1=ciph1[0:32]


    # encrypt website with ciph1 and a constant IV ("thisisaninitvect"), then hash ciph2

    obj=AES.new(ciph1, AES.MODE_CBC, 'thisisaninitvect')
    ciph2=obj.encrypt(website)

    m = SHA256.new()
    m.update(ciph2)
    ciph2=m.hexdigest()


    # convert ciph2 from hexadecimal to decimal, then from decimal to base62

    ciph2 = int(ciph2, 16)

    ciph2 = int2base(ciph2,62,alphabet='0123456789abcdefghijklmnopqrstuvwxyz')


    # hash and convert for as long as ciph2 doesn't meet requirements

    while Works(ciph2) == False:
        m = SHA256.new()
        m.update(ciph2)
        ciph2=m.hexdigest()
        ciph2 = int(ciph2, 16)
        ciph2 = int2base(ciph2,62,alphabet='0123456789abcdefghijklmnopqrstuvwxyz')


    # use the following password format: xxx-xxx-xxx-xxx, where x is a base 62 caracter, from the start of ciph2

    password = ciph2[0:3]+"-"+ciph2[3:6]+"-"+ciph2[6:9]+"-"+ciph2[9:12]

    return password


# input data

name= raw_input ('Enter your full name: ')
masterkey= getpass.getpass ('Enter your master key: ')

while True:
    website= raw_input ('Enter the service domain name: ')
    print "Your password is:", Password (name, masterkey, website)
