class Node:
  '''Trie Node

  Attributes
  ----------
  stateId : int
    node id
  isEnd : bool
    1 if the node is an accepting state, otherwise 0
  nexts : dict [str, Node]
    transitions, map next letter to the next state
  prevId : int
    previous state id
  failId : int
    fail state id
  upLink : str
    upstream link letter
  
  '''
  def __init__(
    self, 
    stateId:int, 
    isEnd:bool = False,
    nexts:dict = {},
    prevId:int = None,
    failId:int = None,
    upLink:str = ''
  ):
    self.stateId = stateId
    self.isEnd = isEnd
    self.nexts = nexts
    self.prevId = prevId
    self.failId = failId
    self.upLink = upLink
