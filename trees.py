import re
# from jira import JIRA


class IssueNode(object):
    """Represent a single Jira issue as a tree node"""

    def __init__(self, issue_key: str, children=None, jira=None):
        self.jira = jira

        # e.g. EPIC-3, FEAT-5
        self.issue_key = issue_key

        # e.g. EPIC, FEAT
        self.issue_type = re.match("([A-Z]+)-[0-9]+", issue_key).group(1)

        self.children = []
        if children:
            for child in children:
                self.add_child(child)

    def __repr__(self, depth=0):
        """Hierarchical string representation of this node and all its descendants"""
        tree_repr = "  "*depth + " - " + f"{self.issue_key}"
        for child in self.children:
            tree_repr += f"\n{child.__repr__(depth+1)}"

        return tree_repr

    def add_child(self, node):
        if not isinstance(node, IssueNode):
            raise TypeError("'node' is not an IssueNode object")

        else:
            self.children.append(node)

    def find_descendants(self):
        """Feed a JQL (Jira Query Language) statement to the Jira REST API to
        search the instance and "fill the tree" below this node, recursively"""
        children_issues = self.jira.search_issues(f"\"Parent\" = {self.issue_key}")

        if children_issues:
            for child_key in children_issues.keys():
                new_child_node = IssueNode(child_key)
                new_child_node.find_descendants()
                self.add_child(new_child_node)
