import random
def randInt(min=0, max=100):
    if(min>max or max<0):
       return "invalid parameters"

    num = random.random()*max
    return round(num)

print(randInt())
print(randInt(max=50))
print(randInt(min=50))
print(randInt(min=50, max=500))
print(randInt(min=50, max=0))
print(randInt(min=200, max=110))
