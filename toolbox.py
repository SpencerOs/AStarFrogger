# toolbox.py
# Author: Spencer Ollila

# Where the tools are kept

import heapq

# This class was based off of the priority queue
# found in the util.py file we received in our homeworks
class priority_queue:
    def __init__(self):
        self.heap   = []
        self.count  = 0

    def __len__(self):
        return self.count

    def __contains__(self, item):
        return item in self.heap
        
    
    # You can push an item already existing into the queue,
    # but the old (hopefully bigger) one won't be deleted.
    # This is alright, because the higher costing duplicate
    # won't be popped off, seeing how all the other cheaper
    # options will be popped off and the goal found, before
    # the bigger duplicate is popped.
    # This whole long comment block is more reassurance for
    # me than anything else.
    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        self.count -= 1
        return item

    def is_empty(self):
        return len(self.heap) == 0

# Returns the distance between the agent on the road
# and the sandbar on the river
def sandbar_distance(loc):
    #print("toolbox: h_cost at %s is: %d" % (loc, (loc[0] - 6)))
    return (loc[0] - 6)

# Returns the distance between the agent and the first
# available landing pad
def goal_distance(loc, guide):
    #print("goal_distance: being called with value " + str(loc))
    queue = priority_queue()
    # if the first landing bay is empty
    if guide[0][1] == 1:
        distance = (loc[0] + abs(loc[1] - 1))
        queue.push(1, distance)
    # if the second landing bay is empty
    if guide[0][5] == 1:
        distance = (loc[0] + abs(loc[1] - 5))
        queue.push(5, distance)
    # if the third landing bay is empty
    if guide[0][9] == 1:
        distance = (loc[0] + abs(loc[1] - 9))
        queue.push(9, distance)
    # if the fourth landing bay is empty
    if guide[0][13] == 1:
        distance = (loc[0] + abs(loc[1] - 13))
        queue.push(13, distance)
    # if the fifth landing bay is empty
    if guide[0][17] == 1:
        distance = (loc[0] + abs(loc[1] - 17))
        queue.push(17, distance)
    # pop off the spot which will have the lowest distance
    nearest = queue.pop()
    distance = (loc[0] + abs(loc[1] - nearest))
    return distance
