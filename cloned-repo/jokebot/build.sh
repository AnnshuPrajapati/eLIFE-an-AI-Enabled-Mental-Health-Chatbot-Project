#!/bin/sh
VERS=1.1.1
REGISTRY=ghcr.io/rgstephens
#REGISTRY=stephens
IMAGE=jokebot
#K8S_DEPLOYMENT=bandonbrawl
#K8S_NAMESPACE=gstephens

echo Building ${REGISTRY}/${IMAGE}:${VERS}
if [ -z "$CR_PAT" ]; then
  echo "must set CR_PAT"
  exit 1
fi
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
time docker buildx build --platform linux/amd64 --output=type=registry --tag ${REGISTRY}/${IMAGE}:${VERS} --tag ${REGISTRY}/${IMAGE}:latest .
#time docker buildx build --platform linux/amd64,linux/arm64 --output=type=registry --tag ${REGISTRY}/${IMAGE}:${VERS} --tag ${REGISTRY}/${IMAGE}:latest .
docker push ${REGISTRY}/${IMAGE} --all-tags
#kubectl config use-context default
#kubectl rollout restart deploy ${K8S_DEPLOYMENT} -n ${K8S_NAMESPACE}
docker pull ${REGISTRY}/${IMAGE}:${VERS}
