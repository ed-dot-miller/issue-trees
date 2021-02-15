import yaml
from pathlib import Path
from trees import IssueNode
from db import DBConnector
from datetime import datetime

# load config
path_to_config = Path("config.yaml")
with open(path_to_config) as f:
    config = yaml.safe_load(f)


def test_snapshot_methods():
    """Make an example issue tree, store it as a snapshot - then recreate it from
    database with DBConnector.make_tree(), and compare with original"""
    pg = DBConnector(**config['postgres'])

    # make example issues
    epic1 = IssueNode("EPIC-1")
    feat1 = IssueNode("FEAT-1")
    feat2 = IssueNode("FEAT-2")
    story2 = IssueNode("STORY-2")
    story3 = IssueNode("STORY-3")
    story5 = IssueNode("STORY-5")
    bug3 = IssueNode("BUG-3")
    bug4 = IssueNode("BUG-4")
    acc = IssueNode("ACC-1")
    change = IssueNode("CHR-4")

    # make tree, with root 'epic1'
    story2.add_child(bug3)
    story2.add_child(acc)
    story3.add_child(bug4)
    story5.add_child(change)
    feat1.add_child(story2)
    feat1.add_child(story5)
    feat2.add_child(story3)
    epic1.add_child(feat1)
    epic1.add_child(feat2)

    # store this tree as new snapshot
    new_snapshot_id = pg.put_snapshot(epic1, str(datetime.now()))

    # restore from db
    restored_epic1 = pg.pull_snapshot(new_snapshot_id)

    # TO-DO: override IssueNode.__eq__() so we can do
    # assert epic1 == restored_epic1 - for now, can
    # compare visually
    print(epic1)
    print("\n")
    print(restored_epic1)


if __name__ == '__main__':
    test_snapshot_methods()
