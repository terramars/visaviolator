import os
import sys
import csv
import Levenshtein

def get_violator_names(fviolator):
  violator_names = set()

  fviolator = csv.reader(open(fviolator))
  fviolator.next() ## discard header

  print 'finding violator names'

  for row in fviolator:
    trade_nm,legal_name = row[1:3]
    violator_names.update([trade_nm, legal_name])

  print 'found %d violator names'%len(violator_names)
  return violator_names

def get_visa_companies(fvisa):
  fvisa = csv.reader(open(fvisa))
  fvisa.next()
  visacomps = [i[7] for i in fvisa]
  visacomps = set(visacomps)
  return visacomps

def find_similar_names(violator_names, visacomps):
  matches = defaultdict(dict)
  for c0 in visacomps:
    for c1 in violator_names:
      r = Levenshtein.ratio(c0,c1)
      if r > 0.7:
        matches[c0][c1] = r
  return matches

def write_violated_visas(fvisa, fout, violator_names):
  fvisa = csv.reader(open(fvisa))
  header = fvisa.next()
  fout = csv.writer(open(fout,'wb'))
  fout.writerow(header)
  print 'writing matching visas'
  violated_companies = {}

  for line in fvisa:
    if line[7] in violator_names:
      violated_companies[line[7]] = 1
      fout.writerow(line)

  print 'done, %d violators had visas'%len(violated_companies)

if __name__ == '__main__':
  fviolator = sys.argv[1]
  fvisa = sys.argv[2]
  fout = sys.argv[3]

  violator_names = get_violator_names(fviolator)
  write_violated_visas(fvisa, fout, violator_names)
