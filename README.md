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

## Guide for end-to-end process of fine tuning
This guide provides step-by-step instructions for setting up a MongoDB Atlas account, connecting to a MongoDB cluster using Compass, and configuring an AWS EC2 instance for your project and running end-to-end if fine tuning using OpenAI.

### Prerequisites
- MongoDB Atlas account
- AWS account
    
### Step 1: MongoDB Atlas Setup
- Create MongoDB Atlas Account: [Sign up at MongoDB Atlas]([https://www.google.com](https://www.mongodb.com/atlas/database))
- Gather Environment Data: After logging in, navigate to the dashboard to find your environment details and deployment details.
![Alt text](./images/image-18.png)

![Alt text](./images/image-19.png)

- Connect to MongoDB Cluster: Use the MongoDB Atlas interface to connect to your MongoDB cluster (Create Database User and choose a connection method).
![Alt text](./images/image-20.png)

- Use MongoDB Compass: To connect to your application select Compass for an enhanced GUI experience for exploring and managing your data.
![Alt text](./images/image-21.png)

- Securely store your MongoDB username, password, and cluster ID in a `.env` file.
![Alt text](./images/image-22.png)

- Go to the Database Access and update the password by clicking on the Edit button.
![Alt text](./images/image-23.png)

![Alt text](./images/image-24.png)

![Alt text](./images/image-25.png)

![Alt text](./images/image-26.png)

- Use autogenrate secure password button to generate a new password, copy the password, and update it in the `.env` file and click on Add User button.
![Alt text](./images/image-27.png)

![Alt text](./images/image-28.png)

The setup for MongoDB atlas is ready.

### Step 2: AWS EC2 Setup

- Launch an EC2 Instance: Log in to your AWS account and create a new EC2 instance.
![Alt text](./images/image.png)

Use the following settings for instance setup:
- Select OS and instance type: Choose Ubuntu as your operating system. Pick the desired instance type based on your needs.
![Alt text](./images/image-1.png)

- Generate a new key pair: Generate a new key pair, name it, and save it securely.
![Alt text](./images/image-2.png)

![Alt text](./images/image-3.png)

- Storage Configuration: Configure your instance with the required storage (e.g., 50 GB). Launch the EC2 instance. Make sure to store the genrated key pair file (.pem file).
![Alt text](./images/image-4.png)

![Alt text](./images/image-5.png)

- Elastic IP Setting: Create an Elastic IP by allocating a new Elastic IP address in the AWS dashboard. Then, associate Elastic IP by linking the Elastic IP address to your new EC2 instance.
![Alt text](./images/image-7.png)

![Alt text](./images/image-8.png)

![Alt text](./images/image-9.png)

![Alt text](./images/image-10.png)

![Alt text](./images/image-11.png)

- Security Group Setting: Edit the security group settings by modify the inbound rules. Add rules for Custom TCP with a port range of 5000, HTTP, HTTPS, etc.
![Alt text](./images/image-12.png)

![Alt text](./images/image-13.png)

![Alt text](./images/image-14.png)

![Alt text](./images/image-15.png)

- Connect to EC2 Instance: Follow AWS instructions to securely connect to your EC2 instance.
![Alt text](./images/image-16.png)

![Alt text](./images/image-17.png)



### Step 3: Environment Setup and Project Execution
This section guides you through setting up your environment and running the project on an AWS EC2 instance using Docker.

#### Prerequisites
- AWS EC2 instance running Ubuntu
- Root or sudo privileges

#### Setup steps
```bash
# Gain Root Access
sudo su
# Update Package List                   
apt update 

# Install Required Packages
apt install apt-transport-https ca-certificates curl software-properties-common

# Add Docker Repository and Install Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-cache policy docker-ce
apt install docker-ce

# Install Docker Compose, Make, and Nginx
apt install docker-compose make nginx

# Go to /var/www
cd /var/www

# Clone the GitHub Repository
git clone https://github.com/oridosai/img2txt-fine-tuning-api.git

# Navigate to the Project Directory
cd img2txt-fine-tuning-api

# Set Permissions
chmod -R 777 /var/www/img2txt-fine-tuning-api

# Create and Edit Environment File
nano .env

# Enter your environment variables here
# Copy your local env data at this file and save.
OPENAI_API_KEY=
MATHPIX_APP_ID=
MATHPIX_APP_KEY=
MONGODB_USERNAME=
MONGODB_PASSWORD=
MONGODB_CLUSTER_NAME=

# Launch the Application with Docker Compose
docker-compose up -d

# Updating and Re-running the Project
# Pull Updates from Repository
git pull origin dev 
# Check Running Containers        
docker ps       
# Stop and Remove the Container             
docker stop container_id
docker rm container_id
# Restart the Application
docker-compose up -d         
```

### done 
host your elastic ip 
http://{your elastic ip}:5000/total  
create_api + finetuning + chatting

```
py .\script\total_process.py --api_url "api_url" --data_id "regression013" --user "user email" --title "title" --description "description" --question "hi"
```
- Postman
![Alt text](./images/image-34.png)

- curl
```
curl -X 'POST' \
  'http://localhost:5000/total' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user": "",
  "title": "",
  "description": "",
  "data_id": "",
  "question": "hi"
}'
```

http://{your elastic ip}:5000/create_api 
```
py .\script\create_api_key.py --api_url "api_url" --data_id "regression013" --user "user email" --title "title" --description "description"
```
- Postman
![Alt text](./images/image-29.png)

- curl
```
curl -X 'POST' \
  'http://18.118.73.220:5000/create_api' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user": "",
  "title": "",
  "description": "",
  "data_id": ""
}'
```

http://{your elastic ip}:5000/delete_api 
```
py .\script\delete_api_key.py --api_url "api_url" --data_id "regression013" --user "user email" --api_key "api key"
```
- Postman
![Alt text](./images/image-30.png)

- curl
```
curl -X 'POST' \
  'http://18.118.73.220:5000/delete_api' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "api_key": "",
  "user": "",
  "data_id": ""
}'
```

http://{your elastic ip}:5000/check_api 
```
py .\script\check_api_key.py --api_url "api_url" --data_id "regression013" --user "user email" --api_key "api key"
```
- postman
![Alt text](./images/image-31.png)

- curl
```
curl -X 'POST' \
  'http://18.118.73.220:5000/check_api' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "api_key": "",
  "user": "",
  "data_id": ""
}'

```

http://{your elastic ip}:5000/finetuning 
```
py .\script\finetuning.py --api_url "api_url" --data_id "regression013" --user "user email" --api_key "api key"
```
- postman
![Alt text](./images/image-33.png)

- curl
```
curl -X 'POST' \
  'http://18.118.73.220:5000/finetuning' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "api_key": "",
  "user": "",
  "data_id": ""
}'
```

http://{your elastic ip}:5000/conversation 
```
py .\script\conversation.py --api_url "api_url" --data_id "regression013" --user "user email" --api_key "api key" --question "hi"
```
- postman
![Alt text](./images/image-32.png)

- curl
```
curl -X 'POST' \
  'http://18.118.73.220:5000/conversation' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "api_key": "",
  "user": "",
  "data_id": "",
  "question": "hi"
}'
```
