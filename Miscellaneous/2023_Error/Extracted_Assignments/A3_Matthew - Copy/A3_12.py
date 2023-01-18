alph = [chr(x) for x in range(97,123)]
alphUpper = [chr(x).upper() for x in range(97,123)]
nums = [str(x) for x in range(10)]

testlower = lambda x : True if(x in alph) else False
testupper = lambda x : True if(x in alphUpper) else False
testNum = lambda x : True if(x in nums) else False

while True:
  n = input()
  if(len(list(filter(testlower, n))) != 0):
    if(len(list(filter(testupper, n))) != 0):
      if(len(list(filter(testNum, n))) != 0):
        if(len(n) >= 6):
          print("Valid string.")
          break
  print("Invalid input.")
