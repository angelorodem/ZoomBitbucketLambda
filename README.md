
# Integrating Zoom Meetings with Bitbucket using Python and AWS Lambda
This is a example of integration of Zoom Incoming webhooks with bitbucket webhooks on a AWS Lambda

To use this code to integrate Zoom Meetings and Bitbucket, you need to do the following:

**Zoom**
 - Go to zoom, and click settings, then click on enable advanced features
 - Next, click on messaging addons and create a incoming weebhooks
 - When finished, you'll have a endpoint URL and a key
 
**AWS**
 - Create a lambda function (see aws tutorials for better explanation)
 - You may need to create a role
 - Use a API Gateway as the trigger
 - Put the code of this repo in the lambda
 - Configure enviroment variables as explained in the code (create enviroment variables with the zoom webhooks URL/Key)

**API Gateway**
 - As default aws creates a ANY resource, delete it and create a POST resource
 - Create the POST resource as as a lambda function
 - By default API Gateways don't forward request Headers, so you have to modify the Integration request as explained [Here](https://aws.amazon.com/premiumsupport/knowledge-center/custom-headers-api-gateway-lambda/) 

