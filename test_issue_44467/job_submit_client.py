from ray.dashboard.modules.job.sdk import JobStatus, JobSubmissionClient
import os

client = JobSubmissionClient("http://127.0.0.1:8265")
entrypoint = "python folder2/main.py"
HOME = "/Users/gene"
client.submit_job(
    entrypoint=entrypoint,
    # Working dir
    runtime_env={
        "working_dir": f"{os.environ['HOME']}/workspace/test_anyscale_deployments/test_issue_44467",
    }
)
