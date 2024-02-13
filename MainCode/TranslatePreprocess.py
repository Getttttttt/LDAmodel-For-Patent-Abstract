import sys
import uuid
import requests
import hashlib
import time
from imp import reload
import json
import time
import os
import langid

reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '0b66bda02a0868a1'
APP_SECRET = 'mAWfLZVQ1DlIko8SFFkKF6s9svb1KZlz'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect(q):

    data = {}
    data['from'] = 'auto'
    data['to'] = 'en'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign
    data['vocabId'] = "4DDF671083954709AC9B7AE523D186AF"

    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        millis = int(round(time.time() * 1000))
        filePath = "合成的音频存储路径" + str(millis) + ".mp3"
        fo = open(filePath, 'wb')
        fo.write(response.content)
        fo.close()
    else:
        dic = json.loads(response.content)
        result = dic.get('translation')
        return result
        


if __name__ == '__main__':
    input_path="./Abstract"
    output_path="./TranslateAbstract"
    for root, dirs, files in os.walk(input_path):
        for dir in dirs:
            if not os.path.exists(output_path+'/'+dir):
                os.mkdir(output_path+'/'+dir)
            for root, dirs, files in os.walk(input_path+'/'+dir):
                for file in files:
                    with open(output_path+'/'+dir+'/'+file,'w', encoding='utf-8') as f_output:
                        with open(input_path+'/'+dir+'/'+file,'r',encoding='utf-8') as f_input:
                            for line in f_input:
                                each_patent = line.split('    ',1)
                                id_number = each_patent[0]
                                abstract = each_patent[1]
                                id_number = id_number.split('-',1)[1]
                                abstract = abstract.split('-',1)[1]
                                if abstract == '' or abstract == None:
                                    continue
                                if 'WO' in id_number or 'EP' in id_number or 'JP' in id_number or 'US' in id_number:
                                    if langid.classify(abstract)[0] != 'en':
                                        connect_abstract = connect(abstract)
                                        abstract = connect_abstract[0].strip()
                                    f_output.write('id-'+id_number)
                                    f_output.write('    ')
                                    f_output.write('abstract-'+abstract)
                                    f_output.write('\n')
                                    time.sleep(1)