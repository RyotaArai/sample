from elasticsearch import Elasticsearch
import os
import sys

def get_document(index_name):
    index_list=[]
    data = es.search(index=index_name, scroll='1h',  body={"query": {"match_all": {}}})
    return get_index(data, index_list)


def get_index(data, index_list):
    sid = data['_scroll_id']
    scroll_size = len(data['hits']['hits'])
    for i in data['hits']['hits']:
        index_list.append([i])
    while scroll_size > 0:
        data = es.scroll(scroll_id=sid, scroll='1h')
        for i in data['hits']['hits']:
            index_list.append([i])
        sid = data['_scroll_id']
        scroll_size = len(data['hits']['hits'])
    return index_list


# Main
args = sys.argv

es_endpoint = os.getenv('ELASTICSEARCH_HOST')
es_user = os.getenv('ES_USER')
es_password = os.getenv('ES_PWD')
index_name = os.getenv('INDEX_NAME')

es = Elasticsearch(
    es_endpoint,
    http_auth=(es_user, es_password),
    headers={'Content-Type':'application/json'}
)

index_list=get_document(index_name)

cnt=0
for log in index_list:
    if  len(args) == 2 and args[1] == 'output':
        print(log)
    cnt=cnt+1
print("Size: " + str(cnt))
