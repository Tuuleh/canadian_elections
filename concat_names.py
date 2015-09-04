from nameparser import HumanName
import csv
f = open('appointees.csv', 'rb')
reader = csv.reader(f)
headers = reader.next()
print headers
column = {}
for header in headers:
  column[header] = []
for row in reader:
  for h, v in zip(headers, row):
    column[h].append(v)
for appointee in column['CleanNameNoMiddle']:
  print "%s %s" % (HumanName(appointee.decode('utf-8')).first.lower(), HumanName(appointee.decode('utf-8')).last.lower())
