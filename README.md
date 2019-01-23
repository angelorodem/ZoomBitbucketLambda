
# Integrating Zoom Meetings with Bitbucket using Python and AWS Lambda
This is a example of integration of Zoom Incoming webhooks with bitbucket webhooks on a AWS Lambda

To use this code to integrate Zoom Meetings and Bitbucket, you need to do the following:

**Zoom**
 - Go to zoom, and click settings, then click on enable advanced features
 - Next, click on messaging addons and create a incoming weebhooks
 - When finished, you'll have a endpoint URL and a key
 
**AWS**
 - Create a lambda function (see aws tutorials for better explanation)
 - You may need to create a role (Full lambda, KMS (if using encripted enviroment variables), and full S3, if storing logs and code there)
 - Use a API Gateway as the trigger
 - Put the code of this repo in the lambda
 - Configure enviroment variables as explained in the code (create enviroment variables with the zoom webhooks URL/Key)

**API Gateway**
 - As default aws creates a ANY resource when adding a trigger to a lambda, delete it and create a POST resource
 - Create the POST resource as a lambda function
 - By default API Gateways don't forward request Headers, so you have to modify the Integration request as explained [Here](https://aws.amazon.com/premiumsupport/knowledge-center/custom-headers-api-gateway-lambda/) 

**BitBucket**
- Go to the **repo** settings and click webhooks
- Add a new webhook with the following custom triggers in the **Pull request** section: *Created*, *Approved*, *Merged*, *Comment created*
- Add the AWS API Gateway link  to the bitbucket weebhook url

that should be it


Note, if using encripted enviroment variables you may need change a few things, like adding a code to decript using the kms


    WEBHOOK_URL_ENC = os.environ['ZOOM_INCOMING_WH_URL']
    WEBHOOK_URL_DEC = boto3.client('kms').decrypt(CiphertextBlob=b64decode(WEBHOOK_URL_ENC))['Plaintext'].decode()
    
    ZOOM_KEY_ENC = os.environ['ZOOM_INCOMING_WH_PW']
    ZOOM_KEY_DEC = boto3.client('kms').decrypt(CiphertextBlob=b64decode(ZOOM_KEY_ENC))['Plaintext'].decode() # bytes to str

