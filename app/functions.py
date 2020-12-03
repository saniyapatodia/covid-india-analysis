def sum(a, b):
    return a + b

a = 3
b = 2
answer = sum(a,b)
print(answer)


def product(a, b):
    return a * b

x = 3
y = 2
answer = product(x, y)
print(answer)

def custom_prod(a, b):
    return product(sum(a, b), a) + product(b, a)

a = 3
b = 4
answer  = custom_prod(a,b)
print(answer)
answer = custom_prod(b, a)

def pow(a , b):
    ans = 1
    for i in range(1,b+1):
        ans = ans * a
    return ans

a = 3
b = 4
answer  = pow(a, b)
print(answer)

def pow_2(a , b):
    num = 1
    for i in range(1, (sum(a , b) + 1)):
        num = num * a
    print(num)

a = 2
b = 3
answer = pow_2(a , b)

answer = pow(a, sum(a , b))

def pow_3(a , b):
    num = 1
    for i in range(1, (product(a , b) + 1)):
        num = num * sum(a,b)
    print(num)

a = 2
b = 3
answer = pow_3(a , b)

answer = pow(sum(a, b), product(a, b))

# x, y -> x to the power of y
# x to the power of x + y
# x + y to the power of x * y

def find_number(l, number):
    for val in l:
        if val == number:
            return True
    return False

l = [ 1, 3, 4, 31]
number = 34
answer = find_number(l, number)
print(answer)

def is_prime(n):
    for i in range(2,n):
        if n % i == 0:
            return False
    return True

n = 13
answer = is_prime(n)
print(answer)

def prime_nos(n):
    l = []
    for i in range(2,n):
        if is_prime(i):
            l.append(i)
    return l

n = 10000
answer = prime_nos(n)
#print(answer)

def sqrt(n):
    start = 1
    end = x
    while start <= end:
        mid = (start + end) // 2

        if (mid * mid == x) : 
            return mid 
        if (mid * mid < x) : 
            start = mid + 1
            ans  = mid
        else:
            end = mid-1

    return ans

x = 15          
answer = sqrt(n)
print(answer)




    