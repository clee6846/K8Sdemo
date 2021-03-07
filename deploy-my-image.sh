#!/bin/bash
Deploymentfile=my-image-deployment.yaml
Servicefile=my-image-service.yaml
kubectl create -f ./${Deploymentfile} --record
sleep 10
#kubectl get deployment
echo "kubectl get deployment"
kubectl get deployment
echo
echo "kubectl get pods"
kubectl get pods
echo "kubectl describe deployment my-image"
kubectl describe deployment my-image
echo
echo "kubectl create -f ./my-image-service.yaml"
kubectl create -f ./${Servicefile}
sleep 10
echo "kubectl get svc"
kubectl get svc
echo
echo "The below is external name"
kubectl get svc|grep my-image-svc|awk '{print $4}'

