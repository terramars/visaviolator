from util import *
import os
import sys

def build_big_name_index(fstats, fviolator):
  statcomps = get_stats_companies(fstats)
  allnames = []
  fv = csv.reader(open(fviolator))
  fv.next()
  for row in fv:
    allnames += map(normalize_name,row[1:3])

  matches = find_similar_names(allnames,statcomps)
  idx = build_name_index(matches)

  fv = csv.reader(open(fviolator))
  fv.next()
  for row in fv:
    trade_name, legal_name = map(normalize_name,row[1:3])
    if legal_name in idx:
      idx[trade_name] = idx[legal_name]
  return idx

def binary_feature(feat):
  feat = float(feat)
  if feat > 0:
    return 1
  return 0

def get_violator_stats(row):
  stats = defaultdict(int) ###city, state, naics description, h1b violations, had violations, bw, had bw, num ee, had ee, cmp, had cmp
  stats['inspection_city'] = row[4]
  stats['inspection_state'] = row[5]
  stats['naics'] = row[8]
  stats['h1b_violations'] = row[16]
  stats['had_h1b_violations'] = binary_feature(row[16])
  stats['back_wages'] = row[17]
  stats['had_back_wages'] = binary_feature(row[17])
  stats['affected_employees'] = row[18]
  stats['had_affected_employees'] = binary_feature(row[18])
  stats['fine'] = row[19]
  stats['had_fine'] = binary_feature(row[19])
  return stats

def combine_data(fstats,fviolator,fout):
  name_idx = build_big_name_index(fstats,fviolator)
  vdata = [i for i in csv.reader(open(fviolator))][1:]
  vheader = sorted(get_violator_stats(vdata[0]).keys())
  statsheader = csv.reader(open(fstats)).next()
  violatorstats = {}
  for row in vdata:
    try:
      violatorstats[name_idx[normalize_name(row[1])]] = get_violator_stats(row)
    except Exception:
      continue
  fs = csv.reader(open(fstats))
  fs.next()
  fout = csv.writer(open(fout,'w'))
  fout.writerow(statsheader + vheader)
  n = 0
  for row in fs:
    try:
      vstats = violatorstats[name_idx[row[0]]]
    except:
      n+=1
      continue
    vrow = [vstats[i] for i in vheader]
    fout.writerow(row + vrow)
  print n


