for x in range(151):
    print(x)

for x in range(5, 1000, 5):
    print(x)

for x in range (1, 100):
    if(x%10==0):
        print("Coding Dojo")
    elif(x%5==0):
        print("Coding")
    else:
        print(x)

sum=0
for x in range(500000):
    if (x%2==1):
        sum=sum+x
print(sum)

i=1
sum1=0
while i<=500000:
    if (i%2==1):
        sum1=sum1+i
    i=i+1
print ('Sum of odd numbers',sum1)

j=2018
while j>=0:
    print(j)
    j=j-4

def multiples(lowNum, highNum, mult):
    i=lowNum
    while i<=highNum:
        if (i%mult==0):
            print(i)
        i=i+1
multiples(2, 9, 3)
