from Crypto.Cipher import AES
from Crypto.Hash import SHA256


# input data

name="name"
masterkey="masterkey"
website="website"


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

print name
print masterkey
print website


# fix input data hash length (multiple of 16 for plaintext, 32 for key), by adding "0" or truncating

while len(name)%16 != 0:
    name+="0"

if len(masterkey)>31:
    masterkey=masterkey[0:32]

while len(masterkey)<32:
    masterkey+="0"

print name
print masterkey


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

print website
print ciph1


# encrypt website with ciph1 and a constant IV ("thisisaninitvect"), then hash ciph2

obj=AES.new(ciph1, AES.MODE_CBC, 'thisisaninitvect')
ciph2=obj.encrypt(website)

m = SHA256.new()
m.update(ciph2)
ciph2=m.hexdigest()

print ciph2


# convert ciph2 from hexadecimal to decimal, then from decimal to base62 (def from Stack Overflow, credit to Mark Borgerding)

ciph2 = int(ciph2, 16)

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

ciph2 = int2base(ciph2,62,alphabet='0123456789abcdefghijklmnopqrstuvwxyz')
print ciph2

password = ciph2[0:3]+"-"+ciph2[3:6]+"-"+ciph2[6:9]+"-"+ciph2[9:12]
print(password)
