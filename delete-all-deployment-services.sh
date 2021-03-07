#!/bin/bash
kubectl get deployment >temp
awk '(NR>1)' temp|kubectl delete deployment `awk '{print $1}'`

kubectl get service >temp
awk '(NR>1)' temp|kubectl delete service `awk '{print $1}'`

