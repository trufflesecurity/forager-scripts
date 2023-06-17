# Forager scripts
This tool is complementary to https://forager.trufflesecurity.com

It show's an example of monitoring employee commits. It is not intended for production use.

## how to run
Clone the repo:
`git clone https://github.com/trufflesecurity/forager-scripts`

Fill out config.json in your current working directory
```
{
    "organizations": ["uber", "lyft"],
    "api_key": "<yourGitHubAPIKeyHere>"
}
```
Run the script:
`docker run -v ${PWD}/db:/app/db -v ${PWD}/config.json:/app/config.json --rm -it forager`

## Disclaimer
This is an example script, not meant to be maintained long term, please only use for inspiration, don't operationalize without modifying
