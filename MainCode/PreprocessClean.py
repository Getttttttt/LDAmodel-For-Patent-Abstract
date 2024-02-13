import os

if __name__ == '__main__':
    input_path="./TranslateAbstract"
    output_path="./CleanAbstract"
    for root, dirs, files in os.walk(input_path):
        for dir in dirs:
            if not os.path.exists(output_path+'/'+dir):
                os.mkdir(output_path+'/'+dir)
            for root, dirs, files in os.walk(input_path+'/'+dir):
                for file in files:
                    with open(input_path+'/'+dir+'/'+file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    # 去除空行
                    lines = [line for line in lines if line.strip()]
                    # 去除以'abstract-'为结尾的行
                    lines = [line for line in lines if not line.strip().endswith('abstract-')]
                    with open(output_path+'/'+dir+'/'+file, 'w', encoding='utf-8') as f:
                        f.writelines(lines)
