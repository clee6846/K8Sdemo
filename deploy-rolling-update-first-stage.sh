#!/bin/bash
#
Deploymentfile=my-image-rolling-update-deployment.yaml
DOCKER_HUB_USERNAME=chauwei150

#Create a new rolling update deployment
echo "kubectl create -f ${Deploymentfile}"
kubectl create -f ${Deploymentfile}
#
# show deployment
kubectl get deployments
sleep 5
#scale up the Deployment to increase the amount of Pods to 6
echo "scale up the Deployment to increase the amount of Pods to 6"
echo "kubectl scale deployment hugo-app-rolling-update --replicas 6"
kubectl scale deployment my-image-rolling-update --replicas 6
#
#
# show deployemnts
kubectl get deployments
echo "kubectl describe deployment my-image-rolling-update"
kubectl describe deployment my-image-rolling-update
# Create my-image-service
echo "Create my-image-rolling-update-svc"
echo  "kubectl expose deployment my-image-rolling-update --name=my-image-rolling-update-svc "
echo "--type=LoadBalancer --port=80 --target-port=80"
kubectl expose deployment my-image-rolling-update --name=my-image-rolling-update-svc \
 --type=LoadBalancer --port=80 --target-port=80
echo "show services"
kubectl get svc
sleep 20
echo "kubectl describe deployment my-image-rolling-update"
kubectl describe deployment my-image-rolling-update
#
echo "Below is external name"
kubectl get svc|grep rolling|awk '{print $4}'

