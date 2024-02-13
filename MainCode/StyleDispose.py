import csv

if __name__ == '__main__':
    with open('OutcomeAbstract.txt', 'r') as f:
        lines = f.readlines()

    with open('output.csv', 'w' ,newline='' ) as f:
        writer = csv.writer(f)
        for line in lines:
            id_str = line.split(' ')[0].split('-')[1]
            vector_str = line.split('vector-')[1]
            vector_list = eval(vector_str)
            list_output=[0 for i in range(24)]
            for i in range(len(vector_list)):
                list_output[vector_list[i][0]] = vector_list[i][1]
            row = [id_str]
            for i in range(24):
                row.append(list_output[i])
            writer.writerow(row)
