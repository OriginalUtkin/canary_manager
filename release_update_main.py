#!/usr/bin/python
from canary_hitman.clients.gitlab import GitlabClient
import os
import re
from typing import List, Dict


def get_build_job_id(jobs: List[Dict], branch_ref: str) -> int:
    for job in jobs:
        if job["ref"] == branch_ref and job["name"] == "build":
            return job["id"]


if __name__ == "__main__":
    token = os.environ["GITLAB_API_TOKEN"]
    gitlab_base_path = os.environ["GITLAB_PATH"]
    filename_to_update = os.environ["FILENAME_TO_UPDATE"]
    build_branch_reference = os.environ["BUILD_BRANCH_REFERENCE"]
    target_branch_reference = os.environ["TARGET_BRANCH_REFERENCE"]

    project_id_merge_request = int(os.environ["PROJECT_ID_TO_UPDATE"])
    project_id_build = int(os.environ["PROJECT_ID_TO_BUILD"])

    cli = GitlabClient(gitlab_base_path, token)

    jobs = cli.request_api_get(path=f"/projects/{project_id_build}/jobs")
    recent_job_id = get_build_job_id(jobs, build_branch_reference)
    job_trace = cli.request_api_get(path=f"/projects/{project_id_build}/jobs/{recent_job_id}/trace", json_output=False)

    image_hash = re.findall(r"Successfully tagged (registry.skypicker.com:5005[/a-z-]+:[0-9a-z]{40}-chrome)", job_trace)[0]

    branch_name = f"update_docker_to_{image_hash[-1:-41:-1]}"

    cli.create_branch(project_id=project_id_merge_request, branch=branch_name, ref=target_branch_reference)
    cli.update_file(
        project_id=project_id_merge_request,
        branch=branch_name,
        message="Bump latest automation image",
        file_name="Automation-Modules-Master-Dockerfile",
        file_content=f"FROM {image_hash}\n"
    )
    cli.create_merge_request(
        repository_id=project_id_merge_request,
        source_branch=branch_name,
        target_branch=target_branch_reference,
        title=f"Update {filename_to_update}"
    )