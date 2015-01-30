# This script shows queries the Jira for Sakai CLE
# finds all the "Awaiting Review" and Not assigned issues
# filters out any of these which are Security issues (since they cannot be safely assigned to just anyone)
# and then filters out any that had already been assigned to one of the Jira Triage group at some point (which may or may not mean the ticket was reviewed, most probably yes).
# What will be left is a pool of new issues from which to assign Jiras for triage

import sys
import xlrd

if ( len(sys.argv) < 3 ): 
    print ("please pass in your Jira user name and password. Thanks. Aborting program.\n")
    sys.exit(1)


from jira.client import JIRA

options = {
    'server': 'https://jira.sakaiproject.org'
}

# I don't like having my password in here. I wonder what a better option would be?
username = sys.argv[1]
password = sys.argv[2]

jira = JIRA(options, basic_auth=(username,password))

# 13710 is the id of the Jira filter I created to show all Awaiting Review and Unassigned Jiras
# The alias name in Jira is called "AR Unassigned older than 30" . The thinking is that *I* should triage
# issues less than 30 days old. maybe?

my_unassigned_filter = jira.filter('14773')

print "Getting up to 1000 Jira issues which are Awaiting review and unassigned."
# run the filter and assign to this new list
list_of_unassigned = jira.search_issues(my_unassigned_filter.jql, 0, 1000)
# we want a set of just the Jira keys
latest_jiras = [one_issue.key for one_issue in list_of_unassigned]
print "Jira issues retrieved."


# This filter is called "AR Security Unassigned older than 30".
# It is the same as the last query with an additional check for issues
# flagged for security
my_unassigned_security = jira.filter('13711')

print "Getting the Jira security issues which are Awaiting review and unassigned."
# run the issue for unassigned security issues
list_of_ua_security = jira.search_issues(my_unassigned_security.jql,0,1000)
# we want a set of just the Jira keys
security_issues = [one_issue.key for one_issue in list_of_ua_security]
print "Security issues retrieved."


print "Removing security issues from pool of issues"
# Do not assign security jiras. Leave them for the security group

# remove security issues from latest issues
for issue in security_issues:
     if issue in latest_jiras:
         latest_jiras.remove(issue)
print "Done removing security issues."

print "Getting the list of assigned issues from the Excel spreadsheet."
file_path = "/Users/nealcaidin/Dropbox/Sakai Foundation/Jira/"
file_name = "jira_issue_assignments_tcc.xls"
book = xlrd.open_workbook(file_path+file_name)

assigned_jiras = []
for sh in book.sheets():
    # go through the range of all rows in each book
    for rx in range(sh.nrows):
         # skip the first row (rx > 0)
         if (rx > 0):
            # if Column C has an entry then the assumption is that the Jira ticket is assigned to whoever
            # is listed in the cell in Column C and row rx. Strip for white space first.
            if ((sh.cell_value(rowx=rx, colx=2)).strip() != ""):
                    # passed the test, so add the Jira number to the list
                    # assumption is that the Jira id is in Column A
                    assigned_jiras.append(sh.cell_value(rowx=rx, colx=0))

print "Got all the assigned issues on the spreadsheet."

print "Remove assigned issues (spreadsheet) from list"
# remove security issues from latest issues
for issue in assigned_jiras:
     if issue in latest_jiras:
         latest_jiras.remove(issue)

print "Issues removed."
print "Sending issues to assign to ready_to_assign.txt"

file_path = "/Users/nealcaidin/Documents/Sakai/JiraPython/"
output = open(file_path + "ready_to_assign.txt", "w")

for issue in latest_jiras:
     print >>output, issue

print "Done."
