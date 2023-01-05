# To perform a preorder traversal of an N-ary tree in Python, you can use a recursive function that visits each node in the tree in the following order:
#
# Visit the current node.
# Recursively visit the children of the current node, in the order that they appear.

class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children


def preorder(root: Node) -> list:
    # Base case: if the root is None, return an empty list
    if root is None:
        return []

    # Visit the root node
    result = [root.val]
    print(result)
    print("ROOTCHILDREN",root.children)
    # Recursively visit the children of the root
    if root.children is not None:
        for child in root.children:
            print("child", child)
            if child is not None:
                result.extend(preorder(child))

    return result

# Define the N-ary tree
#      1
#    / | \
#   3  2  4
#  / \    | \
# 5   6    7  8
root = Node(1, [Node(3, [Node(5), Node(6)]), Node(2), Node(4, [Node(7), Node(8)])])

# Perform a preorder traversal of the tree
result = preorder(root)

# Print the result
print(result)
