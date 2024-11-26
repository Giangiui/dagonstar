import sys
import math

x = open(sys.argv[1],'r')

print(math.pow(int(x.read()), 2))