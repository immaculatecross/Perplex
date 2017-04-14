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

def Works (string, constant):
    digit = 0
    upper = 0
    lower = 0
    for i in range (0,12):
        character = string[i+constant*12:i+constant*12+1]
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


    # fix input data hash length (multiple of 16 for plaintext, 32 for key), by adding "0" or truncating

    while len(name)%16 != 0:
        name+="0"

    if len(masterkey)>31:
        masterkey=masterkey[0:32]

    while len(masterkey)<32:
        masterkey+="0"


    # encrypt plain with key and a constant IV ("thisisaninitvect"), then hash ciph1


    obj1=AES.new(masterkey, AES.MODE_CBC, 'thisisaninitvect')
    ciph1 = obj1.encrypt(name)

    m = SHA256.new()
    m.update(ciph1)
    ciph1=m.hexdigest()


    # fix hash length (multiple of 16 for plaintext, exactly 32 for key), by adding "0" or truncating

    while len(website)%16 != 0:
        website+="0"

    if len(ciph1)>31:
        ciph1=ciph1[0:32]

    while len(ciph1)<32:
        ciph1+="0"


    # encrypt website with ciph1 and a constant IV ("thisisaninitvect"), then hash ciph2

    obj=AES.new(ciph1, AES.MODE_CBC, 'thisisaninitvect')
    ciph2=obj.encrypt(website)

    m = SHA256.new()
    m.update(ciph2)
    ciph2=m.hexdigest()


    # convert ciph2 from hexadecimal to decimal, then from decimal to base62

    ciph2 = int(ciph2, 16)

    ciph2 = int2base(ciph2,62,alphabet='0123456789abcdefghijklmnopqrstuvwxyz')


    # Choose the correct interval

    digit = 0
    upper = 0
    lower = 0

    for i in range (0,6):
        if Works (ciph2,i):
            c = i*12
            break
        elif i == 5:
            c=0
            if digit == 0:
                ciph2 = ciph2[0:2]+"0"+ciph2[3:12]
            if upper == 0:
                ciph2 = "P"+ciph2[1:12]
            if lower == 0:
                ciph2 = ciph2[0:1]+"w"+ciph2[2:12]
            break


    # use the following password format: xxx-xxx-xxx-xxx, where x is a base 62 caracter, from the start of ciph2

    password = ciph2[0+c:3+c]+"-"+ciph2[3+c:6+c]+"-"+ciph2[6+c:9+c]+"-"+ciph2[9+c:12+c]

    return password


# input data

name= raw_input ('Enter your full name: ')
masterkey= getpass.getpass ('Enter your master key: ')

while True:
    website= raw_input ('Enter the service domain name: ')
    print "Your password is:", Password (name, masterkey, website)
