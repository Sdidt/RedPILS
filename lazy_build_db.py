from utils.constants import keywords, solr_var
from utils.helpers import *
from reddit_retriever.solr_interface import solr_ingest

def retain_all_except_id_version(list_data):
    return [
        {
            k: v for k, v in doc.items() if k not in ["id", "_version_"]
        }
        for doc in list_data
    ]

#--------------------solr init - comments data--------------------#
data_ingest = solr_ingest(solr_var["solr_url"],solr_var['data_collection_name'],solr_var['headers'])
# data_ingest.upload_configset(solr_var["configset_zip_path"], solr_var["configset_name"], "true")
# data_ingest.define_schema(solr_var['data_collection_name'], solr_var['data_schema'])
data_ingest.delete_collection(solr_var['data_collection_name'])
data_ingest.create_collection(solr_var['data_collection_name'], solr_var['data_schema'], solr_var['data_unique_key'], solr_var['filtered_text_type'])
# data_ingest.replace_schema(solr_var['data_collection_name'], solr_var['data_schema'])
data_ingest.delete_data(solr_var['data_collection_name'])
data = read_json("backup_before_reindex")
data = retain_all_except_id_version(data)
data_ingest.push_data(solr_var["data_collection_name"], data)
#-------------------------------------------------#


keyword_ingest = solr_ingest(solr_var["solr_url"],solr_var['keyword_collection_name'],solr_var['headers'])
keyword_ingest.delete_collection(solr_var['keyword_collection_name'])
keyword_ingest.create_collection(solr_var['keyword_collection_name'],solr_var['keyword_schema'],solr_var['keyword_unique_key'], solr_var['filtered_text_type'])
keyword_ingest.delete_data(solr_var['keyword_collection_name'])
keywords = read_json("keywords")
keywords = retain_all_except_id_version(keywords)
keyword_ingest.push_data(solr_var['keyword_collection_name'], keywords)
# #-------------------------------------------------#
