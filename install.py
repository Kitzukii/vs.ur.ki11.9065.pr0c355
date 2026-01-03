import requests,json,os

class GitRepo:
    """
    provider is a str like this:<br>
    raw.githubusercontent.com

    repo is a str like this:<br>
    Username/Repository

    (both "get"s default to https and branch "main")
    """
    def __init__(self,repo:str,provider:str="raw.githubusercontent.com"):
        self.provider=provider
        self.repo=repo
    
    def __fmt_lnk(self,p:str,r:str,f:str):
        return "https://"+p+"/"+r+"/refs/heads/main/"+f

    def __fmt_lnk_wTkn(self,p:str,r:str,f:str,t:str):
        return ("https://"+p+"/"+r+"/refs/heads/main/"+f+
            "?token="+t)
    
    def get(self,path):
        return requests.get(
            self.__fmt_lnk(
                self.provider,
                self.repo,
                path
            )
        ).content
    
    def getWithtoken(self,path,token):
        return requests.get(
            self.__fmt_lnk_wTkn(
                self.provider,
                self.repo,
                path,
                token
            )
        ).content

cwd = os.getcwd()
mdrp = GitRepo(
    provider="raw.githubusercontent.com",
    repo="Kitzukii/vs.ur.ki11.9065.pr0c355"
)
with open("private.token","r") as f:
    tk = f.read().strip()

print(mdrp.getWithtoken("md/fs.json",tk))
# metadata:dict = json.loads(mdrp.getWithtoken("md/fs.json",tk))
# print(metadata)
# filePrefixes:str = metadata.get("prefix")
# filesToGet:list = metadata.get("files")

# for file in filesToGet:
#     p=os.path.join(cwd,file)
#     c=mdrp.getWithtoken
#     f=open(p,"w")
#     f.write()