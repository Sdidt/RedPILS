# RedPILS

IR Project

## Setup and Installation

1. Install Solr 9.1.1 and a Java>=13 <=19 and set up Java home variable appropriately.
2. Start Solr on cloud mode `bin/solr.cmd start -cloud`
3. `pip install -r requirements.txt` - Preferably on a virtual environment

### Setup for lazy building of DB

1. Start Solr in Cloud mode.
2. Check the "Test ConfigSet" request on this collection: https://interstellar-comet-46866.postman.co/workspace/New-Team-Workspace~65626761-938b-4a33-85be-f73afd0c8592/collection/9115718-98f32580-ff87-435d-9aa7-348344f0aec8?action=share&creator=9115718. Copy the request to your local (desktop) Postman; note the query params, and headers.Then in body, switch to binary mode, and select the zip file to upload. Then send request.
3. Check the "List configsets" on the same collection above. Run the request, and confirm that teh confg set "myConfigSet" has been added. If not, let me know.
4. Place backup_before_reindex.json and keywords.json in the outputs directory (/outputs from topmost directory of project).
5. Run lazy_build_db.py
