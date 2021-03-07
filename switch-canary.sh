#!/bin/bash
#You can simulate this by forcing a page reload in your browser multiple times until you see 
#the one more 'hello world'  change from v.1.0 to v.1.1.
kubectl get pods --label-columns=track
sleep 5
echo "To increase the percentage of requests that go to the canary Deployment" 
echo "will scale up the v.1.1  Deployment to three Pods and then scale down the v.1.0 to one Pod:"

kubectl scale deployment my-image-canary-v-1-1  --replicas=3
kubectl scale deployment my-image-canary-v-1-0  --replicas=0

kubectl get pods --label-columns=track


