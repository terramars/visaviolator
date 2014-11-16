import csv
from collections import defaultdict, Counter
import Levenshtein
import string
import re

whitespace_re = re.compile(r'\s')
suffix_re = re.compile(r'INC$|LLC$|INCORPORATED$')
bad_words_re = re.compile(r'GROUP|DISTRICT|CORPORATION|CORP')


def normalize_name(name):
  name = name.upper()
  name = name.translate(string.maketrans("",""), string.punctuation)
  name = whitespace_re.sub(' ',name)
  name = suffix_re.sub('',name)
  name = bad_words_re.sub('',name)
  name = name.strip()
  return name

def count_company_visas(fname, idx = 7):
  company_counts = Counter()
  f = csv.reader(open(fname))
  f.next()
  for row in f:
    name = normalize_name(row[idx])
    company_counts[name]+=1
  return company_counts

def get_stats_companies(fstats):
  fstats = csv.reader(open(fstats))
  fstats.next()
  statcomps = set([i[0] for i in fstats])
  return statcomps

def get_visa_companies(fvisa):
  fvisa = csv.reader(open(fvisa))
  fvisa.next()
  visacomps = [normalize_name(i[7]) for i in fvisa]
  visacomps = set(visacomps)
  return visacomps

def build_name_tree(names):
  idx = defaultdict(list)
  for n in names:
    f = n.split(' ',1)[0]
    idx[f].append(n)
  return idx

def find_similar_names(violator_names, visacomps, thresh=0.7):
  matches = defaultdict(dict)
  i=0
  vindex = build_name_tree(violator_names)
  for c0 in visacomps:
    i+=1
    if i%1000 == 0:
      print i
    c0f = c0.split(' ',1)[0]
    for c1 in vindex[c0f]:
      r = Levenshtein.ratio(c0,c1)
      if r > thresh:
        matches[c0][c1] = r
  return matches

def build_name_index(matches):
  idx = {}
  n=0
  for k,v in matches.iteritems():
    if k in idx:
      i = idx[k]
    else:
      i = n
      n+=1
    idx[k] = i
    for c in v:
      idx[c] = i
  invidx = {}
  for k,v in idx.iteritems():
    if v not in invidx:
      invidx[v] = k
  finalidx = {}
  for k,v in idx.iteritems():
    finalidx[k] = invidx[v]
  return finalidx





