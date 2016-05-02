# This script shows how to use the client in anonymous mode
# against jira.atlassian.com.
import re
import cookielib
import browsercookie

from jira import JIRA

def cookies_extractor():
    cj = browsercookie.load()
    cookies = {}
    for k in cj._cookies:
        for kk in cj._cookies[k]:
            for kkk in cj._cookies[k][kk]:
                if k == "alm.accenture.com" and kk == "/jira/":
                    cookies[kkk] = cj._cookies[k][kk][kkk].value

    ddd = cj._cookies.copy()
    for k in ddd:
        for kk in ddd[k]:
            if k != "alm.accenture.com" and kk != "/jira/":
                cj._cookies.pop(k,None)

    return cj

# By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK
# (see https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details).
# Override this with the options parameter.

kkk = cookies_extractor()

options = {
    'server': 'https://alm.accenture.com/jira',
     'headers':{
        'Host': 'alm.accenture.com/jira',
        'Accept': '*/*',
        'Origin': 'https://alm.accenture.com',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Atlassian-Token': 'nocheck',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Accept-Language': 'en-US,en;q=0.8,ru;q=0.6,uk;q=0.4,tr;q=0.2',
    },
    'verify': False,
    'cookies':kkk
}

jira = JIRA(options=options, cookies_auth="yes")

# Get all projects viewable by anonymous users.
projects = jira.projects()

# Sort available project keys, then return the second, third, and fourth keys.
keys = sorted([project.key for project in projects])[2:5]

# Get an issue.
issue = jira.issue('ASDN-517')

# Find all comments made by Atlassians on this issue.
atl_comments = [comment for comment in issue.fields.comment.comments
                if re.search(r'@atlassian.com$', comment.author.emailAddress)]


