# From Charles Lee, 

1. The repo has two prts the first is the Python codes

a. deploymentautomations.py
b. rdsutilities.py
c. ta.py
d. terraform.py
e. aws utilities

2. The demo of K8S three kind of deployments




I have two containers which has the test webpage in my own Docker hub
the userid is chauwei150
password is clee6846@yahoo.com
within the IP, you don't have to set up the secret in Kubenetes


You can first login the EC2 instance I created in US-west-2 :  ssh -i "tester2.pem" ubuntu@IP
After login 

cd /home/ubuntu/

In this take homw test, I use Ubuntu as my Kubernete master none ans Amazon Linux as worker nodes. I just want to show you I familiar to this two Linux OS.
I use EKSCTL with the ymal file. I chose eksctl is because in the background which use Cloudformation while I have certain knowledge in Cloudformation. AS we use terraform to crate VPC, subnet,network, security group.
In Kubernete, I have install helm as package management system, Prometheus as alert system, as moniting engine for minitoring services, conatiners, apis etc within Kubernete. And Grafana can display Prometheus's metrics in illustrational dashborads

I created three kinds of Kubernete deployment
1. rolling-update
2. canary
3. blue and green

Please play around the following scripts, Thanks

create-eks-cluster1.sh : To create EKS managed cluster "cluster1"
createEKScluster.yaml : eksctl will create 4 nodes, each in the us-west-2a, us-west-2b, us-west-2c, us-west-2d
delele-eks-cluster1.sh : To delete EKS cluster "cluser1"
delete-all-deployment-services.sh : delete two K8S deployments and two services

* deploy-my-image.sh : To deploy a simple k8S cluster "my-image" will display the Hello World web application, you can find elb dns name at the end of script.

* deploy-rolling-update-first-stage.sh : To deploy a simple K8S cluster "my-image-rolling-update", first will deploy a one pod, 
                                       next step will update to 6 pods, each pod will display the Hello World appliaction in the browser. 
                                       you can find elb dns name at the end of script.
* deploy-rolling-update-second-stage.sh: To rolling update the Hello World applaiction, will display one more line in each 6 pods.

* deploy-canary.sh: To create two deployments. One is stable, the other is canary
* switch-canary.sh: To switch stable to canary and canary to stable. The webpage will be changed from v1.0 to v1.1.
 
* deploy-blue-green.sh: To create two deployments, One is color=blue, the othe color=green
* switch-blue-gree.sh: To switch the selector the LoadBalancer Service is using for color from blue to green. The webpage will be chnaged from v1.0 to v1.1

* setupInfluxTeleHelmfPromGraf.sh : This script will setup helm, add helm char repos, prometheus, prometheus-grafana. You can view Grafana at
                                   http://44.237.190.202:3000/  userid is admin the password is prom-operator. Prometheus provide many metrics to help
                                  system admin to get close look when monitor Kubernetes. Grafana provides the dashboard to display prometheus metrics, also we can 
                                  customerize many different dashboards from InfluxDB, Loki, Graphit etc. I installed Telegraf and InfluxDB but I didn't setup them.
                                  In my company, we use Telegraf to collect the EC2 instances monitor metrics and customerized script to collect server events to 
                                  InfludDB and view them in the Grafana.
"you can access Prometheus  dashboard at http://44.237.190.202:9090"
nohup kubectl port-forward -n prometheus prometheus-prometheus-prometheus-oper-prometheus-0 --address 0.0.0.0 9090 &
#
"you can access Grafana dashboard at http://44.237.190.202:3000"
echo 
nohup kubectl port-forward -n prometheus prometheus-grafana-d6545c767-884vq --address 0.0.0.0 3000 & 
echo "You will get the Grafana dashboard username and password from getting a secret from prometheus-grafana."
echo 
kubectl get secret --namespace prometheus prometheus-grafana -o yaml

echo "For getting username"
echo "openssl base64 -d  YWRtaW4= admin"
echo "For getting password"
echo "openssl base64 -d cHJvbS1vcGVyYXRvcg==   prom-operator"

Below are support files

tester2.pem
README.md
index.html
my-image-blue-deployment.yaml
my-image-blue-green-svc.yaml
my-image-blue-green.yaml
my-image-canary-v-1-0-deployment.yaml
my-image-canary-v-1-0-svc.yaml
my-image-canary-v-1-1-deployment.yaml
my-image-deployment.yaml
my-image-green-deployment.yaml
my-image-rolling-update-deployment.yaml
my-image-service.yaml
nohup.out

I first created terraform in the other VPC and peering with the default VPC, but I'm going to use eksctl which acrually is Cloudformation. 
So I decided not to use Terraform. 

