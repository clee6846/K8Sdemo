#!/bin/bash
#Install InfluxDB
echo "Installing InfluxDB"
echo
https://dl.influxdata.com/influxdb/releases/influxdb2-2.0.4-amd64.deb
sudo dpkg -i influxdb2-2.0.4-amd64.deb
echo
#For redHat & CentOS
#https://dl.influxdata.com/influxdb/releases/influxdb2-2.0.4.x86_64.rpm
#sudo yum localinstall influxdb2-2.0.4.x86_64.rpm
#Install Telegraf
echo "Installing telegraf"
echo
wget https://dl.influxdata.com/telegraf/releases/telegraf_1.17.3-1_amd64.deb
sudo dpkg -i telegraf_1.17.3-1_amd64.deb
echo
#For redhat & CentOS
#wget https://dl.influxdata.com/telegraf/releases/telegraf-1.17.3-1.x86_64.rpm
#sudo yum localinstall telegraf-1.17.3-1.x86_64.rpm
#Install Helm
echo "Installing helm"
echo 
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
sudo apt-get install apt-transport-https --yes
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
echo 
sudo apt-get update
sudo apt-get install helm
#
#Add Helm repositories
#Adding Helm Chat Repository
helm repo add stable https://charts.helm.sh/stable
#list the charts you can install
echo "list the charts you can install"
helm search repo stable
#Creating Monitor Namespace
echo "Creating Monitor Namespace"
echo 
kubectl create namespace prometheus

#Installation Of Prometheus Operator
echo "Installation Of Prometheus Operator by using helm"
echo 
# Make sure we get the latest list of charts
helm search repo stable
helm install prometheus stable/prometheus-operator --namespace prometheus
kubectl get pods -n prometheus
nohup kubectl port-forward -n prometheus prometheus-prometheus-prometheus-oper-prometheus-0 0.0.0.0 9090 &
#
echo "you can access Grafana dashboard at http://44.237.190.202:3000"
echo 
nohup kubectl port-forward -n prometheus prometheus-grafana-d6545c767-884vq --address 0.0.0.0 3000 & 
echo "You will get the Grafana dashboard username and password from getting a secret from prometheus-grafana."
echo 
kubectl get secret --namespace prometheus prometheus-grafana -o yaml

echo "For getting username"
echo "openssl base64 -d  YWRtaW4= admin"
echo "For getting password"
echo "openssl base64 -d cHJvbS1vcGVyYXRvcg==   prom-operator"
echo "you can access Grafana dashboard at http://44.237.190.202:3000"
