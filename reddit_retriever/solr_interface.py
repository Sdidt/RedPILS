import requests
import json

class solr_ingest():
    def __init__(self,solr_url,collection_name,headers,data) -> None:
        self.solr_url = solr_url
        self.collection_name = collection_name
        self.headers = headers
        self.data = data

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

    def create_collection(self,collection_name,schema):
        collection_exists = self.check_collection_exists(collection_name)
        if(collection_exists):
            print(f'Collection "{collection_name}" exists')
            return
        else:
            print(f'Collection "{collection_name}" does not exist')

        config_name = 'my_config'
        num_shards = 2
        replication_factor = 2

        request_data = {
            'action': 'CREATE',
            'name': collection_name,
            'numShards': num_shards,
            'replicationFactor': replication_factor,
            'configName': config_name
        }

        response = requests.get(f'{self.solr_url}/admin/collections', params=request_data)
        if response.status_code == 200:
            print(f'Collection "{collection_name}" created successfully')
        else:
            print(f'Error creating collection: {response.text}')

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
        else:
            print(f'Error deleting the collection: {response.text}')

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


    def push_data(self,collection_name):
        url = self.solr_url+'/'+collection_name

        doc_json = json.dumps(self.data)
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

if __name__ == '__main__':
    # define solr endpoint
    solr_url = 'http://localhost:8983/solr'
    # define collection name
    collection_name = 'new_collection'
    # global headers definition
    headers = {'Content-type': 'application/json'}
    # dummy data to be ingested into solr database
    data = [
            {'id': '1', 'title': 'Document 1', 'text': 'This is the first document'},
            {'id': '2', 'title': 'Document 2', 'text': 'This is the second document'},
            {'id': '3', 'title': 'Document 3', 'text': 'This is the third document'}
        ]
    # query params
    # q - query
    # fl - fields to query
    # rows - max rows to query
    params = {
            'q': 'text:document',
            'fl': 'id,title',
            'rows': 10
        }
    fields = [
            {"name": "id", "type": "string"},
            {"name": "title", "type": "text_en"},
            {"name": "content", "type": "text_en"},
            ]

    # define solr_ingest object
    data_ingest = solr_ingest(solr_url,collection_name,headers,data)
    # delete collection defined above
    data_ingest.delete_collection('my_collection')
    # create new collection using same name
    data_ingest.create_collection(collection_name,fields)
    # delete all data in the collection
    data_ingest.delete_data(collection_name)
    # push data to the collection
    data_ingest.push_data(collection_name)
    # query data based on paramaters defined above
    search_data = data_ingest.query_data(params,collection_name)
    print(search_data)
    # update data based on rules defined inside the function
    data_ingest.update_data(collection_name)
