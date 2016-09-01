#!/usr/bin/python

from scipy.stats import ttest_ind
import sys
from collections import defaultdict
import random
import numpy as np

# NOTES:
# Everything is Zero indexed


# HELP
if len(sys.argv) != 3:
    print "USAGE: ./t_test data_file.txt community_file.txt"
    sys.exit(1)


######## Load the TRUST info from the main data file(1st file)

# > trust = {}  | trust b/w i and j
# > matrix = [][] | trust b/w i and j | boolean1
filename = sys.argv[1]
with open(filename) as f:
    lines = f.read().split('\n')

max_node_index = 0
edges = defaultdict(list)
for s in lines:
    if len(s) < 1:
	continue
    i,j = s.split()
    i, j = int(i), int(j)
    edges[i] += [j]
    max_node_index = max(max_node_index, max(i, j))

matrix = np.zeros((max_node_index + 1, max_node_index + 1))
for (i,js) in edges.items():
    for j in js:
	matrix[i][j] = 1






####### Load the community info from the 2nd file
filename = sys.argv[2]
with open(filename) as f:
    lines = f.read()
    lines = lines.split('\n')

communities = {}

for s in lines:
    if len(s) < 1:
	continue
    node, community = s.split()
    node, community = int(node), int(community)

    if community not in communities.keys():
        communities[community] = []
    communities[community].append(node)


# Test arrays
a = []
b = []


# Selecting the nodes
##### Choose random community
# com_no = random.randint(0, max(communities.keys()))
##### Choose the biggest
sizes_ = {len(communities[com]):com for com in communities.keys()}
com_no = sizes_[max(sizes_)]
print "Choosen Community: (No=%d, Size=%d)" % (com_no, len(communities[com_no]))

people_outside = [i for i in range(max_node_index+1) if i not in communities[com_no]]
for member in communities[com_no]:
    outside = people_outside[random.randint(0, len(people_outside)-1)]
    a.append(matrix[member][outside])
    b.append(matrix[outside][member])

# Show stats about the data used in t-test
print "%f percent of 1's in a | %f percent of 1's in b" %((len([1 for i in a if i == 1])*100.0)/len(a), (len([1 for i in b if i == 1])*100.0)/len(b))

#import pdb
#pdb.set_trace()
# Test
try:
    t, p = ttest_ind(a, b, equal_var=False)
    print "ttest_ind:            t = %g  p = %g" % (t, p)
except:
    print ">>>>>>>>> ERROR!"
