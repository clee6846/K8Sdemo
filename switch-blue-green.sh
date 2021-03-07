#!/bin/bash

echo "To have all requests immediately rerouted to the green Deployment, we will change the selector" 
echo "the LoadBalancer Service is using for color from blue to green:"

kubectl set selector svc/my-image-blue-green color=green

