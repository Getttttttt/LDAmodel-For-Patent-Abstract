import os

if __name__ == '__main__':
    input_path="./Abstract"
    for root, dirs, files in os.walk(input_path):
        for dir in dirs:
            os.remove(input_path+'/'+dir+'/'+"Date2023-2024.txt")