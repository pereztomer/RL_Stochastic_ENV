# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

def print_hi(name):
    list_of_tuples = [(12,15),(18,12),(17,4),(12,5)]
    list_of_tuples = sorted(list_of_tuples) #key=lambda x: x[1]
    print(list_of_tuples)
    print(type(sys.float_info.min))
    # Use a breakpoint in the code line below to debug your script.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
