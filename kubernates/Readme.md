TO Deploy On the minikube

kubectl apply -f ras_deployment.yaml
kubectl apply -f ras_services.yaml
kubectl get pod,svc