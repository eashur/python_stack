
import unittest

class MathDojo:
    def __init__(self):
        self.result=0

    def add(self, num, *nums):
       
        for n in range (0, len(nums)):
            if (type(nums[n]) is list or type(nums[n]) is tuple):
                for k in nums[n]:
                    self.result += k
            else:
                self.result += nums[n]
        self.result = self.result+num
        return self


    def subtract(self, num, *nums):
        for n in range (0, len(nums)):
            if (type(nums[n]) is list or type(nums[n]) is tuple):
                for k in nums[n]:
                    self.result -= k
            else:
                self.result -= nums[n]
        self.result = self.result-num
        return self


# create an instance:



# to test:
# x = md.add(2).add(5, 5, 6).subtract(5, 4, 6).result
# y = md.add(2, [3, 4, 5]).add(1, (1, 3, 4)).subtract(4, [3, 2, 1]).result

# x = md.add(2).add(2,5,1).subtract(3,2).result
# print(x)	# should print 5d
# print(y)	# should print 5d

class addTests(unittest.TestCase):
    def testTwo(self):
        md = MathDojo()
        self.assertEqual(md.add(2).result, 2)
    def testTwoFive(self):
        md25 = MathDojo()
        self.assertEqual(md25.add(2, 5).result, 7)
    def testTwoFive7(self):
        md257 = MathDojo()
        self.assertEqual(md257.add(2, 5, 7).result, 14)

    def testTwoFive73(self):
        md2573 = MathDojo()
        self.assertEqual(md2573.add(2, 5, 7).subtract(3).result, 11)

    def testTwoFive732(self):
        md25732 = MathDojo()
        self.assertEqual(md25732.add(2, 5, 7).subtract(3, 2).result, 9)


if __name__ == '__main__':
    unittest.main() # this runs our tests