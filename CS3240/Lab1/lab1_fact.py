#Gabriel Groover (gtg3vv)

def factorial1(n):
    if n == 0:
        return 1
    if n < 0:
        raise ValueError("Cannot compute negative factorials")
        
    result = n
    while (n > 1):
        n-=1
        result *= n
    return result
        
def factorial2(n):
    values = []
    for i in range(n+1):
        values.append(factorial1(i))
    return values
    
def test_fact1():
    assert factorial1(0) == 1, "Factorial of 0 not 1"
    assert factorial1(1) == 1, "Factorial of 1 not 1"
    assert factorial1(5) == 120, "Factorial of 5 not 120"
    try:
        factorial1(-1)
    except ValueError:
        print("Negative number!")


if __name__ == "main":
    test_fact1()
    assert factorial2(4) == [1,1,2,6,24], "Incorrect 0 to n factorial for 4"
    

        