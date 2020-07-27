# Git Raider

Searches for secrets in provided git repos. Built on top of https://github.com/nielsing/yar/

## How to use
1. Create and activate python3.8 virtual environment
2. Update raider.yaml with your organizations / members / repos. Note that it searches all member's in an organizations repos as well, so no need to list members in the members section
3. Add util/yarconfig.json. An example can be found at https://github.com/nielsing/yar/blob/master/config/yarconfig.json
4. (Recommended) Create a github personal access token at https://github.com/settings/tokens and `export YAR_GITHUB_TOKEN=$yourtoken`
5. `python3.8 main.py` which will output all currently found secrets. All following runs will only show new secrets