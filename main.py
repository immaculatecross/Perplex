from Crypto.Hash import SHA256
import codecs
import getpass

# encrypt with SHA-256, turn into base 64, and remove unwanted characters
def Encrypt (string):
    # hash using SHA-256
    m = SHA256.new()
    m.update(string)
    string=m.hexdigest()
    # turn into base 64
    string = codecs.encode(codecs.decode(string, 'hex'), 'base64').decode()
    # remove unwanted characters
    string = string.replace("+", "")
    string = string.replace("/", "")
    return string

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
    # combine input data into ciph
    ciph = name + masterkey + website
    # encrypt with SHA-256, turn into base 64, and remove unwanted characters
    ciph = Encrypt (ciph)
    # hash and convert for as long as ciph doesn't meet requirements
    while Works(ciph) == False:
        ciph = Encrypt (ciph)
    # use the following password format: xxx-xxx-xxx-xxx, where x is a base 62 caracter, from the start of ciph
    password = ciph[0:3]+"-"+ciph[3:6]+"-"+ciph[6:9]+"-"+ciph[9:12]
    return password

# input data
name= raw_input ('Enter your full name: ')
masterkey= getpass.getpass ('Enter your master key: ')
# infinite loop to prompt for website
while True:
    website= raw_input ('Enter the service domain name: ')
    print "Your password is:", Password (name, masterkey, website)
