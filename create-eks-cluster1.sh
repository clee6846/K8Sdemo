#!/bin/bash
#This script will create EKS cluster cluter1
eksctl create cluster -f createEKScluster.yaml
echo "creating please wait"
echo "When it's done, just run kubectl get nodes"
