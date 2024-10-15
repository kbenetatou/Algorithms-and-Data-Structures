import sys

green = { 
    '0' : [['','G'],
          ['G','G']],
    '90' : [['G', ''],
           ['G','G']],
    '180' : [['G','G'],
            ['','G']],
    '270' : [['G','G'],
            ['G','']]
}
blue = {
    '0' : [['','B'],
          ['B','B']],
    '90' : [['B', ''],
           ['B','B']],
    '180' :[['B','B'],
            ['','B']],
    '270' :[['B','B'],
            ['B','']]
}
red = {    
    '0' : [['','R'],
          ['R','R']],
    '90' : [['R', ''],
           ['R','R']],
    '180' : [['R','R'],
            ['','R']],
    '270' :[['R','R'],
            ['R','']]
}
position_of_void = { #this dictionary will help me find the degrees of the colors i need to use.
    (0,0): '0',
    (0,1):'90',
    (1,0) :'180',
    (1,1):'270'
}
user_number=int(sys.argv[1])
n=pow(2,user_number)
ans = [['X']*n for i in range(n)] #arxikopoiw ton ans me 'X'
if user_number == 1 : #an einai 2x2 den mpainei stin synartisi kai ginetai aytomata.
        color = green.get('90') #apo to paradeigma pairnw degree = 90
        for i in range(len(color)): #vazw ston ans to color
            for j in range(len(color[i])):
                if color[i][j] != '':  
                    ans[(n-2)//2 + i][(n-2)//2 + j] = color[i][j]

def rec(ans,user_number) : 

    if user_number == 2 :
        n=pow(2,user_number) 
        middle = n//2
        #put green in the middle. i need to find the degrees.
        x = [x for x in ans if 'G' in x] #check if there is already a green in my square. 

        degrees = '270' #if there isnt i go with 270.
        pos = None

        if len(x) != 0 : #if there is i want to keep its position
            pos = (ans.index(x[0]), x[0].index('G'))
            if pos[0] == pos[1] : #if pos[0] == pos[1] i know its either 0 or 270 degrees
                if pos[0] == 0 :
                    degrees = '0'
                else :
                    degrees = '270'
            elif pos[0] == 0 and pos[1] != 0: 
                degrees = '90'

            elif pos[0] >= 1 and pos[1] != 1:
                degrees = '180'

        color = green.get(degrees) 
        for i in range(len(color)): #put greeen in the ans 
            for j in range(len(color[i])):
                if color[i][j] != '':
                    ans[(n-2)//2 + i][(n-2)//2 + j] = color[i][j]

        #begin with red : 
        helper = [row[0:middle] for row in ans[middle:n]]#begin with bottom left quadrant. put it in a list (helper)
        #i want to check if i have a G in helper 
        x = [x for x in helper if 'G' in x] 

        if len(x) != 0 : 
            if 'G' not in x[0] :  
                color = red.get('270')
            else:
                position=(helper.index(x[0]),x[0].index('G')) #vlepw pou exw to 'g'-> ekei tha einai to void tou tromino

                color = red.get((position_of_void.get(position))) #to position tou void mou kathorizei tis moires.
        else :
             color = red.get('270')
        for i in range(len(color)):
            for j in range(len(color[i])):
                if color[i][j] != '':
                    ans[i + (n - 2)][j] = color[i][j]
        #continue with blue
        helper = [row[0:middle] for row in ans[0:middle]]#top left quadrant. 
        x = [x for x in helper if 'G' in x][0]
        if 'G' not in x :
            color = blue.get('270')
        else:       
            position=(helper.index(x),x.index('G'))
            color = blue.get((position_of_void.get(position)))
        for i in range(len(color)):
            for j in range(len(color[i])):
                if color[i][j] != '':
                    ans[i][j] = color[i][j]

        helper = [row[middle:n] for row in ans[0:middle]]#top right quadrant.
        x = [x for x in helper if 'G' in x][0]
        if 'G' not in x :
            color = red.get('270')
        else:
            position=(helper.index(x),x.index('G'))
            color = red.get((position_of_void.get(position)))
        for i in range(len(color)):
            for j in range(len(color[i])):
                if color[i][j] != '':
                    ans[i][j+(n-2)] = color[i][j]
        
        helper = [row[middle:n] for row in ans[middle:n]]#bottom right quadrant.
        x = [x for x in helper if 'X' in x][0]

        if 'G' not in x : #an den yparxei to G sto quarter mou
                color = blue.get('270')
        else :
                position=(helper.index(x),x.index('G'))
                color = blue.get((position_of_void.get(position)))

        for i in range(len(color)):
            for j in range(len(color[i])):
                if color[i][j] != '':
                    ans[i + (n - 2)][j+(n-2)] = color[i][j]

        return ans
    if user_number > 2:
        
        #find the middle and put green in there i want to see if there is already a green in ans. if there isnt put green0
        n=pow(2,user_number)
        middle = n//2
        x = [x for x in ans if 'G' in x]
        degrees = '0'
        pos = None
        if len(x) != 0 :
            pos = (ans.index(x[0]), x[0].index('G'))

            if pos[0] == pos[1] :
                if pos[0] == 0 :
                    degrees = '0'
                else :
                    degrees = '270'
            elif pos[0] == 0 and pos[1] != 0:
                degrees = '90'
            elif pos[0] >= 1 and pos[1] != 1:
                degrees = '180'
        color = green.get(degrees)

        for i in range(len(color)):
            for j in range(len(color[i])):
                if color[i][j] != '':
                    ans[(n-2)//2 + i][(n-2)//2 + j] = color[i][j]
        #divide ans to 4 quadrants. 
        helper1 = [row[0:middle] for row in ans[middle:n]]#bottom left
        helper2 = [row[0:middle] for row in ans[0:middle]]#top left
        helper3 = [row[middle:n] for row in ans[0:middle]]#top right
        helper4 = [row[middle:n] for row in ans[middle:n]]#bottom right

        if user_number > 3 : #i want to keep the return of helper1 and set it as the new helper1 when recursion happens for more than 2 times.
            helper1 = rec(helper1,user_number-1) 
        else:
            rec(helper1,user_number-1)

        if user_number > 3 :
            helper2= rec(helper2,user_number-1)
        else:
            rec(helper2,user_number-1)

        if user_number > 3 :
            helper3 = rec(helper3,user_number-1)
        else:
            rec(helper3,user_number-1)

        if user_number > 3 :
            helper4 = rec(helper4,user_number-1)
        else :
            rec(helper4,user_number-1)
        #merge helper1,2,3,4 :
        ans =[[''] * n for _ in range(n)]
        # Assign helper2 to the top-left quadrant of ans
        for i in range(middle):
            for j in range(middle):
                ans[i][j] = helper2[i][j]

        # Assign helper3 to the top-right quadrant of ans
        for i in range(middle):
            for j in range(middle):
                ans[i][j + middle] = helper3[i][j]

        # Assign helper1 to the bottom-left quadrant of ans
        for i in range(middle):
            for j in range(middle):
                ans[i + middle][j] = helper1[i][j]

        # Assign helper4 to the bottom-right quadrant of ans
        for i in range(middle):
            for j in range(middle):
                ans[i + middle][j + middle] = helper4[i][j]


    return ans





ans = rec(ans,user_number)

for i in range(n) :            
   print(*ans[i], sep=' ')
