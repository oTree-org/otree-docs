'''
(Designed for oTree 3.0+)
To run this script:

python pagetimes.py infile.csv outfile.csv

infile.csv should be the name of the "page times" csv file you downloaded from oTree.
The script will create your outfile.csv with an extra column,
showing how much time was spent on each page.

You can modify this script to tabulate other things, e.g. how much time a participant spent on wait pages in total.

'''

from sys import argv
from csv import DictReader, DictWriter

times = {}

with open(argv[1]) as inf, open(argv[2], 'w', newline='') as outf:
    reader = DictReader(inf)
    writer = DictWriter(outf, fieldnames=reader.fieldnames + ['seconds_on_page'])
    writer.writeheader()
    for row in reader:
        pcode = row['participant_code']
        # to learn what Epoch time is, search on Google.
        time = int(row.get('epoch_time_completed') or row.get('epoch_time'))
        last_time = times.get(pcode)
        if last_time:
            delta = time - last_time
        else:
            delta = ''
        row['seconds_on_page'] = delta
        writer.writerow(row)
        times[pcode] = time
