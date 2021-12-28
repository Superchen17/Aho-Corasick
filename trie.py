from node import Node

class Trie:
  '''Trie

  Attributes
  ----------
  root : Node
    the root node
  counter : int
    a counter used to assign id to states, initialized to 0
  loopupTable : dict [int, Node]
    a map of the state id and its corresponding node object
  
  '''
  def __init__(self):
    self.root = Node(0)
    self.counter = 1
    self.lookupTable = {}

    self.lookupTable[0] = self.root 

  def lookup_with_id(self, stateId):
    '''get a node object by state id

    Parameters
    ----------
    stateId : int
      node state id

    Returns
    -------
    (Node | None)
      Node if corresponding state id exists, or None

    '''
    if stateId in self.lookupTable.keys():
      return self.lookupTable[stateId]
    else:
      return None

  def _add_word(self, word):
    '''add a single word to the trie

    Parameters
    ----------
    word : str
      a word to be added to the trie
    
    '''
    currNode = self.root

    for (i, letter) in enumerate(word):
      if letter not in currNode.nexts.keys(): #* add new node if existing path not exist
        isEnd = True if (i == len(word) - 1) else False
        newNode = Node(
          stateId=self.counter,
          isEnd=isEnd,
          nexts={},
          prevId=currNode.stateId,
          upLink=letter
        )
        currNode.nexts[letter] = newNode
        self.lookupTable[self.counter] = newNode 
        self.counter += 1

      else: #* else update existing path
        currNode.isEnd = True if (i == len(word) - 1) else False

      currNode = currNode.nexts[letter]
  
  def add(self, words):
    '''add a list of words to the trie

    Parameters
    ----------
    words : list[str]
      a list of words to be added to the trie
    
    '''
    for word in words:
      self._add_word(word)

  def compute_fail(self):
    '''compute fail nodes for all nodes in the trie
    
    '''
    visited = [0 for _ in range(self.counter)]
    queue = []

    currNode = self.root
    currNode.failId = None
    visited[currNode.stateId] = 1
    queue.append(currNode)

    while len(queue) != 0:
      currNode = queue.pop(0)

      for child in currNode.nexts.values():
        if visited[child.stateId] == 0:
          visited[child.stateId] = 1

          upLinkNode = self.lookup_with_id(child.prevId)
          failNode = self.lookup_with_id(upLinkNode.failId)

          if failNode == None: #* fail to root if node depth = 1
            child.failId = 0

          else: #* otherwise compute fail node recursively
            while(child.upLink not in failNode.nexts.keys() and failNode.prevId != None):
              failNode = self.lookup_with_id(failNode.failId)

            if child.upLink in failNode.nexts.keys():
              child.failId = failNode.nexts[child.upLink].stateId
            else:
              child.failId = 0

          queue.append(child)
    
    self.root.failId = self.root.stateId

  def reconstruct_word(self, node:Node, index:int):
    '''reconstruct a word when a accepting node is encountered

    Parameters
    ----------
    node : Node
      a trie node
    index : int
      the end position of the a matching substring in the text
    
    '''
    currNode = node
    failNode = self.lookup_with_id(currNode.failId)
    if(failNode.isEnd):
      self.reconstruct_word(failNode, index)

    buffer = ''
    currNode = node
    while(currNode.prevId != None):
      buffer = currNode.upLink + buffer
      currNode = self.lookup_with_id(currNode.prevId)
    print(buffer, 'from position', index - len(buffer) + 1, 'to', index)

  def traverse(self, text):
    '''traverse throught the constructed trie and perform word look up

    Parameters
    ----------
    text : str
      text containing words of interest
    
    '''
    currNode = self.root
    for (i, letter) in enumerate(text):
      if letter in currNode.nexts.keys():
        currNode = currNode.nexts[letter]
        if currNode.isEnd == True:
          self.reconstruct_word(currNode, i)
          if len(currNode.nexts.keys()) == 0:
            currNode = self.lookup_with_id(currNode.failId)
      else:
        currNode = self.lookup_with_id(currNode.failId)

  def display_trie(self):
    '''display relative information of the constructed trie,
    used for debugging purposes
    
    '''
    visited = [0 for _ in range(self.counter)]
    queue = []

    currNode = self.root
    visited[currNode.stateId] = 1
    queue.append(currNode)

    while len(queue) != 0:
      currNode = queue.pop(0)
      print(
        currNode.stateId, 
        list(currNode.nexts.keys()), 
        currNode.prevId,
        currNode.isEnd,
        currNode.failId,
        currNode.upLink
      )

      for child in currNode.nexts.values():
        if visited[child.stateId] == 0:
          visited[child.stateId] = 1
          queue.append(child)

    print()
