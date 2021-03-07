#!/bin/bash
#This script delete EKS cluster1
eksctl delete cluster cluster1
echo "deleting, please wait"
echo "You may run kubectl get nodes"
