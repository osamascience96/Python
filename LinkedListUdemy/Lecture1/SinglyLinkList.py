class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def InsertHead(self, headNode):
        if self.head is None:
            self.InsertNode(headNode)
        else:
            tempNode = self.head
            self.head = headNode
            self.head.next = tempNode
            # delete the tempNode pointing to the previous head node
            del tempNode

    def lengthOfList(self):
        length = 0
        currentNode = self.head
        while currentNode.next is not None:
            currentNode = currentNode.next
            length +=1
        return length
    
    def InsertAt(self, node, position):
        if position < 0 or position > self.lengthOfList():
            print("Invalid Position")
        else:
            if position == 0:
                # if the position is zero then,
                self.InsertHead(node)
            else:
                currentNode = self.head
                previousNode = None
                for i in range(position):
                    previousNode = currentNode
                    currentNode = currentNode.next
                
                node.next = currentNode
                previousNode.next = node
    
    def DeleteAt(self, position):
        if position < 0 or position >self.lengthOfList():
            print("Invalid Position")
        else:
            if position == 0:
                self.deleteHead()
            else:
                tempNode = self.head
                previousNode = None
                for x in range(position):
                    previousNode = tempNode
                    tempNode = tempNode.next
                
                # deref the nextNode of the previous one and this(current) node 
                previousNode.next = tempNode.next
                tempNode.next = None
                del tempNode
    
    def deleteEnd(self):
        currentNode = self.head
        previousNode = None
        while currentNode.next is not None:
            previousNode = currentNode
            currentNode = currentNode.next
        previousNode.next = None
    
    def deleteHead(self):
        tempNode = self.head
        # set the head value 
        self.head = self.head.next

        # deref the previous head to the nextnode
        tempNode.next = None
        # deleted the pointer as well, optional(also done automatically when the function is ended)
        del tempNode

    
    def InsertNode(self, newNode):
        # check if the headnode is null, 
        if self.head is None:
            self.head = newNode
        else:
            # traverse to the last node until next node is not null
            lastNode = self.head
            while lastNode.next is not None:
                lastNode = lastNode.next
            
            #init the newnode to the latest node 
            lastNode.next = newNode
    
    def printList(self):
        if self.head is None:
            print("List is Empty")
            return
        
        currentNode = self.head
        while currentNode is not None:
            print(currentNode.data)
            currentNode = currentNode.next

if (__name__ == "__main__"):
    linklist = LinkedList()

    # creating some nodes 
    firstNode = Node("Osama")
    secondNode = Node("you")
    thirdNode = Node("will")
    fourthNode = Node("be")
    fifthNode = Node("Single")
    sixthNode = Node("Forever")

    # passing all the nodes one by one to the function
    linklist.InsertNode(firstNode)
    linklist.InsertNode(secondNode)
    linklist.InsertNode(thirdNode)
    linklist.InsertNode(fourthNode)
    linklist.InsertNode(fifthNode)
    linklist.InsertNode(sixthNode)

    # insert the new node to the beginning
    headNode = Node("Hey!")
    linklist.InsertHead(headNode)

    # Insert the data at position
    dataNode = Node("Ahmed")
    linklist.InsertAt(dataNode, 2) 

    # delete the last node
    linklist.deleteEnd()
    # delte the head node
    linklist.deleteHead()

    # delete the node at position x
    linklist.DeleteAt(2)

    # print the list 
    linklist.printList()