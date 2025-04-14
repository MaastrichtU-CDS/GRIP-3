# Example project vantage6 for GRIP3

This is a basic project showing an example federated algorithm It includes all the files necesary to build and run an
algorithm

## Requirements

The following needs to be installed:

- Python 3.10
- Vantage6 4.9.1 (to run in practice)
- Docker

## Local testing the infrastructure
To setup a local development algorithm for Vantage6, and to use the mock client for testing purposes, the following steps will get you going.

### 1.: Start local test infrastructure

Open the root folder of **this repository**, and run the command `docker compose up -d`. This will create a local instance of Coder (Visual Studio Code in the Browser), including all Vantage6 dependencies.
You can open this instance at [http://localhost:8080/?folder=/home/coder/workspace](http://localhost:8080/?folder=/home/coder/workspace) with the password `12345`.

If you want to change some settings (e.g. the password), you can edit [./docker-compose.yaml](docker-compose.yaml).

### 2.: Run the mock tests

In the VSCode browser session, open a terminal window (using `` ctrl + ` ``) and navigate to the test folder (`cd test`).

In this test folder, you can execute the python script using the following command: `python MockTest.py`.
The result should be similar as the result below

```logs
[info ] - Initializing nodes
info > Mocking waiting for results
info > Mocking waiting for results
info > Mocking waiting for results
info > Mocking waiting for results
- incidentie D88 per 1000 patient jaren: [0.0]
[info ] - Initializing nodes
info > Mocking waiting for results
info > Mocking waiting for results
info > Mocking waiting for results
info > Mocking waiting for results
- incidentie D98 per 1000 patient jaren: [0.02]
[info ] - Initializing nodes
info > Mocking waiting for results
info > Mocking waiting for results
info > Mocking waiting for results
info > Mocking waiting for results
- incidentie H71 per 1000 patient jaren: [0.15]
[info ] - Initializing nodes
info > Mocking waiting for results
info > Mocking waiting for results
info > Mocking waiting for results
info > Mocking waiting for results
-puntincidentie H71 per 1000 patient jaren: [0.07]
[info ] - Initializing nodes
info > Mocking waiting for results
info > Mocking waiting for results
info > Mocking waiting for results
info > Mocking waiting for results
Average BMI: [28]
```

## Creating a demo network

To create a local demo network use the command: ``v6 dev create-demo-network``. The network can be started using the
command ``v6 dev start-demo-network``. Do bear in mind to explicitly stop the network using ``v6 dev stop-demo-network``
. It may be necesary to manually stop certain nodes as well.

## Creating the boilerplate for a vantage6 algorithm

Creating the boilerplate code can be done using the command ``v6 algorithm create``. This will start a small wizard in
the command line that will help fill out the basic things needed for your algorithm.

## Compiling a Docker Image:

`pushscript.sh` contains the instructions to create a docker image for this example. Be aware this script pushes to the
repo `fvandaalen` on `hub.docker.com` and requires a password.

## Running the algorithm

The algorithm can be run using one of the two test scripts contained in this repository. There is a test script using
the mockclient, which can be debugged in an IDE. There is also a test script for running the algorithm on a proper
network. In this case debugging becomes significantly harder. It is important to note that the mockclient is currently
intended for horizontally partitioned scenarios as it cannot mock the VPN.

Running the algorithm in a "real" enviroment requires a similar script, however, the mockclient needs to be swapped for
a genuine client with the correct ip-adresses and passwords etc.

## How to incorperate other programming languages

Other programming languages can be used within vantage6. To do this simply use the boilerplate code to start the "real"
program. For example, a subtask that needs to run a JAR file that contains the federated calculations will look as
follows:

```
import subprocess
import os

from vantage6.algorithm.tools.decorators import data
from vantage6.algorithm.tools.util import get_env_var

from vantage6.common import info

@data(1)
def init(*args, **kwargs):
    info('Starting java server')
    subprocess.run(['java', '-jar', _get_jar_path()])

def _get_jar_path():
    return os.environ.get('JAR_PATH')
```

## Example algorithm

The example algorithm is very simple and consists of the following. The algorithm assumes the data is split up
vertically (the dataset belonging to each party contains a different population, but the same attributes). The algorithm
is called with the following call:

```
central_task = client.task.create(
    input_={'method': 'grip3IncidentieTest',
            'args': [org_ids, {'attribute': <attribute_name>, 'value': <attribute_value>}, {'attribute': <date_attribute_name>, 'value': <date_value>}]},
    organizations=[org_ids[0]],
)
```

This call counts the number of records for which attribute `<attribute_name>` has value `<attribute_value>` and for
which attribute `<date_attribute_name>` lays on or after `<data_value>`.

Given the relative simple nature of this algorithm the only privacy preserving measure that has been taken is a standard
disclosure control check. A result is only returned if a party locally has 10 or more record that fullfill the listed
criteria.

It is important to note that this particular algorithm could be used to partially reconstruct the joint dataset using
repeat queries with slight variations (e.g. moving the date by 1 day in subsequent request).

The image can be found here: `https://hub.docker.com/r/fvandaalen/grip3`

The image name is `fvandaalen/grip3`