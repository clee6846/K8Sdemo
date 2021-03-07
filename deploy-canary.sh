#!/bin/bash
Deploymentfile0=my-image-canary-v-1-0-deployment.yaml
Servicefile0=my-image-canary-v-1-0-svc.yaml
Deploymentfile1=my-image-canary-v-1-1-deployment.yaml
Servicefile1=my-image-canary-v-1-0-svc.yaml
kubectl create -f ./${Deploymentfile0} --record
sleep 10
#kubectl get deployment
echo "kubectl get deployment"
kubectl get deployment
echo
echo "kubectl get pods"
kubectl get pods
echo "kubectl describe deployment my-image-canary-v-1-0"
kubectl describe deployment my-image-canary-v-1-0
echo
echo "kubectl create -f ./my-image-service.yaml"
kubectl create -f ./${Servicefile0}
sleep 10
echo "kubectl get svc"
kubectl get svc
echo
echo "The below is external name"
kubectl get svc|grep my-image-canary|awk '{print $4}'
#
kubectl create -f ./${Deploymentfile1} --record
sleep 10
#kubectl get deployment
echo "kubectl get deployment"
kubectl get deployment
echo
echo "kubectl get pods"
kubectl get pods
echo "kubectl describe deployment my-image-canary-v-1-1"
kubectl describe deployment my-image-canary-v-1-1


