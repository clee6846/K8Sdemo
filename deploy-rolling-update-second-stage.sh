#!/bin/bash
#
Deploymentfile=my-image-rolling-update-deployment.yaml
DOCKER_HUB_USERNAME=chauwei150

kubectl set image deploy/my-image-rolling-update my-image=${DOCKER_HUB_USERNAME}/my-image:1.1; \
kubectl rollout restart deployment my-image-rolling-update
echo "show deployments"
kubectl get deployments
echo
echo "show pods"
kubectl get pods
echo
echo
echo "show services"
kubectl get svc
sleep 20
echo "kubectl describe deployment my-image-rolling-update"
kubectl describe deployment my-image-rolling-update
#
echo "Below is external name"
kubectl get svc|grep rolling|awk '{print $4}'
