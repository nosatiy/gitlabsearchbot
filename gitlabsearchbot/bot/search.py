from collections import defaultdict

from aiogram import types
from gitlab.parser import git_parser
from settings import settings


async def search(target_text: str, ignore_registry: bool = False) -> str:
    results = defaultdict(list)

    for project in git_parser.projects:
        for blob in project.blobs:
            if not blob.raw:
                continue
            for num_string, string in enumerate(blob.raw.split("\n"), start=1):
                if target_text in string or (
                    ignore_registry and target_text.lower() in string.lower()
                    ):
                    results[(project.path, project.project_id)].append(
                        f"{settings.git_url}/{blob.raw_path}#L{num_string}"
                    )

    if not results:
        return 'Ничего не нашел :('

    results = dict(sorted(results.items(), key=lambda x: len(x[1]), reverse=True))

    result_string = ""
    count_res = 0
    for project, matched_stings in results.items():
        if count_res > 20:
            break
        result_string += f"{project[0]}\nCовпадений в проектк: {len(matched_stings)}\n"
        if len(matched_stings) < 10:
            result_string += "\n".join(matched_stings)
        else:
            result_string += f"{settings.git_url}/search?search={target_text}&project_id={project[1]}&search_code=true&repository_ref=master"
        result_string += "\n\n"
        count_res += 1

    return result_string
