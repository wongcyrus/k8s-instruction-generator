# k8s-instruction-generator
According to the game character background to generate conversation and k8s instruction.


## Setup for AWS Academy Leaner Lab 
Since AWS Academy does not support Amazon Bedrock, we need to setup 2 AWS profile

1. Account with Amazon Bedrock
```
aws configure --profile genai
```
2. AWS Academy Learner Lab Account
```
aws configure --profile leaner_lab
aws configure set aws_session_token <Session Token>
```

Set both profile with
```
Default region name [None]: us-east-1
Default output format [None]: json
```

