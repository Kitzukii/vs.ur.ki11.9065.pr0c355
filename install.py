import requests
import os
import json

class GitRepo:
    def __init__(self, repo: str, branch: str = "main"):
        self.repo = repo
        self.branch = branch
        self.base = f"https://raw.githubusercontent.com/{repo}/{branch}"

    def _headers(self, token: str | None):
        if token is None:
            return {}
        return {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.raw"
        }

    def get(self, path: str, token: str | None = None) -> bytes:
        url = f"{self.base}/{path}"
        r = requests.get(url, headers=self._headers(token))
        r.raise_for_status()
        return r.content


cwd = os.getcwd()

repo = GitRepo("Kitzukii/vs.ur.ki11.9065.pr0c355")

with open("private.token", "r") as f:
    token = f.read().strip()

data = repo.get("fs.json", token)
print(data)

# metadata:dict = json.loads(mdrp.getWithtoken("md/fs.json",tk))
# print(metadata)
# filePrefixes:str = metadata.get("prefix")
# filesToGet:list = metadata.get("files")

# for file in filesToGet:
#     p=os.path.join(cwd,file)
#     c=mdrp.getWithtoken
#     f=open(p,"w")
#     f.write()