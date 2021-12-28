from trie import Trie

trie = Trie()

trie.add(['he', 'she', 'his', 'hers'])
trie.compute_fail()

trie.traverse('ahishers')
