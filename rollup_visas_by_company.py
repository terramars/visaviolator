from util import *
import numpy as np

def summary_stats(numbers):
  numbers = np.array(numbers)
  stats = {}
  stats['total'] = numbers.size
  stats['avg'] = numbers.mean()
  stats['std'] = numbers.std()
  stats['lower'] = numbers.min()
  stats['upper'] = numbers.max()
  numbers.sort()
  stats['median'] = numbers[total/2]
  stats['q1'] = numbers[total/4]
  stats['q3'] = numbers[total*3/4]
  stats['iqr'] = stats['q3'] - stats['q1']
  return stats

class Visa:

  def __init__(self,row,name_index):
    self.status = row[1]
    self.submit_date = row[2]
    self.decision_date = row[3]
    self.visa_class = row[4]
    self.start_date = row[5]
    self.end_date = row[6]
    self.company = name_index[normalize_name(row[7])]
    self.city = row[9]
    self.state = row[10]
    self.soc_code = row[12]
    self.soc_name = row[13]
    self.wage_unit = row[17]
    self.wage_lower = float(row[15])
    self.wage_upper = float(row[16])
    self.pw = float(row[22])
    if self.wage_unit=='Hour':
      self.wage_lower *= 40*52
      self.wage_upper *= 40*52
      self.pw *= 40*52
    elif self.wage_unit == 'Week':
      self.wage_lower *= 52
      self.wage_upper *= 52
      self.pw *= 40*52
    self.wage_diff = self.wage_upper - self.wage_lower
    self.full_time = row[18]
    self.total_workers = int(row[19])
    self.naics_code = row[34]

def group_visas_by_company(fvisa):
  cnames = get_visa_companies(fvisa)
  matches = find_similar_names(cnames,cnames,0.92)
  name_index = build_name_index(matches)
  fvisa = csv.reader(open(fvisa))
  fvisa.next()
  visas = defaultdict(list)
  for row in fvisa:
    try:
      visa = Visa(row,name_index)
    except Exception:
      continue
    if len(visa.company) > 1:
      visas[visa.company].append(visa)
  return visas

def calculate_stats_for_companies(visas):
  pass















