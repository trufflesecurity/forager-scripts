# Forager scripts
This tool is complementary to https://forager.trufflesecurity.com

It show's an example of monitoring employee commits. It is not intended for production use.

## how to run
docker run -v ${PWD}/db:/app/db -v ${PWD}/config.json:/app/config.json --rm -it forager

