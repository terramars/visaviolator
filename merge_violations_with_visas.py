import os
import sys
import string
from util import *

def get_violator_names(fviolator):
  violator_names = set()

  fviolator = csv.reader(open(fviolator))
  fviolator.next() ## discard header

  print 'finding violator names'

  for row in fviolator:
    trade_nm,legal_name = row[1:3]
    violator_names.update(map(normalize_name,[trade_nm, legal_name]))

  print 'found %d violator names'%len(violator_names)
  return violator_names

def write_violated_visas(fvisa, fout, matches):
  fvisa = csv.reader(open(fvisa))
  header = fvisa.next()
  fout = csv.writer(open(fout,'wb'))
  fout.writerow(header)
  print 'writing matching visas'

  violated_companies = {}
  for line in fvisa:
    cname = normalize_name(line[7])
    if len(cname)>1 and cname in matches:
      violated_companies[line[7]] = 1
      fout.writerow(line)

  print 'done, %d violators had visas'%len(violated_companies)



if __name__ == '__main__':
  fviolator = sys.argv[1]
  fvisa = sys.argv[2]
  fout = sys.argv[3]

  violator_names = get_violator_names(fviolator)
  write_violated_visas(fvisa, fout, violator_names)
