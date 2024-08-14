import sys
import tempfile
import hashlib
import os
import bisect
# uniq expects things to be ordered
# our unique does not
# called with some arguments? all the same. just process stdin
# how big?
# whitespace diff 
# worst case is O(n) where n is the sum of all characters

# how to handle a lot of stuff
# batch/chunk
# write some to files
# some compression -> can help but has a ceiling
# map/reduce

# have chunks
# once chunk reaches size offload/write.
# keep track of your chunks
# merge chunks
# how to merge?
# read a chunk from file read in line by line
# sorting? need to keep order of unordered things
# finished output set is bigger than memory
# max bloom filter memory but keep streaming. compact representation vs 100% correctness
# correctness, robustness over speed

# once you get your bucket/chunk size
# hash to files
# open that file to see if it already exists
# re distribute the keys as you make new files
# 100 files
# red black storage instead of apepnd only file
class ConsistentHashDeduplicator:
    def __init__(self, num_virtual_nodes=100, num_physical_nodes=10):
        self.num_virtual_nodes = num_virtual_nodes
        self.num_physical_nodes = num_physical_nodes
        self.temp_dir = tempfile.mkdtemp()
        self.ring = []
        self.node_mapping = {}
        self.files = {}
        self._init_hash_ring()

    def _add_node(self, node):
        # insert self into ring with a key
        # f'node{node}:{virtual}
        for i in range(self.num_virtual_nodes):
            key = f'node{node}:{i}'
            hash_val = self._hash(key)
            index = bisect.bisect(self.ring, hash_val)
            self.ring.insert(index, hash_val)
            self.node_mapping[hash_val] = node

    def _init_hash_ring(self):
        for i in range(self.num_physical_nodes):
            self._add_node(i)
    
    def _hash(self, key):
        return hashlib.md5(str(key).encode()).hexdigest()

    def _get_node(self, line):
        hash_value = self._hash(line)
        # find the node by bin saerch
        # get the node from node mapping
        index = bisect.bisect(self.ring, hash_value)
        if index == len(self.ring):
            index = 0
        return self.node_mapping[self.ring[index]]
    
    def _get_file(self, node):
        # check if it exists
        if node not in self.files:
            filename = os.path.join(self.temp_dir, f"node_{node}")
            self.files[node] = open(filename, "a+")
        return self.files[node]
    
    def is_unique(self, line):
        node = self._get_node(line)
        
        file = self._get_file(node)
        # check line by line instead of reading all into mem
        file.seek(0)
        for existing_line in file:
            if existing_line.strip() == line:
                file.seek(0, 2)
                return False

        file.write(line + '\n')
        file.flush()
        return True

    def cleanup(self):
        # deleete all the files
        os.rmdir(self.temp_dir)

def process_stdin(input_stream=sys.stdin, output_stream=sys.stdout):
    deduplicator = ConsistentHashDeduplicator()
    #try:
    for line in input_stream:
        line = line.strip()
        if deduplicator.is_unique(line):
            print(line, file=output_stream)
            output_stream.flush()
    #finally:
        #deduplicator.cleanup()
    # clean up temp

# def process_stdin(input_stream=sys.stdin, output_stream=sys.stdout):
#     seen_lines = set()
#     for line in input_stream:
#         line = line.strip()

#         if line not in seen_lines:
#             print(line, file=output_stream)
#             seen_lines.add(line)

if __name__ == "__main__":
    process_stdin()


