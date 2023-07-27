import sys
from waterTemp import *
from dataExtract import *

def main():
    """Main function calling all other functions """

    """Call function to import dataset into object"""
    data = dataExtract() 

    """Call function to analyse dataset object"""
    waterTemp(data) 

if __name__ == '__main__':
    sys.exit(main()) 