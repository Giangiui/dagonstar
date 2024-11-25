import sys

x = open(sys.argv[1],'r')
y = open(sys.argv[2],'r')

z = int(x.read()) + int(y.read())

print(z)