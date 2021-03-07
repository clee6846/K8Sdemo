#!/bin/bash
Deploymentfile0=my-image-blue-deployment.yaml
Servicefile0=my-image-blue-green-svc.yaml
Deploymentfile1=my-image-green-deployment.yaml
kubectl create -f ./${Deploymentfile0} --record
sleep 10
#kubectl get deployment
echo "kubectl get deployment"
kubectl get deployment
echo
echo "kubectl get pods"
kubectl get pods
echo "kubectl create -f ./my-image-blue-green-svc.yaml"
kubectl create -f ./${Servicefile0}
sleep 10
echo "kubectl get svc"
kubectl get svc
echo
echo "The below is external name"
kubectl get svc|grep my-image-blue-green|awk '{print $4}'
#
kubectl create -f ./${Deploymentfile1} --record
sleep 10
#kubectl get deployment
echo "kubectl get deployment"
kubectl get deployment
echo
echo "kubectl get pods"
kubectl get pods
echo "kubectl describe deployment my-image-blue"
kubectl describe deployment my-image-blue
echo
echo "kubectl describe deployment my-image-green"
kubectl describe deployment my-image-green
echo "kubectl describe svc my-image-blue-green"
kubectl describe service my-image-blue-green


