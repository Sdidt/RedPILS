import os
import json
import pickle
import datetime
from pprint import pprint

from models.comment import Comment


def store_raw_data(self, sub_data):
    with open("outputs/{}_raw.txt".format(self.output_filename), "w", encoding='utf-8') as f:
        pprint(sub_data, f)

def store_data(sub_data,output_filename):
    isExist = os.path.exists('./outputs')
    if not isExist:
        os.makedirs('./outputs')

    with open("outputs/{}.txt".format(output_filename), "wb") as f:
        pickle.dump(sub_data, f)

def read_data(output_filename):
    try:
        with open("outputs/{}.txt".format(output_filename), "rb") as f:
            print("File exists!")
            sub_data = pickle.load(f)
    except: 
        sub_data = []
    return sub_data

def read_json(file_name):
    with open('outputs/{}.json'.format(file_name)) as f:
        data = json.load(f)
    return data

def store_json(data,file_name):
    json_res = process_json(data)
    with open('outputs/{}.json'.format(file_name), 'w') as f:
        json.dump(json_res , f)

def convert_to_datetime(timestamp):
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    iso_format = dt_object.isoformat()
    return iso_format

def process_json(data: list[Comment]):
    json_ex = []
    for comment in data:
        json_ex.append(
            {
                "submission_id": comment.submission_id,
                "submission_title": comment.submission_title.decode('utf-8'),
                "subreddit_id": comment.subreddit_id,
                "subreddit_name": comment.subreddit_name,
                "id": comment.id,
                "comment": comment.comment.decode('utf-8'),
                "timestamp": convert_to_datetime(comment.timestamp),
                "url": comment.url,
                "score": comment.score,
                "redditor_id": comment.redditor_id
            }
        )
    # for key in data:
    #     new_dict = {'subreddit':key}
    #     for post_key in data[key]:
    #         new_dict['post_id'] = post_key
    #         for comments in data[key][post_key]['comments']:
    #             new_dict.update(comments.__dict__)
    #             new_dict['comment'] = new_dict['comment'].decode('utf-8')
    #             new_dict['timestamp'] = convert_to_datetine(new_dict['timestamp'])
    #             new_dict['comment_id'] = new_dict.pop('id')
    #             json_ex.append(new_dict)
    return json_ex