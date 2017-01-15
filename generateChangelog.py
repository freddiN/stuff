from pygerrit2.rest import GerritRestAPI
from collections import defaultdict
from datetime import datetime

def readDatetimeFromFile():
  f = open('/home/freddi/changelog_startdate', 'r');
  str = f.readline();
  return str.strip();

def isInvalidDate(dateMin, dateOfChange):
  # TO DO: UTC?
  # 2017-01-15 09:34:37
  #print 'isInvalidDate min=' + dateMin + ' change=' + dateOfChange;
  date_format = "%Y-%m-%d %H:%M:%S";
  min = datetime.strptime(dateMin, date_format)
  change = datetime.strptime(dateOfChange, date_format)
  diff = (min-change).total_seconds();
  #print 'isInvalidDate diff=' + str(diff);
  if diff > 0:
    print 'invalid date min=' + dateMin + ' change=' + dateOfChange;
    return True;
  else:
    return False;

def isInvalidDeviceChange(project):
  if project.find('device') != -1 and project.find('gemini') == -1:
    print 'ignore device ' + project;
    return True;
  else:
    return False;

def isInvalidKernelChange(project):
  if project.find('kernel') != -1 and project.find('msm8996') == -1:
    print 'ignore kernel ' + project;
    return True;
  else:
    return False;

def writeChangelogFile(changelog):
  f = open('/home/freddi/changelog', 'w');
  f.write(changelog);
  f.close();

def dictionaryToString(dictionary):
  strChangelog = '';
  for key, changelist in dictionary.iteritems():
    #print 'key: ' + k;
    strChangelog += key + ':\n';
    for s in changelist:
      #print ' value:' + s;
      strChangelog += '  ' + s + '\n';
  return strChangelog;

def queryGerrit():
  endpoint = 'https://review.lineageos.org';
  query = '/changes/?q=status:merged%20branch:cm-14.1';
  rest = GerritRestAPI(url=endpoint, auth=None);
  return rest.get(query);


dic_changes  = defaultdict(list);
dateMin = readDatetimeFromFile();
print 'min date: ' + dateMin;

changes = queryGerrit();
for change in changes:
  #print 'Change: ' + change['project'] + ' ' + change['subject'] + ' ' ;
  project = change['project'];
  if isInvalidDeviceChange(project):
    continue;

  if isInvalidKernelChange(project):
    continue;

  if isInvalidDate(dateMin, change['updated'][:19]):
    continue;

  print 'ok ' + project;
  dic_changes[change['project']].append(change['subject'] + ' - ' + change['updated'][:19] + ' - ' + change['change_id'][1:]);

print '------------------------------------';
strChangelog = dictionaryToString(dic_changes);

print 'changes: ' + strChangelog;
writeChangelogFile(strChangelog);

