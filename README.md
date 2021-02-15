## issue-trees

### motivation
Issues are the basic building block of Jira, and agile software projects are often organised into parent-child hierarchies that look something like this - the "user story" being the standard term for the basic work-unit on Scrum/Kanban boards. 
- EPIC
- - FEATURE
- - - USER STORY
- - - - ACCEPTANCE CRITERION / BUG / CHANGE REQUEST

We want to be able to create snapshots of this "issue tree", stored in a PostgreSQL database. (And one could add automation rules and post functions to issue transitions in Jira to take these snapshots automatically, using a webhook.) On a simple Flask web app, we should then be able to a) visualise snapshots and b) compare previous snapshots with each other, or with the current issue tree, with a "diff" function. 

Currently:
- we can represent issue trees with IssueNode objects
- we can put/pull snapshots of trees to/from the database

### setup + test
Install Python requirements:
```
pip install requirements.txt
```

Install PostgreSQL and start cluster:
```
sudo apt-get install postgresql-12
sudo pg_ctlcluster 12 main start
```

A fresh postgresql-12 install will make a database called "postgres" and a superuser of the same name. To run the tests with the YAML file as-is, first give this superuser a password and then make the required tables:
```
sudo su postgres
psql
ALTER USER postgres WITH PASSWORD 'postgres';
CREATE TABLE snapshots (
  snap_id SERIAL PRIMARY KEY,
  created_on TIMESTAMP NOT NULL
);
CREATE TABLE snap_issues (
  snap_id INT NOT NULL,
  issue_version_id SERIAL PRIMARY KEY,
  parent_issue_version_id INT,
  issue_key VARCHAR(16) NOT NULL,
  CONSTRAINT snap_fk FOREIGN KEY (snap_id) REFERENCES snapshots(snap_id)
);
\q
exit
```

Finally, run test_db.py. At the moment, all this does is make an example issue tree, store it in the database, then "restore" it from the database. Then we print the original and the restored tree to check the put_snap and pull_snap methods are working.
```
python test_db.py
```
