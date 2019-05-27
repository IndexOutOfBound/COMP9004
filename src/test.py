import numpy as np



if __name__ == "__main__":
    first = np.zeros(10)
    h = first.copy()
    first[6] = 5
    print(first)
    print( h)