# aws-cdk-factorial-deployment



## to make it go

```bash
#Create cloud9 environment via aws.
#Check your python version python --version 
git clone https://github.com/srdrcn/cdk-infra-ecs.git
cd cdk-infra-ecs
virtualenv --python=/usr/bin/python3.7 venv
#activate venv.
source venv/bin/activate
pip install -r requirements.txt
# if you've not used cdk before you may need to bootstrap it into
# your aws environment (creates s3 bucket for cloud formation templates, etc)

cdk bootstrap 

# test run to see if it creates a template
cdk synth

# if it's good, then deploy
cdk deploy

# it should warn you about upcoming changes and ask you to accept (a security precaution)
# at the end of the deployment you'll get outputs to the two loadbalanced services
# copy the url for the 'frontend' one, toss it into your browser and you should see the demo page

# clean up with a
cdk destroy
```
