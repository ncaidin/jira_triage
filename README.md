jira_triage
===========

Script or scripts to identify issues remaining for triage. 

jira_triage_new_issues.py makes a number of assumptions:

    1) Requires a Jira account at https://jira.sakaiproject.org
    2) Assumes you have access to Security issues. It's okay if you don't because it filters these out anyway, but might need to comment out some code.
    3) Assumes a particular place to write a file with the results - ready_to_assign.txt .  You'll need to update your paths in the file.
    4) It assumes you have a local Excel spreadsheet in which the first column is the Jira Id and the third column (column C) contains the person or institution assigned to review the issue. Note that you can have more than one worksheet in the spreadsheet with this format. It looks through every worksheet in your workbook.

Bigger picture - Gosh it would sure be easier just to assign the person reviewing the issues in Jira. I'm not 100% sure, but I think part of the rationale is that by keeping a spreadsheet it allows me to assign to an institution or arbitrary group like the S2U schools (Spanish Speaking Univeristies) without having to create additional groups in Jira. And it keeps separate issue which are *really* assigned to an individual vs ones that are assigned for triage.

That being said, it still makes sense to me in this moment to review the possibility of managing this in Jira. After all, Jira is a robust database that can definitely handle this sort of thing.

