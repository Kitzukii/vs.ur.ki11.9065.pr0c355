import requests, os, venv

class GitRepo:
    def __init__(self,user,repo,branch):
        self.__repo_base_url__:str = f"https://raw.githubusercontent.com/{user}/{repo}"
        self.branch = branch

    def getFile(self,path:str) -> str:
        r = requests.get(f"{self.__repo_base_url__}/refs/heads/{self.branch}/{path}")
        return r.text

    def getJsonFile(self,path:str) -> str:
        import json
        r = requests.get(f"{self.__repo_base_url__}/refs/heads/{self.branch}/{path}")
        return json.loads(r.text)

repo = GitRepo("Kitzukii","vs.ur.ki11.9065.pr0c355","main")
meta = repo.getJsonFile("fs.json")

filePrefix = meta.get("prefix","mods")
filesToGet = meta.get("files",[])
if not ( filePrefix[-1] == "/" ):
    filePrefix = f"{filePrefix}/"

for file in filesToGet:
    f = open(file,"w")
    f.write(repo.getFile(filePrefix+file))
    f.close()
    print(f"Downloaded file: {file}")