from util import *
import numpy as np


def group_by_status(visas):
  stati = Counter()
  for visa in visas:
    stati[visa.status] += 1
  return stati

class Visa:

  def __init__(self,row,name_index):
    self.status = row[1]
    #self.submit_date = row[2]
    #self.decision_date = row[3]
    self.visa_class = row[4]
    self.start_date = row[5]
    self.end_date = row[6]
    self.company = name_index[normalize_name(row[7])]
    self.employer_city = row[9]
    self.employer_state = row[10]
    self.soc_code = row[12]
    self.soc_name = row[13]
    self.work_city = row[20]
    self.work_state = row[21]
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
    elif self.wage_unit != 'Year':
      raise Exception('invalid wage unit')
    self.wage_diff = self.wage_upper - self.wage_lower
    self.pw_diff = self.wage_lower - self.pw
    self.full_time = row[18]
    self.total_workers = int(row[19])
    self.naics_code = row[34]

def summary_stats(numbers):
  total = len(numbers)
  numbers = 1.0*np.array(numbers)
  stats = {}
  stats['avg'] = numbers.mean()
  stats['std'] = numbers.std()
  stats['min'] = numbers.min()
  stats['max'] = numbers.max()
  numbers.sort()
  stats['median'] = numbers[total/2]
  stats['q1'] = numbers[total/4]
  stats['q3'] = numbers[total*3/4]
  stats['iqr'] = stats['q3'] - stats['q1']
  return stats

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

def calculate_top_thing(stuff):
  counts = Counter()
  for thing in stuff:
    counts[thing] += 1
  return counts.most_common()[0][0]

def calculate_stats_for_companies(company_visas):
  company_stats = defaultdict(lambda: defaultdict(int))
  for company,visas in company_visas.iteritems():
    total = len(visas)
    company_stats[company]['total_visas'] = total
    company_stats[company]['num_soc'] = len(set([v.soc_code for v in visas]))
    company_stats[company]['num_work_cities'] = len(set([v.work_city for v in visas]))
    company_stats[company]['top_work_state'] = calculate_top_thing([v.work_state for v in visas])
    company_stats[company]['top_soc'] = calculate_top_thing([v.soc_name for v in visas])
    stati = group_by_status(visas)
    for status,count in stati.iteritems():
      company_stats[company]['pct_'+status] = 1.0 * count / total
    num_fulltime = len([v for v in visas if v.full_time == 'Y'])
    company_stats[company]['total_fulltime'] = num_fulltime
    company_stats[company]['pct_fulltime'] = 1.0*num_fulltime / total
    lowers = [v.wage_lower for v in visas]
    uppers = [v.wage_upper for v in visas]
    pws = [v.pw for v in visas]
    pw_diffs = [v.pw_diff for v in visas]
    diffs = [v.wage_diff for v in visas]
    pct_diffs = [1.0*v.wage_diff / v.wage_lower for v in visas]
    pct_pw_diffs = [1.0*v.pw_diff / v.wage_lower for v in visas]
    stats_to_calculate = [('lower',lowers),('upper',uppers),('pw',pws),('pw_diffs',pw_diffs),('wage_range',diffs), \
                          ('pw_diff_pct',pct_pw_diffs),('pct_wage_range',pct_diffs)]
    for key,numbers in stats_to_calculate:
      stats = summary_stats(numbers)
      for k,v in stats.items():
        company_stats[company][key+'_'+k] = v
  return company_stats

def get_stats_keys(stats):
  return sorted(list(set([k for v in stats.values() for k in v])))

def write_company_stats(company_stats, fout):
  header = ['company'] + get_stats_keys(company_stats)
  fout = csv.writer(open(fout,'w'))
  fout.writerow(header)
  for company,stats in company_stats.iteritems():
    row = [company]
    row += [stats[k] for k in header[1:]]
    fout.writerow(row)















