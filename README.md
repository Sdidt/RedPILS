# RedPILS

An Efficient Information Retrieval System for the Indian Political Sentiments on Reddit. 

## Setup and Installation

### Database

1. Install Solr 9.1.1 and a Java>=13 <=19 and set up Java home variable appropriately.
2. Start Solr on cloud mode :

Windows: 
```
bin/solr.cmd start -cloud
```
Linux: 
```
bin/solr start -cloud
```
By default, the solr will be serving on `http://localhost:8983` if available. 

#### Setup for lazy building of DB

1. Start Solr in Cloud mode.
2. Check the "Test ConfigSet" request on this collection: https://interstellar-comet-46866.postman.co/workspace/New-Team-Workspace~65626761-938b-4a33-85be-f73afd0c8592/collection/9115718-98f32580-ff87-435d-9aa7-348344f0aec8?action=share&creator=9115718. Copy the request to your local (desktop) Postman; note the query params, and headers.Then in body, switch to binary mode, and select the zip file to upload. Then send request.

Alternatively note the request details below, and run the request on Postman:
Type: GET

```
http://localhost:8983/solr/admin/configs?action=UPLOAD&name=myConfigSet&overwrite=true
```

Headers:

    Content-Type = application/octet-stream

Body: Binary Mode: Zip File Upload

3. Check the "List configsets" on the same collection above. Run the request, and confirm that the confg set "myConfigSet" has been added. 
4. Place backup_before_reindex.json and keywords.json in the `outputs` directory of the root folder.
5. Run lazy_build_db.py

#### Python Codebase for Building Database
1. Install Requirements on a Python==3.9 or 3.10 environment.
``` 
pip install -r requirements.txt 
```

2. Create a `.env` file in the root directory. A sample can be found in `.env.sample`. Ensure that the correct API Keys (reddit) and Syspath are used.

3. Run `main.py`
```
python main.py
```

### Flask App
1. Install Requirements on a Python==3.9 or 3.10 environment.
``` 
pip install -r requirements.txt 
```
2. Create a `.env` file in the root directory. A sample can be found in `.env.sample`. Ensure that the correct API Keys (reddit) and Syspath are used. 

3. Export the Flask App from the root directory using:
``` 
export FLASK_APP=flask_app/app.py 
```
4. Start the Flask Server: 
``` 
flask run 
```

The app should be serving on `http:\\localhost:5000`


### React App: User Interface

1. Install the dependencies

```
npm install
```

2. Start the Server
```
npm start
```
The app should be serving on `http:\\localhost:3000`