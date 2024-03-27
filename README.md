## Manual

```
py -m venv venv

Window:
venv\Scripts\Activate

MacOS:
venv\bin\activate

pip uninstall -r requirements.txt -y
pip install -r requirements.txt

```

## Step-by-step

### Fine Tuning with specific data
- Generate the new folder at src\test\regression\regression_testxxx
Copy and paste the files at here

- Fine Tuning
```
py .\finetuning.py --payload_dir="payload_dir" 

example: 
py .\finetuning.py --payload_dir="./test/regression/regression_testxxx/payload/finetuning_payload.json"  
```

- After fine tuning, you will get the model id, you can check the model_id at console or data_path/generated_data/model.txt
- Please check the "./test/regression/regression_testxxx/payload/chatting_payload.json"
After successfully complete the fine tuning, will update the model_id automatically.
If you want to update this, please change the model_id with your specific id.

### Conversational Agent
```
py .\chatting.py --payload_dir="payload_dir" --question="question"

example: 
py .\chatting.py --payload_dir="./test/regression/regression_testxxx/payload/chatting_payload.json" --question="what's the golf?"
```

You will see the result at console.


### Full process: data preprocessing -> pdf to image -> image to text -> fine tuning
Please install requirement again.

```
pip install -r requirements.txt

py main.py
```

### Create, Delete, Check API Key
- Create API Key
```
py .\create_api_key.py --payload_dir="payload_dir" --user="user email" --title=[Optional] --description=[Optional]

example:
py .\create_api_key.py --payload_dir="./test/regression/regression_testxxx/payload/mongodb_payload.json" --user="user@gmail.com" --title="title" --description="description"
```

- Delete API Key
```
py .\delete_api_key.py --payload_dir="payload_dir" --user="user email" --api_key="api key"

example:
py .\delete_api_key.py --payload_dir="./test/regression/regression_testxxx/payload/mongodb_payload.json" --user="user@gmail.com" --api_key="api_key"
```

- Check API key
```
py .\check_api_key.py --payload_dir="payload_dir" --user="user email" --api_key="api key"

example:
py .\check_api_key.py --payload_dir="./test/regression/regression_testxxx/payload/mongodb_payload.json" --user="user@gmail.com" --api_key="api_key"
```

### MongoDB:
{
    "mongo_uri": "mongodb+srv://{user_name}:{password}@cluster0.ill5gnu.mongodb.net",
    "db_name": "oridosai",
    "collection_name": "apis"
}