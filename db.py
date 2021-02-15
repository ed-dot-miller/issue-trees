import psycopg2
from trees import IssueNode


class DBConnector:

    def __init__(self, host, port, user, password, dbname):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password,
                                     host=host, port=port)

    def close(self):
        self.conn.close()

    def fetch(self, query: str):
        with self.conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()

        return results

    def put_snapshot(self, issue_tree, date_time):
        with self.conn.cursor() as cur:

            # new entry in 'snapshots' table
            cur.execute(f"INSERT INTO snapshots(created_on) VALUES (\'{date_time}\') RETURNING snap_id")
            new_snap_id = cur.fetchone()[0]

            # new entries in 'snap_issues' table
            insert_tree(cur, issue_tree, new_snap_id)

        self.conn.commit()
        return new_snap_id

    def pull_snapshot(self, snap_id):
        with self.conn.cursor() as cur:

            # grab all issues in this snapshot
            cur.execute(f"""SELECT issue_version_id, parent_issue_version_id, issue_key
                            FROM snap_issues WHERE snap_id={snap_id}
                            ORDER BY parent_issue_version_id""")
            issues = cur.fetchall()

        # ordering by parent ID puts 'NULL' - the root - at the end
        root_issue = issues.pop(-1)

        # make list of tuples (issue ID, parent ID, IssueNode object)
        issues = [(root_issue[0], root_issue[1], IssueNode(root_issue[2]))] +\
                 [(issue[0], issue[1], IssueNode(issue[2])) for issue in issues]

        # for every non-root node C, find its parent P and do P.children.append(C)
        for child in issues[1:]:
            parent_node = [issue for issue in issues if issue[0] == child[1]][0][2]
            parent_node.add_child(child[2])

        # return root IssueNode object
        return issues[0][2]


def insert_one_and_return_id(cur, snap_id, parent_id, issue_key):
    cur.execute(f"""INSERT INTO snap_issues(snap_id, parent_issue_version_id, issue_key)
                            VALUES ({snap_id}, {parent_id}, \'{issue_key}\')
                            RETURNING issue_version_id""")
    return cur.fetchone()[0]


def insert_tree(cur, issue_tree: IssueNode, snap_id, parent_id="NULL"):
    """Recursively parse tree to insert each issue - each row has an issue ID and parent ID"""
    root = issue_tree
    root_id = insert_one_and_return_id(cur, snap_id, parent_id, root.issue_key)
    for child in root.children:
        insert_tree(cur, child, snap_id, root_id)
