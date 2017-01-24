from gittle import *

repo_url = "http://10.100.13.22:8080/tfs/CloudCollection/IaasPlatform/_git/test"
repo_path = '/root/git/test'

repo = Gittle(repo_path, origin_uri=repo_url)
repo.auth(username="wangfangjie", password="pdmi1234")
#auth_info = GittleAuth(username="wangfangjie", password="pdmi1234")
#repo = Gittle.clone(repo_url, repo_path, auth=auth_info)
print repo.branches
print repo.modified_files
repo.push()


