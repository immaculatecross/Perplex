from Crypto.Cipher import AES
from Crypto.Hash import SHA256

plain="username"
key="password"
website="site.com"
root_key = "00000"

m1 = SHA256.new()
m1.update(key)
key = m1.hexdigest

m2 = SHA256.new()
m2.update(username)
username = m2.hexdigest

m3 = SHA256.new()
m3.update(website)
website = m3.hexdigest

for i in range(0,2):

    while len(plain)%16 != 0:
        plain+="0"

    if len(key)>31:
        key=key[0:32]
    while len(key)<32:
        key+="0"

    obj1=AES.new(key, AES.MODE_CBC, 'thisisaninitvect')
    ciph = obj1.encrypt(plain)

    if i == 0:
        root_key = ciph


for i in range(0,2):

    while len(website)%16 != 0:
        website+="0"

    if len(root_key)>31:
        root_key=root_key[0:32]
    while len(root_key)<32:
        root_key+="0"

    obj=AES.new(root_key, AES.MODE_CBC, 'thisisaninitvect')
    ciph1=obj.encrypt(website)

    m4 = SHA256.new()
    m4.update(ciph1)
    ciph1=m4.hexdigest()

    if i == 0:
        plain=website
        key=ciph1
    #else:
    #    print(ciph1)

lasthexpassword = "P-"+ciph1[0:3]+"-"+ciph1[3:6]+"-"+ciph1[6:9]+"-"+ciph1[9:12]
#print(lasthexpassword)

decimalpass = int(ciph1, 16)
#print(decimalpass)

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

base62pass = int2base(decimalpass,62,alphabet='0123456789abcdefghijklmnopqrstuvwxyz')
#print(base64pass)

lastb62password = base62pass[0:3]+"-"+base62pass[3:6]+"-"+base62pass[6:9]+"-"+base62pass[9:12]
print(lastb62password)
