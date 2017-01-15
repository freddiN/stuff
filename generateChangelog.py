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
    strChangelog += '\n' + key + ':\n';
    for s in changelist:
      #print ' value:' + s;
      strChangelog += '  ' + s + '\n';
  return strChangelog;

def queryGerrit():
  endpoint = 'https://review.lineageos.org';
  query = '/changes/?q=status:merged%20branch:cm-14.1';
  rest = GerritRestAPI(url=endpoint, auth=None);
  return rest.get(query);

def generateChangelogLine(change):
  line = '%-60s %s  https://review.lineageos.org/#/c/%s' % (change['subject'], change['updated'][:19],  str(change['_number'])); 
  return line;


dic_changes  = defaultdict(list);
dateMin = readDatetimeFromFile();
print 'min date: ' + dateMin;

changes = queryGerrit();
for change in changes:
  #print 'Change: ' + change['project'] + ' ' + change['subject'] + ' ' ;

  if isInvalidDeviceChange(change['project']):
    continue;

  if isInvalidKernelChange(change['project']):
    continue;

  if isInvalidDate(dateMin, change['updated'][:19]):
    continue;

  print 'valid   ' + change['project'];
  dic_changes[change['project']].append(generateChangelogLine(change));

print '------------------------------------';
strChangelog = dictionaryToString(dic_changes);

print 'changes: ' + strChangelog;
writeChangelogFile(strChangelog);
