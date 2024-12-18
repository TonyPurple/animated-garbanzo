import hashlib

String = str(input("Type out the word you would like to hash "))
Hash_Type = str(input("Type your prefered hash type. SHA or MD5"))

if Hash_Type == "SHA":
	Final_Hash = hashlib.sha256(String.encode()).hexdigest()
elif Hash_Type == "MD5":
	Final_Hash = hashlib.md5(String.encode()).hexdigest()
else:
	Final_Hash = "Invalid hash type"

print(Final_Hash)
