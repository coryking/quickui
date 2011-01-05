from collections import deque

class DependencyMap():
    '''
    A map that tracks which items are dependent upon which other item(s).
    Calling DependencyMap.add(A, B) indicates that A depends on B.
    Each item can only be directly dependent upon a single other item, which may
    or may not itself appear in the map.
    
    Note that we can't use a dictionary as a base class, because we want the
    order of keys to be stable; i.e., they should reflect the order in which the
    entries were added.
    '''
    def __init__(self, entries=[]):
        self.map = []
        for (key, value) in entries:
            self.add(key, value)

    def add(self, key, value):
        '''
        Add an entry to indicate that key depends on value.
        '''
        self.map.append((key, value))
        
    def sort(self):
        '''
        Return the keys in order such that each key comes after all items it depends upon.
        '''
        keys = [key for (key, value) in self.map]   # Original set of keys.
        unsorted = deque(self.map)                  # Entries not yet sorted.
        sorted_keys = [];                           # Keys already sorted.

        # Each pass through the map should sort at least one item.
        # This gives us a maximum number of passes as n*(n+1) / 2.
        max_pass = (len(self.map) * (len(self.map) + 1)) // 2
        for i in range(max_pass):
            # On each pass, we pull out anything that has no dependencies,
            # is depend on an item which has already been sorted, or is
            # dependent on something not in this map.
            entry = unsorted.popleft()
            (key, value) = entry
            if value == None or value in sorted_keys or value not in keys:
                sorted_keys.append(key)
                if len(unsorted) == 0:
                    break   # Done
            else:
                unsorted.append(entry)    # Defer sorting for a later pass.

        if len(unsorted) > 0:
            raise Exception("Dependency map contains a circular reference.")
        return sorted_keys

import unittest
class DependencyMapTests(unittest.TestCase):
    def test_typical(self):
        map = DependencyMap([
            ("A", "C"),   # Forward reference
            ("B", "E"),   # Forward reference
            ("D", None),  # No dependency
            ("C", "B"),   # Backward reference
            ("E", None),  # No dependency
            ("F", "G")    # Dependent on something outside map
        ])
        self.assertEquals(["D", "E", "F", "B", "C", "A"], map.sort())
    
    def test_degenerate(self):
        map = DependencyMap([
            ("A", None),
            ("B", None),
            ("C", None),
            ("D", None),
            ("E", None)
        ])
        self.assertEquals(["A", "B", "C", "D", "E"], map.sort())

    def test_worst_case(self):
        map = DependencyMap([
            ("A", "B"),
            ("B", "C"),
            ("C", "D"),
            ("D", "E"),
            ("E", None)
        ])
        self.assertEquals(["E", "D", "C", "B", "A"], map.sort())

    def test_circular_reference(self):
        map = DependencyMap([
            ("A", "B"),
            ("B", "C"),
            ("C", "A")
        ])
        self.assertRaises(Exception, map.sort)

    def test_empty(self):
        map = DependencyMap()
        self.assertEquals([], map.sort())
