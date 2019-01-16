#! /bin/bash
# GitHub에서 발생한 WebHook이 PUSH일 경우만 실행하도록한다.
if [ -z "$TRAVIS_PULL_REQUEST" ] || [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
# master 브랜치일경우만 push가 실행되도록한다.
if [ "$TRAVIS_BRANCH" == "master" ]; then

eval $(aws ecr get-login --no-include-email --region ap-northeast-2)

# Build and push
docker build -t $IMAGE_NAME:base -f Dockerfile.base .
docker build -t $IMAGE_NAME .
echo "Pushing $IMAGE_NAME"
docker tag $IMAGE_NAME:latest "$REMOTE_IMAGE_URL:latest"
docker tag $IMAGE_NAME:base "$REMOTE_IMAGE_URL:base"
docker push "$REMOTE_IMAGE_URL:base"
docker push "$REMOTE_IMAGE_URL:latest"
echo "Pushed $IMAGE_NAME:latest"

else
echo "Skipping deploy because branch is not 'master'"
fi
else
echo "Skipping deploy because it's a pull request"
fi