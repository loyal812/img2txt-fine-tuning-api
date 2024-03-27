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

### AWS EC2

- Launch Instance
![Alt text](./images/image.png)

- Instance Setting
![Alt text](./images/image-1.png)

![Alt text](./images/image-2.png)

![Alt text](./images/image-3.png)

![Alt text](./images/image-4.png)

![Alt text](./images/image-5.png)

- Elastic IP Setting
![Alt text](./images/image-7.png)

![Alt text](./images/image-8.png)

![Alt text](./images/image-9.png)

![Alt text](./images/image-10.png)

![Alt text](./images/image-11.png)

- Security Group Setting
![Alt text](./images/image-12.png)

![Alt text](./images/image-13.png)

![Alt text](./images/image-14.png)

![Alt text](./images/image-15.png)

- Connect to Instance
![Alt text](./images/image-16.png)

![Alt text](./images/image-17.png)

### Project Setting
```
sudo su
apt update

apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-cache policy docker-ce
apt install docker-ce

apt install docker-compose

apt install make

apt install nginx

cd /var/www

git clone https://github.com/oridosai/img2txt-fine-tuning-api.git

cd img2txt-fine-tuning-api

chmod -R 777 /var/www/img2txt-fine-tuning-api

nano .env

Please copy your local env data at this file and save.

OPENAI_API_KEY=
MATHPIX_APP_ID=
MATHPIX_APP_KEY=
MONGODB_USERNAME=
MONGODB_PASSWORD=
MONGODB_CLUSTER_NAME=

docker-compose up -d
```

### done 
host your elastic ip 

http://{your elastic ip}:5000/create_api 
POST
```
{
  "user": "",
  "title": "",
  "description": "",
  "data_id": ""
}
```

http://{your elastic ip}:5000/delete_api 
POST
```
{
  "api_key": "",
  "user": "",
  "data_id": ""
}
```

http://{your elastic ip}:5000/check_api 
POST
```
{
  "api_key": "",
  "user": "",
  "data_id": ""
}
```

http://{your elastic ip}:5000/finetuning 
POST
```
{
  "api_key": "",
  "user": "",
  "data_id": ""
}
```

http://{your elastic ip}:5000/conversation 
POST
```
{
  "api_key": "",
  "user": "",
  "data_id": "",
  "question": "hi"
}
```
