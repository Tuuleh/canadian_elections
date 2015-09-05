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
  for name in appointee_data['CleanNameNoMiddle']:
    # Build an array decoding all of the appointee names and last names from utf-8 into unicode,
    # then convert those into ASCII ignoring errors, because the R output csv was converted into ASCII
    parsed_names.append(("%s %s" % (HumanName(name.decode('utf-8')).first.lower(), 
      HumanName(name.decode('utf-8')).last.lower())).encode('ascii', 'ignore'))
  return parsed_names

def find_donor_appointees(donor_data, appointee_array):
  donor_appointee_ids = []
  for i, donor in enumerate(donor_data['name']):
    if donor in appointee_array:
      print "we have a match with %s" %(donor)
      donor_appointee_ids.append(donor_data['contributor_id'][i])
  return donor_appointee_ids

def write_results(res, csvfile):
  with open(csvfile, "w") as output:
      writer = csv.writer(output, lineterminator='\n')
      for val in res:
          writer.writerow([val]) 

def run(appointees_file, donors_file):
  donor_data = get_file_column(donors_file)
  appointee_array = populate_appointee_array(get_file_column(appointees_file))
  matches = find_donor_appointees(donor_data, appointee_array)
  write_results(matches, 'matches.csv')

appointees = 'appointees.csv'
donors = 'contributor_lookup_table.csv'

if __name__ == "__main__":
    run(appointees, donors)