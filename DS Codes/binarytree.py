# Binary Tree Level Order Traversal

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def levelOrder(root: TreeNode) -> list[list[int]]:
    # Base case: if the root is None, return an empty list
    if root is None:
        return []

    # Initialize the queue with the root node
    queue = [root]
    # Initialize the result list
    result = []

    # Iterate through the queue
    while queue:
        # Get the size of the queue
        size = len(queue)
        # Initialize the level list
        level = []

        # Iterate through the nodes in the current level
        for _ in range(size):
            # Remove the front node from the queue
            node = queue.pop(0)
            # Add the value of the node to the level list
            level.append(node.val)
            # Add the children of the node to the queue
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        # Add the level list to the result
        result.append(level)

    return result

# Define the binary tree
#      3
#    /   \
#   9     20
#  / \   /  \
# 15 7  8   9
root = TreeNode(3, TreeNode(9, TreeNode(15), TreeNode(7)), TreeNode(20, TreeNode(8), TreeNode(9)))

# Perform a level order traversal of the tree
result = levelOrder(root)

# Print the result
for level in result:
    print(level)

