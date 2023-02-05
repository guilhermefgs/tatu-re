# tatu-re
Tatu Recommendation Engine

## Installation

Clone this repository.

It is recommended to use a python (>= 3.7) virtual environment for the next steps.

Execute the following commands
```bash
$ cd tatu-re
$ pip install -e .
```

To deploy the dashboard online, execute the following commands in the main folder of the repository

```bash
$ gclond init
$ gcloud app deploy app.yaml
```