# KMS Slack Interface

to do:
- write this readme

`docker build -t kms-slack .` then `docker run -p 4000:80 kms-slack`

`docker logs -f kms-slack` to see output while container is running


## Deployment
`docker buildx build -t kms-slack-client --platform linux/amd64 .`

`docker tag kms-slack-client gcr.io/knowledge-management-333914/kms-slack`

`docker push gcr.io/knowledge-management-333914/kms-slack`