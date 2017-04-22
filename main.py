from Crypto.Hash import SHA256
import codecs
import getpass


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


    # combine and hash into ciph

    ciph = name + masterkey + website

    m = SHA256.new()
    m.update(ciph)
    ciph=m.hexdigest()
    #print ciph


    # convert ciph from hexadecimal to base64

    ciph = codecs.encode(codecs.decode(ciph, 'hex'), 'base64').decode()
    ciph = ciph.replace("+", "")
    ciph = ciph.replace("/", "")
    #print ciph
    #print len(ciph)


    # hash and convert for as long as ciph doesn't meet requirements

    while Works(ciph[0:12]) == False:
        #print ciph
        #print len(ciph)
        m = SHA256.new()
        m.update(ciph)
        ciph=m.hexdigest()
        #print ciph
        ciph = codecs.encode(codecs.decode(ciph, 'hex'), 'base64').decode()
        ciph = ciph.replace("+", "")
        ciph = ciph.replace("/", "")
        #print ciph


    # use the following password format: xxx-xxx-xxx-xxx, where x is a base 62 caracter, from the start of ciph

    password = ciph[0:3]+"-"+ciph[3:6]+"-"+ciph[6:9]+"-"+ciph[9:12]

    return password


# input data

name= raw_input ('Enter your full name: ')
masterkey= getpass.getpass ('Enter your master key: ')

while True:
    website= raw_input ('Enter the service domain name: ')
    print "Your password is:", Password (name, masterkey, website)
