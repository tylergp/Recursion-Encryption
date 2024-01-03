# Problem Set 4a
# Name: Tyler Proctor
# Collaborators: N/A
# Time spent: 2 hours 30 mins

from tree import Node  # Imports the Node object used to construct trees

# Part A0: Data representation
# Fill out the following variables correctly.
# If correct, the tests named data_representation should pass.
tree_1 = Node(9, Node(6), Node(3, Node(7), Node(8))) 
tree_2 = Node(7, Node(13, Node(15, Node(4), Node(6)), Node(5)), Node(2, Node(9), Node(11)))
tree_3 = Node(4, Node(9, Node(14), Node(25)), Node(17, Node(1), Node(8, Node(11), Node(6))))

def find_tree_height(tree):
    '''
    Find the height of the given tree
    Input:
        tree: An element of type Node constructing a tree
    Output:
        The integer depth of the tree
    '''
    # Base case:
    if tree == None:
        return -1
        # have to remove one at the end to account for recursion adding one for the next layer each time
    # Recursive case:
    # For tree, find height of two subtrees (right and left) using recursion

    sub_right_h = find_tree_height(tree.get_right_child())
    sub_left_h = find_tree_height(tree.get_left_child())
    # Compare right and left to see which height is bigger (aka the max)
    #return that value + 1
    if sub_right_h > sub_left_h:
        return sub_right_h + 1
    else: 
        return sub_left_h + 1

def is_heap(tree, compare_func):
    '''
    Determines if the tree is a max or min heap depending on compare_func
    Inputs:
        tree: An element of type Node constructing a tree compare_func: 
              a function that compares the child node value to the parent node value
            
            i.e. compare_func(child_value,parent_value) for a max heap would return False 
                 if child_value > parent_value and True otherwise
                 
                 compare_func(child_value,parent_value) for a min meap would return False 
                 if child_value < parent_value and True otherwise
    Output:
        True if the entire tree satisfies the compare_func function; False otherwise
    '''
    # NOTE: compare_func tells us if tree passed in could be a potential max or min heap based on the child and parent
    # Base case:
    # Check if tree has no branches, and therefore is a heap
    if tree == None:
        return True
    
    # Store values for left and right childs of tree to utilize for each possible scenario of branches
    left_branch = tree.get_left_child()
    right_branch = tree.get_right_child()

    # Check if tree has both a branch on the right and left sides
    if right_branch != None and left_branch != None:
        # Check if both branches are a max or min heap
        if compare_func(right_branch.get_value(), tree.get_value()) and compare_func(left_branch.get_value(), tree.get_value()):
            # recurse through next branches for if they are also max or min heaps and return result
            return is_heap(right_branch, compare_func) and is_heap(left_branch, compare_func)
        else:
            return False
        
    # Check if tree has no branch on right and only on left side
    if right_branch == None and left_branch != None:
        # Check if left branch is a heap of either max or min using compare_func
        if compare_func(left_branch.get_value(), tree.get_value()):
            # recurse through left child branch for if also a max or min heap and return result
            return is_heap(left_branch, compare_func)
        else:
            # left branch not a max or min heap
            return False
        
    # Check if tree has no branch on left and only on right side
    if right_branch != None and left_branch == None:
        # Check if right branch is a heap for either max or min using compare_func
        if compare_func(right_branch.get_value(), tree.get_value()):
            # check if child right branch is also a heap and return result
            return is_heap(right_branch, compare_func)
        else:
            # right branch not a heap
            return False
    return True

if __name__ == '__main__':
    # # You can use this part for your own testing and debugging purposes.
    # # IMPORTANT: Do not erase the pass statement below if you do not add your own code
    print(find_tree_height(tree_1))
    print(find_tree_height(tree_2))
    print(find_tree_height(tree_3))

    # pass