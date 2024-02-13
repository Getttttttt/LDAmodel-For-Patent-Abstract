import os

if __name__ == '__main__':
    total_num = 0
    input_path="./CleanAbstract"
    for root, dirs, files in os.walk(input_path):
        for dir in dirs:
            for root, dirs, files in os.walk(input_path+'/'+dir):
                for file in files:
                    with open(input_path+'/'+dir+'/'+file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        total_num += len(lines)
    print(total_num)