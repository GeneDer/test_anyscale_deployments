# ray job submit --runtime-env-json='{"working_dir": "/Users/gene/workspace/test_anyscale_deployments/test_issue_44467"}' -- python folder2/main.py
# ray job submit --runtime-env-json='{"working_dir": "'$HOME'/workspace/test_anyscale_deployments/test_issue_44467"}' -- python folder2/main.py
import sys
import ray


sys.path.append('folder1/subfolder1')
from foo import method1


@ray.remote
def run_task():
    method1()


if __name__ == "__main__":
    ray.init()

# ==================================
# ray job submit --working-dir /Users/gene/workspace/test_anyscale_deployments/test_issue_44467 -- python folder2/main.py
# import sys
#
# sys.path.append('folder1/subfolder1')
# # from folder1.subfolder1.foo import method1  # <- this also works
# from foo import method1
#
#
# method1()
