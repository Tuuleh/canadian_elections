from nameparser import HumanName
import csv

def get_file_column(file):
  file = open(file, 'rb')
  reader=csv.reader(file)
  headers=reader.next()
  column={}
  for header in headers:
    column[header] = []
  for row in reader:
    for h, v in zip(headers, row):
      column[h].append(v)
  file.close()
  return column

def populate_appointee_array(appointee_data):
  parsed_names = []
  for i, name in enumerate(appointee_data['CleanNameNoMiddle']):
    # Build an array decoding all of the appointee names and last names from utf-8 into unicode,
    # then convert those into ASCII ignoring errors, because the R output csv was converted into ASCII
    parsed_name = ("%s %s" % (HumanName(name.decode('utf-8')).first.lower(), 
      HumanName(name.decode('utf-8')).last.lower())).encode('ascii', 'ignore')
    parsed_names.append({
      'organization': appointee_data['Organizations'][i],
      'type': appointee_data['Type'][i],
      'parsed_name': parsed_name,
      'name' : appointee_data['CleanName'][i]
    })
  return parsed_names

def find_donor_appointees(donor_data, appointee_array):
  donor_appointees = []
  for i, appointee in enumerate(appointee_array):
    if appointee['parsed_name'] in donor_data['name']:
      print "we have a match with %s" %(appointee['parsed_name'])
      appointee['contributor_id'] = donor_data['contributor_id'][i]
      donor_appointees.append(appointee)
  return donor_appointees

def write_results(res, csvfile):
# "{'parsed_name': 'kathleen lyons', 'organization': 'Tax Court of Canada', 'contributor_id': '38789', 'type': 'Tax Court of Canada', 'name': 'Kathleen T. Lyons'}"
  with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(res[0].keys())
    for val in res:
      writer.writerow(val.values()) 

def run(appointees_file, donors_file):
  donor_data = get_file_column(donors_file)
  appointee_array = populate_appointee_array(get_file_column(appointees_file))
  matches = find_donor_appointees(donor_data, appointee_array)
  write_results(matches, 'matches.csv')

appointees = 'appointees.csv'
donors = 'contributor_lookup_table.csv'

if __name__ == "__main__":
    run(appointees, donors)