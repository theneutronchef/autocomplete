import sys
import nltk
from nltk.corpus import words

#####################
## Data Structures ##
#####################

class Node():
  def __init__(self, val):
    self.val = val
    self.children = []
    self.is_end = False

  def __str__(self, level=0):
    ret = " "*level+repr(self.val)+"\n"
    for child in self.children:
      ret += child.__str__(level+1)
    return ret

  def addChild(self, child):
    self.children.append(child)

  def setEnd(self):
    self.is_end = True

  def isEnd(self):
    return self.is_end

class Trie():
  def __init__(self, wordlist=None):
    self.root = Node(None)
    self.results = []
    if wordlist:
      for word in wordlist:
        self.addWord(word)
    
  def addWord(self, word):
    curr = self.root
    for i in range(len(word)):
      to_append = True
      for child in curr.children:
        if child.val == word[i]:
	  curr = child
	  to_append = False
	  break
      if to_append:
        new_node = Node(word[i])
        curr.addChild(new_node)
	curr = new_node
      if i == len(word) - 1:
        curr.setEnd()

  def display(self, root):
    curr = root
    print curr
    for child in curr.children:
      self.display(child)

  def exists(self, word):
    curr = self.root
    for c in word:
      to_continue = False
      for child in curr.children:
        if child.val == c:
	  curr = child
	  to_continue = True
      if not to_continue:
        return False
    if curr.children:
      return False
    return True

  def suggest(self, word):
    curr = self.root
    word_root = ''
    for c in word:
      to_continue = False
      for child in curr.children:
        if child.val == c:
	  curr = child
	  word_root += c
	  to_continue = True
      if not to_continue:
        return False
    self.dfs(curr, word_root)
    suggestions = list(self.results)
    self.cleanup()
    return suggestions

  def dfs(self, root, curr):
    if root and root.val and root.isEnd():
      self.results.append(curr)
    for child in root.children:
      self.dfs(child, curr + child.val)

  def cleanup(self):
    self.results = []

###############
## Functions ##
###############

def generateWordlist(filename):
  f = open(filename, 'r')
  wordlist = []
  for line in f:
    wordlist.append(line.strip())
  return wordlist

def createTrie():
  wordlist = words.words()
  return Trie(wordlist)

###########
## Tests ##
###########

def importTest():
  print "Running importTest..."
  testfile = 'test/test.txt'
  t = Trie(generateWordlist(testfile))
  list_a = t.suggest('a')
  list_b = t.suggest('b')
  list_c = t.suggest('c')
  try:
    assert len(list_a) == len(list_b) == len(list_c) == 100
    print 'importTest passed'
    return True
  except:
    print 'importTest failed'
    return False

def runTestSuite():
  test_suite = [importTest]
  failed = 0
  print "Starting Test Suite...\n"
  for test in test_suite:
    if not test():
      failed += 1
  if failed > 0:
    print '\n%d/%d test(s) failed!' % (failed, len(test_suite))
  else:
    print "\nAll tests passed!"

#runTestSuite()

