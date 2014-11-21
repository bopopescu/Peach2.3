
'''
Mutators that modify the data tree structure.

@author: Michael Eddington
@version: $Id$
'''

#
# Copyright (c) Michael Eddington
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in	
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

# Authors:
#   Michael Eddington (mike@phed.org)

# $Id$

import sys, os, time, hashlib
from Peach.mutator import *
from Peach.Engine.common import *

class DataTreeRemoveMutator(Mutator):
	'''
	Remove nodes from data tree.
	'''
	
	def __init__(self, peach, node):
		Mutator.__init__(self)
		
		self.isFinite = True
		
		self.name = "DataTreeRemoveMutator"
		self._peach = peach
		
	def next(self):
		raise MutatorCompleted()
	
	def getCount(self):
		return 1

	def supportedDataElement(e):
		if isinstance(e, DataElement) and e.isMutable:
			return True
		
		return False
	supportedDataElement = staticmethod(supportedDataElement)
	
	def sequencialMutation(self, node):
		self.changedName = node.getFullnameInDataModel()
		node.setValue("")
	
	def randomMutation(self, node, rand):
		self.changedName = node.getFullnameInDataModel()
		node.setValue("")


class DataTreeDuplicateMutator(Mutator):
	'''
	Duplicate a node's value starting at 2x through 50x
	'''
	
	def __init__(self, peach, node):
		Mutator.__init__(self)
		
		self.isFinite = True
		
		self.name = "DataTreeDuplicateMutator"
		self._peach = peach
		
		self._cnt = 2
		self._maxCount = 50
		
	def next(self):
		self._cnt += 1
		if self._cnt > self._maxCount:
			raise MutatorCompleted()
	
	def getCount(self):
		return self._maxCount
	
	def supportedDataElement(e):
		if isinstance(e, DataElement) and e.isMutable:
			return True
		
		return False
	supportedDataElement = staticmethod(supportedDataElement)
	
	def sequencialMutation(self, node):
		self.changedName = node.getFullnameInDataModel()
		node.setValue( node.getValue() * self._cnt )
	
	def randomMutation(self, node, rand):
		self.changedName = node.getFullnameInDataModel()
		count = rand.randint(0, self._cnt)
		node.setValue( node.getValue() * count )


class DataTreeSwapNearNodesMutator(Mutator):
	'''
	Swap two nodes in the data model that
	are near each other.
	
	TODO: Actually move the nodes instead of
	      just the data.
	'''
	
	def __init__(self, peach, node):
		Mutator.__init__(self)
		
		self.isFinite = True
		
		self.name = "DataTreeSwapNearNodesMutator"
		self._peach = peach
	
	def next(self):
		raise MutatorCompleted()
	
	def getCount(self):
		return 1

	def _moveNext(self, currentNode):
			
			# Check if we are top dogM
			if currentNode.parent == None or not isinstance(currentNode.parent, DataElement):
					return None
			
			# Get sibling
			foundCurrent = False
			for node in currentNode.parent:
					if node == currentNode:
							foundCurrent = True
							continue
					
					if foundCurrent and isinstance(node, DataElement):
							return node
			
			# Get sibling of parentM
			return self._moveNext(currentNode.parent)
		
	def _nextNode(self, node):
		nextNode = None
		
		# Walk down node tree
		for child in node._children:
			if isinstance(child, DataElement):
				nextNode = child
				break
		
		# Walk over or up if we can
		if nextNode == None:
			nextNode = self._moveNext(node)  ### <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
		
		return nextNode
	
	def supportedDataElement(e):
		if isinstance(e, DataElement) and e.isMutable:
			return True
		
		return False
	supportedDataElement = staticmethod(supportedDataElement)
	
	def sequencialMutation(self, node):
		self.changedName = node.getFullnameInDataModel()
		nextNode = self._nextNode(node)
		if nextNode != None:
			
			v1 = node.getValue()
			v2 = nextNode.getValue()
			
			node.setValue(v2)
			nextNode.setValue(v1)
	
	def randomMutation(self, node, rand):
		self.changedName = node.getFullnameInDataModel()
		self.sequencialMutation(node)

# end
