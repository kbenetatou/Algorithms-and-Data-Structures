import math
import sys
import collections

name_of_file = sys.argv[2]
function_to_call = sys.argv[1]
d ='-d' in sys.argv 
s_find = '-s' in sys.argv
s = 2 #default value for s.
if s_find : #if the user inputs a value for s i have to see if its integer or float. If int throws exception i am using float
    try : 
        s=int(sys.argv[sys.argv.index('-s') +1]) 
    except ValueError:
        s=float(sys.argv[sys.argv.index('-s') +1])
g_find = '-g' in sys.argv
gamma = 1 
if g_find :
    try :
        gamma=int(sys.argv[sys.argv.index('-g') +1])
    except ValueError:
        gamma=float(sys.argv[sys.argv.index('-g') +1])
with open(name_of_file, 'r') as file: #reading the file and putting its values on a list called time. same as before using a try except.
        time = file.read().split()  
        try :
            time = [int(item) for item in time]
        except ValueError:
            time = [float(item) for item in time]

T = time[-1] - time[0] #calculate the overall dt

x = [0]*(len(time)-1)


n = len(time) - 1 #amount of messages sent/received
for i in range(len(x)) :
    x[i] = time[i+1] - time[i]#calculate each dt
k = math.ceil(1 + math.log(T,s) + math.log(1/min(x), s)) #calculating the k number of possible states

g = T / n #calculating g so as to later calculate λi. 


r = [[0 for i in range(k)] for j in range(k)] #will contain the cost of jumping states. 


for i in range(k) : 
    for j in range(k) :
        if math.pow(s,j) / g > math.pow(s,i) / g: # λj > λi
            r[i][j] = gamma*(j-i)*math.log(n) 



def F(x,ell) : #f function
    return ell*math.exp(-ell*x)

def Viterbi(X) : #viterbi function
    global s,g #using my s and g as global variables as i need them to calculate l. 
    for t in range(1,n+1) :
        for S in range(k) :
            lmin = 0
            cmin = C[t-1][0] + r[0][S]
            for l in range(1,k) :
                c = C[t-1][l] + r[l][S]
                if c < cmin :
                    cmin = c
                    lmin = l
            ell = math.pow(s,S) / g
            f = F(X[t-1],ell)
            if f > 0 : #checking id f > 0 since it will go inside a log function
                C[t][S] = cmin - math.log(f)
            else : #if its equal to zero then i take the lim og log(x) as x approaches 0 since i know that x approaches from the positive side its lim(x->0+) which is -oo. 
                C[t][S] = cmin - float('-inf')

            P[S][0:t] = P[lmin][0:t]
            P[S][t] = S
    cmin = C[n][0]
    smin = 0 

    for S in range(1,k) :
        if C[n][S] < cmin :
  
            cmin = C[n][S]
            smin = S

    return P[smin]  

def Bellman_Ford(tgraph,start,d) : 
#bellman ford algorithm but we are altering it, with dist and pred being dictionaries with nodes (t,q) representing the keys in each dict.    
#the bellman ford here is using the queue implementation as when the user gave somewhat of a big number of time slots (four_states.txt),
#the algorithm took very long to execute without the queue. 
#Another change made is that the algorithm gets d as a paramenet as well.
#if d is true then it displays at every iteration the changes made to each node. 

    nodes = tgraph.keys() #my nodes are the keys. proceeding with bellman ford as usual.

    # Initialize dictionary holding path lengths.
    dist = {node: float('inf') for node in nodes}
    dist[start] = 0
    # Initialize dictionary holding node predecessors.
    pred = {node: -1 for node in nodes}
    # Initialize queue.
    q = collections.deque()
    # We'll use a list to check whether something
    # is already in the queue, so that we won't
    # add it twice.
    in_queue = {node: False for node in nodes}
    in_queue[start] = True
    q.append(start)

    # While the queue is not empty:
    while len(q) != 0:
        u = q.popleft()
        in_queue[u] = False
        # For every edge of the current node, check
        # and update if needed.
        for (v, w) in tgraph[u]: 
            if dist[u] != float('inf') and dist[v] > dist[u] + w: #float('inf') here represents max_int
                prevd = dist[v]
                dist[v] = dist[u] + w
                pred[v] = u
                if d : 
                    for nod, edg in tgraph.items() : #i am searching my graph for the burst cost 
                        if nod == u : #i am looking for the neighbours of node u
                            if (len(edg)) !=0 : #if they exist then :
                                for e in edg : #for every item on that list i take the first element e[0]
                                    if e[0] == v : #if it equals to the node v that i am, then i know that its cost will be stored in the next cell.
                                        cost = e[1]

                    burst_cost = cost - r[u[1]][v[1]] #i know that the cost equals to the cost of jumping to the next state [r(i,j)] + the burst cost. 
                    print(f'{v} {prevd:.2f} -> {dist[v]:.2f} from {u} {dist[u]:.2f} + {r[u[1]][v[1]]:.2f} + {burst_cost:.2f}')

                # Add the node of the updated path in the queue
                # if necessary.
                if not in_queue[v]:
                    q.append(v)
                    in_queue[v] = True
     
    return pred, dist
    
