from gitlab.parser import git_parser
import asyncio

if __name__ == '__main__':
    asyncio.run(git_parser.start())
    while True:
        s = input("write string:\n")
        git_parser.saerch_by_projects(s)