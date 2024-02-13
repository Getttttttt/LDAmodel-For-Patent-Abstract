```python
def generateDict(input_path):
    dict_patent={}
    for root, dirs, files in os.walk(input_path):
        for dir in dirs:
            for root, dirs, files in os.walk(input_path+'/'+dir):
                for file in files:
                    with open(input_path+'/'+dir+'/'+file,'r',encoding='utf-8') as f_input:
                        for line in f_input:
                            line=line.strip()
                            each_patent = line.split('    ',1)
                            id_number = each_patent[0]
                            abstract = each_patent[1]
                            id_number = id_number.split('-',1)[1]
                            abstract = abstract.split('-',1)[1]
                            if id_number in dict_patent :pass
                            else : dict_patent[id_number]=abstract
    return dict_patent
```