if function_to_call == 'viterbi' : #if the user enters 'viterbi' then i am initializing lists C and P
    C = [[float('inf') for i in range(k)] for j in range(n+1)] 
    C[0][0] = 0
    P = [[0 for i in range(n+1)] for j in range(k)]
    q = Viterbi(x)
    if d : #if d is true then i display C (rounded up to 2 decimals), the length of q and its values. 
        Cnew = [[round(number, 2) for number in row] for row in C]
        for i in Cnew :
            print(i)
        print(len(q), q)


if function_to_call == 'trellis' : #if the use enters 'trellis' then i have to create the trellis graph
    tgraph = {} #using a dictionary to display it. 
    for i in range(k) :
        for j in range(len(time)) :
            if (i == 0) : #just to make sure that the first state is the only one that has the first time (t0) as its key (t0,k)
                tgraph[(j,i)] = [] 
                for m in range(k) :
                        if j < len(time)-1: 
                            node = (j+1,m)
                            ell = math.pow(s,m) / g
                            dt = time[j+1] - time[j]
                            f = F(dt,ell)
                            if f > 0 :
                                weight = r[i][m] - math.log(f)
                            else :
                                weight = r[i][m] - float('-inf')
                            tgraph[(j,i)].append((node,weight))

            elif (time[j]!= time[0]):
                tgraph[(j,i)] = []
                for m in range(k) :
                        if j < len(time)-1:
                            node = (j+1,m)
                            ell = math.pow(s,m) / g
                            dt = time[j+1] - time[j]
                            f = F(dt,ell)
                            if f > 0 :
                                weight = r[i][m] - math.log(f)
                            else :
                                weight = r[i][m] - float('-inf')                          
                            tgraph[(j,i)].append((node,weight))



    pred, dist = Bellman_Ford(tgraph, (0,0),d)
    #having pred and dist now i want to check on dist for every key tuple whose first element is t_last (t_last,i) which one has the shortest distance. 
    min_value = float('inf')
    min_key = None
    for key, value in dist.items():
        if key[0] == (len(time)-1) and value < min_value: 
            min_value = value
            min_key = key
    #having the key where the shortest path ends i have to go backwards to pred to find the nodes that led to the relaxation.
    #from these nodes i will keep the states.
    v = min_key
    q = [] #is where my states will be stored
    while len(q) < len(time) : #while my q hasn't reached its full length.
        for key, value in pred.items():
            if key == v :
                q.append(v)
                v = value
    q = [i[1] for i in q] #only needing the states so i am getting the second element of the tuple
    q = q[::-1] #since i went backwards from the end i need to reverse the list
    if d :
        print(len(q), q)
    
ans = [[] for i in range(n)]

j=0

for i in range(1,len(q)):
        if q[i-1] == q[i] : #the same q the same state so i insert the time
            ans[j].append(time[i-1])
        else :
            ans[j].append(time[i-1]) #different state means that i need to enter the time to both states.
            ans[j].append(q[i-1]) #since i changed states i am keeping the state i was as a guard
            ans[j+1].append(time[i-1]) #appending the time to the next state as well
            j+=1 #move to the next answer cell
        if i == len(q)-1 : #on the final state i am just insering the corresponding time and state 
            ans[j].append(time[i])
            ans[j].append(q[i])

def number_printer(n): #function that formats the output
    if n % 1 == 0 or (n*10 % 1) == 0.0 : #if its integer or its second decimal is 0 then i just display the first decimal part
        return f"{n:.1f}"
    else:
        return f"{n:.2f}" #otherwise i print both decimal parts

ans = [i for i in ans if i] #remove the extra lists
for i in ans:
        qi = i[-1] #my state is in the last cell of each row of the answer
        first = i[0]#starting time is the first
        last = i[-2] #finishing time is the second to last (as my last cell is the state)

        print (f"{qi} [{number_printer(first)}  {number_printer(last)})")
