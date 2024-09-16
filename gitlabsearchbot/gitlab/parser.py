import asyncio
from typing import Optional
from logging import getLogger

from gitlab.models import GitProject, GitBlob
from gitlab.gitlab_api import GitGraphQL
from settings import settings
from gitlab import querys as q


logger = getLogger(__name__)


class GitParser:

    def __init__(self):
        self.git_api = GitGraphQL()
        self.projects: Optional[list[GitProject]] = []
        self._projects: Optional[list[GitProject]] = []

    async def start(self):
        self._projects = []
        logger.info("start parse projects")
        await self.git_api.create_session()
        await self._get_projects()
        await self._add_blops()
        await self._add_raws()
        await self.git_api.close_session()
        self.projects = self._projects
        logger.info("finish parse projects")

    async def _get_projects(self):
        projects = []
        has_more = True
        end_cursor = ""
        loop_count = 0
        while has_more:
            result = await self.git_api.async_post(q.get_projects_query(end_cursor))
            if not result:
                logger.error(f"some error")
                return
            projects.extend([GitProject(**p) for p in result["projects"]["nodes"]])
            has_more = result["projects"]["pageInfo"]["hasNextPage"]
            end_cursor = result["projects"]["pageInfo"]["endCursor"]
            loop_count += 1
        self._projects = projects
        logger.info(f"start projecst loop count: {loop_count}")

    async def _get_incomplited_project(self, project: GitProject):
        while project.has_more:
            result = await self.git_api.async_post(
                q.get_incomplited_project_query(project.path, project.end_cursor)
            )
            if not result:
                logger.error(f"some error")
                return
            try:
                blobs = result["project"]["repository"]["tree"]["blobs"]["nodes"]
            except:
                blobs = []
            project.blobs.extend([GitBlob(**p) for p in blobs])
            project.has_more = result["project"]["repository"]["tree"]["blobs"][
                "pageInfo"
            ]["hasNextPage"]
            project.end_cursor = result["project"]["repository"]["tree"]["blobs"][
                "pageInfo"
            ]["endCursor"]

    async def _add_blops(self):
        a_tasks = [
            self._get_incomplited_project(p) for p in self._projects if p.has_more
        ]
        logger.info(f"count incomplited projects: {len(a_tasks)}")
        await asyncio.gather(*a_tasks)

    async def _add_one_raw(self, project: GitProject, query: str):
        result = await self.git_api.async_post(query)
        if not result:
            logger.error(f"some error")
            return
        try:
            blobs_results = result["project"]["repository"]["blobs"]["nodes"]
        except:
            blobs_results = []
        for b_res in blobs_results:
            blob = [b for b in project.blobs if b.path == b_res["path"]][0]
            blob.raw = b_res["rawBlob"]
            blob.raw_path = b_res["rawPath"].replace("/raw/", "/blob/")

    async def _add_raws(self):
        a_tasks = []
        for project in self._projects:
            parts_blobs = [
                project.blobs[x : x + 20] for x in range(0, len(project.blobs), 20)
            ]
            for part in parts_blobs:
                blobs = (
                    '"'
                    + '",\n"'.join(
                        [
                            blob.path
                            for blob in part
                            if self._check_extensions(blob.path)
                        ]
                    )
                    + '"'
                )
                if blobs == '""':
                    continue
                a_tasks.append(
                    self._add_one_raw(
                        project=project,
                        query=q.get_project_blobs_query(project.path, blobs),
                    )
                )
        logger.info(f"count a_tasks for blobs: {len(a_tasks)}")
        await asyncio.gather(*a_tasks)
        
    @staticmethod
    def _check_extensions(file_name: str):
        return file_name.split(".")[-1] in settings.extensions

    def saerch_by_projects(self, target_string):
        results = []
        for project in self.projects:
            for blob in project.blobs:
                if not blob.raw:
                    continue
                for num_string, string in enumerate(blob.raw.split("\n"), start=1):
                    if target_string in string:
                        results.append(
                            f"{settings.git_url}/{blob.raw_path}#L{num_string}"
                        )
        for res in results:
            print(res)


git_parser = GitParser()


if __name__ == "__main__":
    gp = GitParser()
    asyncio.run(gp.start())
    while True:
        s = input("write string:\n")
        gp.saerch_by_projects(s)
