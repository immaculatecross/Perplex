from Crypto.Cipher import AES
from Crypto.Hash import SHA256

plain="username"
key="password"
website="site"
print(plain)
print(key)
print(website)

m1 = SHA256.new()
m1.update(plain)
plain=m1.hexdigest()
print(plain)

m2 = SHA256.new()
m2.update(key)
key=m2.hexdigest()
print(key)

m3 = SHA256.new()
m3.update(website)
website=m3.hexdigest()
print(website)

for i in range(0,2):

    while len(plain)%16 != 0:
        plain+="0"

    if len(key)>31:
        key=key[0:31]
    while len(key)<32:
        key+="0"

    obj=AES.new(key, AES.MODE_CBC, 'thisisaninitvect')
    ciph1=obj.encrypt(plain)
    print(plain)
    print(key)
    print(ciph1)
    print(obj.decrypt(ciph1))
    m4 = SHA256.new()
    m4.update(ciph1)
    ciph1=m4.hexdigest()
    print(ciph1)

    if i == 0:
        plain=website
        key=ciph1
    else:
        print("password: "+ciph1)
