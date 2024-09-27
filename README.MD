#Example project vantage6 for GRIP3

This is a basic project showing an example federated algorithm
It includes all the files necesary to build and run an algorithm

## Requirements
The following needs to be installed:
- Python 3.10
- Vantage6 4.7.0
- Docker

## Creating a demo network
To create a local demo network use the command: ``v6 dev create-demo-network``.
The network can be started using the command ``v6 dev start-demo-network``. 
Do bear in mind to explicitly stop the network using ``v6 dev stop-demo-network``.
It may be necesary to manually stop certain nodes as well.

## Creating the boilerplate for a vantage6 algorithm
Creating the boilerplate code can be done using the command ``v6 algorithm create``.
This will start a small wizard in the command line that will help fill out the basic things needed for your algorithm.

## Running the algorithm
The algorithm can be run using one of the two test scripts contained in this repository.
There is a test script using the mockclient, which can be debugged in an IDE.
There is also a test script for running the algorithm on a proper network. In this case debugging becomes significantly harder.
It is important to note that the mockclient is currently intended for horizontally partitioned scenarios as it cannot mock the VPN.

## How to incorperate other programming languages
Other programming languages can be used within vantage6.
To do this simply use the boilerplate code to start the "real" program.
For example, a subtask that needs to run a JAR file that contains the federated calculations will look as follows:
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