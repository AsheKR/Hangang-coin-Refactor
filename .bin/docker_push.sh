#! /bin/bash
# GitHub에서 발생한 WebHook이 PUSH일 경우만 실행하도록한다.
if [ -z "$TRAVIS_PULL_REQUEST" ] || [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
# master 브랜치일경우만 push가 실행되도록한다.
if [ "$TRAVIS_BRANCH" == "master" ]; then

docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD

# Build and push
docker build -t $IMAGE_NAME:base -f Dockerfile.base .
docker push "$IMAGE_NAME:base"
docker build -t $IMAGE_NAME .
docker push "$IMAGE_NAME:latest"

else
echo "Skipping deploy because branch is not 'master'"
fi
else
echo "Skipping deploy because it's a pull request"
fi