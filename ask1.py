import numpy as np
import random
#Read dimension from keyboard with user error controlling
dimension=input("\nΔώσε διάσταση τετραγώνου: ")
while dimension.isdigit()==False:
  dimension=input("\n(ΛΑΘΟΣ ΕΙΣΟΔΟΣ) Δώσε διάσταση τετραγώνου: ")
#Total horizontal,vertical and diagonal 1111
th=0
tv=0
td=0

#Search for '1111' in a given string
def CheckForString(sd):
    count = 0
    start = 0
    while start < len(sd):
        pos = sd.find("1111", start)
        #if present:
        if pos != -1:
            start = pos + 1
            count += 1
        else:
            break
    return count;

#Function to traverse diagonally
def diagonal():
    global td

    #Lower and main diagonal (left bottom to top right)
    for i in range(len(A),-1,-1):
        sd=""
        k=0
        for j in range(i,len(A)):
            sd+=str((A[j][k]))
            k+=1
        #Check for multiple instances of 1111 in 1 diagonal
        td+=CheckForString(sd)
    #Upper diagonal (middle to top right)
    for i in range(len(A)):
        sd=""
        k=0
        for j in range(i+1,len(A)):
            sd+=str((A[k][j]))
            k+=1
        #Check for multiple instances of 1111 in 1 diagonal
        td+=CheckForString(sd)

    #Lower and main diagonal (right bottom to top left)
    for i in range(len(A),-1,-1):
        sd=""
        k=len(A)-1
        for j in range(i,len(A)):
            sd+=str((A[j][k]))
            k-=1
        #Check for multiple instances of 1111 in 1 diagonal
        td+=CheckForString(sd)
    #Upper diagonal (middle to top left)
    for i in range(len(A)-2,-1,-1):
        sd=""
        k=0
        for j in range(i,-1,-1):
            sd+=str((A[j][k]))
            k+=1
        #Check for multiple instances of 1111 in 1 diagonal
        td+=CheckForString(sd)

#Function to traverse horizontally
def horizontal():
    global th
    sd=""
    linebr=dim
    for i in range(len(A)):
        if i==linebr:
            sd+=" "
            linebr+=dim
        sd+=str(A[i])
    th+=CheckForString(sd)

#Function to traverse vertically
def vertical():
    global tv
    sd=""
    for i in range(dim):
        for j in range(i,len(A)+i-dim+1,dim):
            sd+=str(A[j])
        sd+=" "
    tv+=CheckForString(sd)

#X represents number of elements in the dimXdim table
dim=(int(dimension))
x=dim**2
#Create arrays with 1s and 0s half-half. Loops 100 times
l=1
while l<=100:
    #If selected dimension is less than 4,no reason to loop since there are no '1111's
    if dim<=3:
        print("\nSelected dimension does not create four 1's in a row")
        break;
    #Array creation
    A=[]
    for i in range(x//2):
        A.append(0)
    if x%2==0:
        #Case 1: even dimension
        for i in range(x//2):
            A.append(1)
    else:
        #Case 2: odd dimension
        for i in range(x//2+1):
            A.append(1)
    print("\n")
    #Shuffle around the array items
    random.shuffle(A)
    horizontal()
    vertical()
    #Split array into the table lines for diagonal
    A=np.array_split(A, int(dimension))
    diagonal()
    #Print out table
    for i in range(dim):
        #Print acts as \n
        print("")
        for j in range(dim):
            print(A[i][j], end = " ")
    l+=1
#Print-out results
print("\n")
print("Horizontal: ",th)
print("Vertical: ",tv)
print("Diagonal: ",td)
AVG=(th+tv+td)//100
print("Rounded average number of 1111's: ",AVG)
