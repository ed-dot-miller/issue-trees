## issue-trees

### motivation
"Issues" are the basic building block of Jira, and Agile development projects are often organised into parent-child hierarchies that look something like this - the "user story" being the standard term for the basic work-unit on Scrum/Kanban boards. 
- EPIC
- - FEATURE
- - - USER STORY
- - - - ACCEPTANCE CRITERIA / BUG

We want to enable the user to create snapshots of this "issue tree" - and they could add automation rules and post functions to issue transitions in Jira to take these snapshots automatically. On a simple Flask web app, they should then be able to a) visualise snapshots and b) compare previous snapshots with each other, or with the current issue tree, with a "diff" function. This repo is really a simplified model of a real project: there's no real Jira instance to grab issues from, so there are a few stubs. The snapshots are stored in a PostgreSQL database running locally. 
