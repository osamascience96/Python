import sys
sys.path.append("..")
from Lecture1.SinglyLinkList import Node, LinkedList

class NewNode(Node):
    isVisited = False

def DetectCycle(linkedlist):
    currentNode = linkedlist.head
    currentNode.isVisited = True
    while True:
        # this is where the cycle breaks...
        if currentNode.next.isVisited is True:
            currentNode.next = None
            break
        currentNode = currentNode.next
        currentNode.isVisited = True

nodeOne = NewNode('Osama')
nodeTwo = NewNode('Saad')
nodeThree = NewNode('Jafri')
linkedList = LinkedList()
linkedList.InsertNode(nodeOne)
linkedList.InsertNode(nodeTwo)
linkedList.InsertNode(nodeThree)
nodeThree.next = nodeTwo
DetectCycle(linkedList)
linkedList.printList()

