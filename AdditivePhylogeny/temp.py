def get_count(n):
    x = n - 1
    
    def count():
        nonlocal x
        x += 1
        return x
    
    return count


if __name__ == '__main__':
    counter = get_count(5)
    
    print(counter())
    print(counter())
    print(counter())
