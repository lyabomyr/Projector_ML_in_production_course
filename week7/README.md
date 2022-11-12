### Feature store


#### PR1 PR: write instructions on how to setup feast feature store (you can choose another feature store)
Install and run Feast



1. Install the Feast SDK and CLI using pip:
```
pip install wheel
pip install feast
```

2.  Create a feature repository
```
feast init week7
cd week7/feature_repo
```
`
* data/ contains raw demo parquet data
* example_repo.py contains demo feature definitions
* feature_store.yaml contains a demo setup configuring where data sources are
* test_workflow.py showcases how to run all key Feast commands, including defining, retrieving, and pushing features. You can run this with python test_workflow.py
`

example feature store yaml

```
project: my_project
# By default, the registry is a file (but can be turned into a more scalable SQL-backed registry)
registry: data/registry.db
# The provider primarily specifies default offline / online stores & storing the registry in a given cloud
provider: local
online_store:
  type: sqlite
  path: data/online_store.db
entity_key_serialization_version: 2
```

example repo.py

3. Register feature definitions and deploy your feature store

The feature_store.yaml file configures the key overall architecture of the feature store.
Valid values for provider in feature_store.yaml are:
local: use a SQL registry or local file registry. By default, use a file / Dask based offline store + SQLite online store

The `apply` command scans python files in the current directory for feature view/entity definitions, registers the objects, and deploys infrastructure. In this example, it reads example_repo.py and sets up SQLite online store tables. Note that we had specified SQLite as the default online store by configuring `online_store` in `feature_store.yaml`.


Definitions and deploy for feature store in python file (by default definitions is already setupped in python file)

run command:

```
feast apply
```

In result u'll receive
```
Created entity driver
Created feature view driver_hourly_stats
Created feature view driver_hourly_stats_fresh
Created on demand feature view transformed_conv_rate_fresh
Created on demand feature view transformed_conv_rate
Created feature service driver_activity_v1
Created feature service driver_activity_v3
Created feature service driver_activity_v2
Created sqlite table week7_driver_hourly_stats_fresh
Created sqlite table week7_driver_hourly_stats
```

the fs was created  and  we can see UI option - for this  need execute command:

`feast ui`


#### PR: 2 and 3 train and inference
Notion added example from documentation


for run training pipeline

move to fs directory and run python training file

```
python3 training.py
```

for run inference:

move to fs directory and run python training file

```
python3 inference.py
```

