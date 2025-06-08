# Databricks notebook source
# MAGIC %md Test runner for `pytest`

# COMMAND ----------

#!cp ../requirements.txt ~/.
#%pip install -r ~/requirements.txt

# %python
# %pip install -r ../requirements.txt
print("SKIPPING. IT is BROKEN")
# installing from requirements.txt failed here and trying to load in Compute.
# Will just install each individually without version and hope for the best...
%pip install attrs
%pip install cycler fontools iniconfig
%pip install kiwisolver matplotlib numpy packaging pandas pillow
%pip install pluggy py py4j pyarrow pyparsing pyspark
%pip install pytest python-dateutil pytz six tomli wget

# COMMAND ----------

# pytest.main runs our tests directly in the notebook environment, providing
# fidelity for Spark and other configuration variables.
#
# A limitation of this approach is that changes to the test will be
# cache by Python's import caching mechanism.
#
# To iterate on tests during development, we restart the Python process 
# and thus clear the import cache to pick up changes.
dbutils.library.restartPython()

import pytest
import os
import sys

# Run all tests in the repository root.
notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
repo_root = os.path.dirname(os.path.dirname(notebook_path))
os.chdir(f'/Workspace/{repo_root}')
%pwd

# Skip writing pyc files on a readonly filesystem.
sys.dont_write_bytecode = True

retcode = pytest.main([".", "-p", "no:cacheprovider"])

# Fail the cell execution if we have any test failures.
assert retcode == 0, 'The pytest invocation failed. See the log above for details.'
