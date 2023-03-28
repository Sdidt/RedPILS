import requests
import json
import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.environ.get("SYS_PATH"))

from utils.helpers import *
from utils.constants import *

class solr_ingest():
    def __init__(self,solr_url,collection_name,headers, alpha=0.9, beta=0.1) -> None:
        self.solr_url = solr_url
        self.collection_name = collection_name
        self.headers = headers
        self.alpha = alpha
        self.beta = beta

    def get_doc_count(self, collection_name):
        query_params = {
            'q': "*:*", 
            'rows': 0
        }

        url = self.solr_url+'/'+collection_name
        response = requests.get(f'{url}/select', params=query_params)
        numFound = response.json()['response']['numFound']
        print("Number found: {}".format(numFound))
        return numFound

    def upload_configset(self, configset_zip_path, configset_name, overwrite=True):
        query_params = {
            "action": "UPLOAD",
            "name": configset_name,
            "overwrite": overwrite
        }

        headers = {
            'Content-type': 'application/octet-stream'
        }
        data = {
            'file': open(configset_zip_path, 'rb')
        }
        url = self.solr_url + '/admin/configs'

        response = requests.post(url, params=query_params, files=data, headers=headers)
        if response.status_code == 200:
            print("Config set {} successfully updated.".format(configset_name))
        else:
            print("Error occurred uploading config set: {}".format(response.text))


    def check_submission_exists(self, collection_name, submission_id):
        query_params = {
            'q': 'submission_id: {}'.format(submission_id),
            'rows': 0
        }

        url = self.solr_url+'/'+collection_name
        response = requests.get(f'{url}/select', params=query_params)
        numFound = response.json()['response']['numFound']
        print("Number found: {}".format(numFound))
        return numFound > 0

    def check_collection_exists(self,collection_name):
        request_data = {
            'action': 'CLUSTERSTATUS'
        }

        response = requests.get(f'{self.solr_url}/admin/collections', params=request_data)
        if response.status_code == 200:
            cluster_status = response.json()['cluster']
            if collection_name in cluster_status['collections']:
                return True
            else:
                return False
        else:
            print(f'Error checking collection: {response.text}')
            return True

    def create_collection(self, collection_name,schema, unique_key, field_type=None):
        collection_exists = self.check_collection_exists(collection_name)
        if(collection_exists):
            print(f'Collection "{collection_name}" exists')
            return
        else:
            print(f'Collection "{collection_name}" does not exist')

        config_name = 'myConfigSet'
        num_shards = 2
        replication_factor = 2

        request_data = {
            'action': 'CREATE',
            'name': collection_name,
            'numShards': num_shards,
            'replicationFactor': replication_factor,
            'collection.configName': config_name,
            'collection.uniqueKey': unique_key
        }

        response = requests.get(f'{self.solr_url}/admin/collections', params=request_data)
        if response.status_code == 200:
            print(f'Collection "{collection_name}" created successfully')
        else:
            print(f'Error creating collection: {response.text}')

        if field_type is not None:
            self.add_new_field_type(collection_name, field_type)
        self.define_schema(collection_name,schema)

    def delete_collection(self,collection_name):
        url = self.solr_url+'/'+collection_name

        collection_exists = self.check_collection_exists(collection_name)
        if(collection_exists):
            print(f'Collection "{collection_name}" exists')
        else:
            print(f'Collection "{collection_name}" does not exist')
            return

        request_data = {
            'action': 'DELETE',
            'name': collection_name
        }
        response = requests.get(f'{self.solr_url}/admin/collections', params=request_data)
        if response.status_code == 200:
            print(f'The collection "{collection_name}" has been deleted.')
            # print(response.text)
        else:
            print(f'Error deleting the collection: {response.text}')

    def add_new_field_type(self, collection_name, new_field_type):
        url = self.solr_url+'/'+collection_name

        request_data = {
            'add-field-type': new_field_type
        }

        response = requests.post(f'{url}/schema', headers=self.headers,json=request_data)

        if response.status_code == 200:
            print(f'The field type {new_field_type["name"]} for the collection "{collection_name}" has been added.')
        else:
            print(f'Error updating the schema: {response.text}')
        
    def add_new_copy_field(self, collection_name, copy_field):
        url = self.solr_url+'/'+collection_name

        request_data = {
            'add-copy-field': copy_field
        }

        response = requests.post(f'{url}/schema', headers=self.headers,json=request_data)

        if response.status_code == 200:
            print(f'The copy field {copy_field["dest"]} for the collection "{collection_name}" has copied fields now.')
        else:
            print(f'Error updating the schema: {response.text}')
        
    def add_new_request_handler(self, collection_name, request_handler):
        url = self.solr_url+'/'+collection_name

        request_data = {
            'add-requesthandler': request_handler
        }

        response = requests.post(f'{url}/config', headers=self.headers,json=request_data)

        if response.status_code == 200:
            print(f'The request handler {request_handler["name"]} for the collection "{collection_name}" has been added.')
        else:
            print(f'Error updating the config: {response.text}')

    def update_existing_field_type(self, collection_name, field_type_def):
        url = self.solr_url+'/'+collection_name

        request_data = {
            'replace-field-type': field_type_def
        }

        response = requests.post(f'{url}/schema', headers=self.headers,json=request_data)

        if response.status_code == 200:
            print('The field type {} for the collection "{}" has been updated.'.format(field_type_def['name'], collection_name))
        else:
            print(f'Error updating the schema: {response.text}')

    def define_schema(self,collection_name,schema):
        url = self.solr_url+'/'+collection_name

        request_data = {
            'add-field': schema
        }

        response = requests.post(f'{url}/schema', headers=self.headers,json=request_data)

        if response.status_code == 200:
            print(f'The schema for the collection "{collection_name}" has been updated.')
        else:
            print(f'Error updating the schema: {response.text}')

    def update_schema(self,collection_name):
        url = self.solr_url+'/'+collection_name
        new_schema = {
            "add-field": {
                "name": "my_new_field",
                "type": "string",
                "stored": "true",
                "indexed": "true"
            }
        }

        update_headers = {'Content-type': 'application/json', 'If-Match': '*'}
        response = requests.post(f'{url}/schema', json=new_schema, headers=update_headers)

        if response.status_code == 200:
            print('Schema has been updated in Solr.')
        else:
            print(f'Error updating schema in Solr: {response.text}')

    def replace_schema(self,collection_name,schema):
        url = self.solr_url+'/'+collection_name

        request_data = {
            'replace-field': schema
        }

        response = requests.post(f'{url}/schema', headers=self.headers,json=request_data)

        if response.status_code == 200:
            print(f'The schema for the collection "{collection_name}" has been replaced.')
        else:
            print(f'Error replacing the schema: {response.text}')

    def push_data(self,collection_name,data):
        url = self.solr_url+'/'+collection_name

        doc_json = json.dumps(data)
        response = requests.post(f'{url}/update/json/docs', headers=self.headers, data=doc_json)
        requests.get(f'{url}/update?commit=true')

    def query_data(self,query_params,collection_name):
        url = self.solr_url+'/'+collection_name

        response = requests.get(f'{url}/select', params=query_params)
        search_results = response.json()['response']['docs']

        return search_results
    
    def delete_data(self,collection_name):
        url = self.solr_url+'/'+collection_name
        request_data = {'delete': {'query': '*:*'}}
        response = requests.post(f'{url}/update', headers=self.headers,json=request_data)
        commit_response = requests.get(f'{url}/update?commit=true')

        if response.status_code == 200 and commit_response.status_code == 200:
            print(f'All data deleted from collection "{collection_name}" successfully')
        else:
            print(f'Error deleting data from collection: {response.text}')

    def update_data(self,collection_name):
        url = self.solr_url+"/"+collection_name

        query_params = {
            'q': 'text:document',
            'fl': 'id,title,text'
        }
        search_results = self.query_data(query_params,collection_name)
        if len(search_results) > 0:
            print(search_results)
            print('Documents before update:')
            for doc in search_results:
                print(doc)
            
            doc_id = search_results[0]['id']
            update_data = [
                {
                    'id': doc_id,
                    'text': {'set': 'This is an updated description'}
                }
            ]
            update_response = requests.post(f'{url}/update?commit=true', json=update_data, headers=self.headers)
            
            if update_response.status_code == 200:
                print('Document updated successfully.')
            else:
                print(f'Error updating document: {update_response.text}')
            
            query_params['q'] = f'id:{doc_id}'
            updated_search_results = self.query_data(query_params,collection_name)
            if len(updated_search_results) > 0:
                print('Document after update:')
                print(updated_search_results)
            else:
                print(f'Error querying updated document')
        else:
            print(f'Error querying documents')
        
    def compute_avg_tf_idf(self, term, collection_name):
        url = self.solr_url+'/'+collection_name

        query_params = {
            "q": "{{!func}}mul(tf(comment, {}), idf(comment, {}))".format(term, term),
            "fl": "score,url",
            "rows": 100000
        }

        response = requests.get(f'{url}/select', params=query_params)
        search_results = response.json()['response']['docs']
        avg_score = sum([result["score"] for result in search_results])/len(search_results)

        return avg_score

    def compute_query_term_score(self, query_term, collection_name, K):
        url = self.solr_url+'/'+collection_name

        query_params = {
            "q": "comment:{}".format(query_term),
            "_query_": "{!rank f='pagerank', function='log' scalingFactor='1.2'}",
            "fl": "score,comment,url",
            "rows": 100
        }

        response = requests.get(f'{url}/select', params=query_params)
        search_results = response.json()['response']['docs']

        return search_results[:K]

    def phrase_query(self, collection_name, phrase_query, term_imp, bigram_imp, trigram_imp, full_phrase_imp, K):
        url = self.solr_url+'/'+collection_name

        query_params = {
            "q": phrase_query,
            "defType": "edismax",
            "qs": "100",
            "ps": "100",
            # "bf": "log(reddit_score)",
            "qf": "comment^{}".format(term_imp),
            "fl": "comment,score,url",
            "pf": "comment^{}".format(full_phrase_imp),
            "pf2": "comment^{}".format(bigram_imp),
            "pf3": "comment^{}".format(trigram_imp),
            "rows": 3000
        }
        # print(url)
        # print(query_params)
        response = requests.get(f'{url}/select', params=query_params)
        # print (response.json())
        search_results = response.json()['response']['docs']
        # print(search_results)
        return search_results[:K]


if __name__ == '__main__':
    # define solr endpoint
    solr_url = 'http://localhost:8983/solr'
    # define collection name
    collection_name = 'new_collection'
    # global headers definition
    headers = {'Content-type': 'application/json'}

    # query params
    # q - query
    # fl - fields to query
    # rows - max rows to query
    params = {
            'q': 'comment:on',
            'fl': 'comment_id,comment,score',
            'rows': 2
        }
    # define solr_ingest object
    data_ingest = solr_ingest(solr_url,collection_name,headers)
    # delete collection defined above
    data_ingest.delete_collection(collection_name)
    # create new collection using same name
    data_ingest.create_collection(collection_name,solr_var['data_schema'])
    # delete all data in the collection
    data_ingest.delete_data(collection_name)
    # read and process to save as json data
    data_dict = read_data("test3")
    data = process_json(data_dict)
    store_json(data,"text3_json")
    data = read_json("test3_json")
    # push data to the collection
    data_ingest.push_data(collection_name,data)
    # query data based on paramaters defined above
    search_data = data_ingest.query_data(params,collection_name)
    print(search_data)
    # update data based on rules defined
    # data_ingest.update_data(collection_name)
