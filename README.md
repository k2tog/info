# Not for use in production environment!

# the Info API
A simple API endpoint returning "Info".

## Introduction
This code base is an interface for the Info API. "Info" provides information about the service running, it's name, version and git_commit_sha.
  * It is written in python and tested on python3.7. 
  * The API is exposed via `python flask`. 
  * Results are returned in JSON format and are formatted by python `flask jsonify`.
  * Refer https://flask.palletsprojects.com/en/1.1.x/ for more information. 

# Documentation
OpenAPI is located https://app.swaggerhub.com/apis/k355/Info/1.0.0

## Installing
To install Info API - use docker run on the host / cluster of your choice, using:
* run in detached mode using the -d flag
* container port is 5000 and can be bound to host using docker -p 80:5000 
* pass in the two environment variables: service_port and log_level

Example:

$ docker run -d -p 80:5000 --env SERVICE_PORT=8080 --env LOG_LEVEL=INFO --name info k2tog/info



## GET Requests:
HTTP GET to the host where the image is installed.  Example: __http://127.0.0.1:80/api/v1.0/info__


## Results:
In JSON format - the API returns service and environment information:
* service_name, version and git_commit_sha
* environment: log_level and service_port

_service_name and version seem to be GCP related, available when using cloud-build, for now, these values have been hardcoded as build-args._
_https://cloud.google.com/cloud-build/docs/configuring-builds/substitute-variable-values_





## The code
The code is hosted at https://github.com/k2tog/info. Clone the latest development version anonymously with: 

$ git clone git://github.com/k2tog/info.git



## Automated Build
On push of code to k2tog/info

Following a push to GitHub, the /hooks/build triggers an automated build on Dockerhub using the Dockerfile, creating and storing a docker image on Dockerhub.



## Unit Testing
To run the unit tests:

$ python test_app.py

_it will run the app and requires a ctrl-c to get results_

TODO: run the api/app in background mode while unit testing


## Semantics
Note: the service_port is handled as a string and the code accomodates this - should the port need to be returned as an integer, please refactor in app.py.

## No security!
SSL is not used as the self-signed certificates would create more issues than benefit for the purpose of this exercise.
OAuth keys have not been implemented but should be for production use / more sensitive data.
