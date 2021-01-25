# Install KFServing in 5 Minutes (On your local machine)

Make sure you have
[kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl-on-linux) installed.

1) If you do not have an existing kubernetes cluster,
you can create a quick kubernetes local cluster with [kind](https://github.com/kubernetes-sigs/kind#installation-and-usage).

Note that the minimal requirement for running KFServing is 4 cpus and 8Gi memory,
so you need to change the [docker resource setting](https://docs.docker.com/docker-for-mac/#advanced) to use 4 cpus and 8Gi memory.
```bash
kind create cluster
```
alternatively you can use [Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube)
```bash
minikube start --cpus 4 --memory 8192 --kubernetes-version=v1.17.11
```

2) Install Istio lean version, Knative Serving, KFServing all in one.(this takes 30s)
```bash
./hack/quick_install.sh
```

### Test KFServing Installation

#### Check KFServing controller installation
```shell
kubectl get po -n kfserving-system
NAME                             READY   STATUS    RESTARTS   AGE
kfserving-controller-manager-0   2/2     Running   2          13m
```

Please refer to our [troubleshooting section](docs/DEVELOPER_GUIDE.md#troubleshooting) for recommendations and tips for issues with installation.

#### Create KFServing test inference service
```bash
API_VERSION=v1alpha2
kubectl create namespace kfserving-test
kubectl apply -f docs/samples/${API_VERSION}/sklearn/sklearn.yaml -n kfserving-test
```
#### Check KFServing `InferenceService` status.
```bash
kubectl get inferenceservices sklearn-iris -n kfserving-test
NAME           URL                                                              READY   DEFAULT TRAFFIC   CANARY TRAFFIC   AGE
sklearn-iris   http://sklearn-iris.kfserving-test.example.com/v1/models/sklearn-iris   True    100                                109s
```

#### Determine the ingress IP and ports
Execute the following command to determine if your kubernetes cluster is running in an environment that supports external load balancers
```bash
$ kubectl get svc istio-ingressgateway -n istio-system
NAME                   TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)   AGE
istio-ingressgateway   LoadBalancer   172.21.109.129   130.211.10.121   ...       17h
```
If the EXTERNAL-IP value is set, your environment has an external load balancer that you can use for the ingress gateway.

```bash
export INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].port}')
```

If the EXTERNAL-IP value is none (or perpetually pending), your environment does not provide an external load balancer for the ingress gateway. In this case, you can access the gateway using the service’s node port.
```bash
# GKE
export INGRESS_HOST=worker-node-address
# Minikube
export INGRESS_HOST=$(minikube ip)
# Other environment(On Prem)
export INGRESS_HOST=$(kubectl get po -l istio=ingressgateway -n istio-system -o jsonpath='{.items[0].status.hostIP}')

export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
```

Alternatively you can do `Port Forward` for testing purpose
```bash
INGRESS_GATEWAY_SERVICE=$(kubectl get svc --namespace istio-system --selector="app=istio-ingressgateway" --output jsonpath='{.items[0].metadata.name}')
kubectl port-forward --namespace istio-system svc/${INGRESS_GATEWAY_SERVICE} 8080:80
# start another terminal
export INGRESS_HOST=localhost
export INGRESS_PORT=8080
```

#### Curl the `InferenceService`
Curl from ingress gateway
```bash
SERVICE_HOSTNAME=$(kubectl get inferenceservice sklearn-iris -n kfserving-test -o jsonpath='{.status.url}' | cut -d "/" -f 3)
curl -v -H "Host: ${SERVICE_HOSTNAME}" http://${INGRESS_HOST}:${INGRESS_PORT}/v1/models/sklearn-iris:predict -d @./docs/samples/${API_VERSION}/sklearn/iris-input.json
```
Curl from local cluster gateway
```bash
curl -v http://sklearn-iris.kfserving-test/v1/models/sklearn-iris:predict -d @./docs/samples/${API_VERSION}/sklearn/iris-input.json
```

#### Run Performance Test
```bash
# use kubectl create instead of apply because the job template is using generateName which doesn't work with kubectl apply
kubectl create -f docs/samples/${API_VERSION}/sklearn/perf.yaml -n kfserving-test
# wait the job to be done and check the log
kubectl logs load-test8b58n-rgfxr -n kfserving-test
Requests      [total, rate, throughput]         30000, 500.02, 499.99
Duration      [total, attack, wait]             1m0s, 59.998s, 3.336ms
Latencies     [min, mean, 50, 90, 95, 99, max]  1.743ms, 2.748ms, 2.494ms, 3.363ms, 4.091ms, 7.749ms, 46.354ms
Bytes In      [total, mean]                     690000, 23.00
Bytes Out     [total, mean]                     2460000, 82.00
Success       [ratio]                           100.00%
Status Codes  [code:count]                      200:30000
Error Set:
```

### Setup Ingress Gateway
If the default ingress gateway setup does not fit your need, you can choose to setup a custom ingress gateway
- [Configure Custom Ingress Gateway](https://knative.dev/docs/serving/setting-up-custom-ingress-gateway/)
  -  In addition you need to update [KFServing configmap](config/default/configmap/inferenceservice.yaml) to use the custom ingress gateway.
- [Configure Custom Domain](https://knative.dev/docs/serving/using-a-custom-domain/)
- [Configure HTTPS Connection](https://knative.dev/docs/serving/using-a-tls-cert/)

### Setup Monitoring
- [Metrics](https://knative.dev/docs/serving/accessing-metrics/)
- [Tracing](https://knative.dev/docs/serving/accessing-traces/)
- [Logging](https://knative.dev/docs/serving/accessing-logs/)
- [Dashboard for ServiceMesh](https://istio.io/latest/docs/tasks/observability/kiali/)

### Use KFServing SDK
* Install the SDK
  ```
  pip install kfserving
  ```
* Check the KFServing SDK documents from [here](python/kfserving/README.md).

* Follow the [example(s) here](docs/samples/client) to use the KFServing SDK to create, rollout, promote, and delete an InferenceService instance.

### KFServing Features and Examples
[KFServing Features and Examples](./docs/samples/README.md)

### KFServing Presentations and Demoes
[KFServing Presentations and Demoes](./docs/PRESENTATIONS.md)

### KFServing Roadmap
[KFServing Roadmap](./ROADMAP.md)

### KFServing Concepts and Data Plane
[KFServing Concepts and Data Plane](./docs/README.md)

### KFServing API Reference
[KFServing v1alpha2 API Docs](./docs/apis/v1alpha2/README.md)

[KFServing v1beta1 API Docs](./docs/apis/v1beta1/README.md)

### KFServing Debugging Guide :star:
[Debug KFServing InferenceService](./docs/KFSERVING_DEBUG_GUIDE.md)

### Developer Guide
[Developer Guide](/docs/DEVELOPER_GUIDE.md).

### Performance Tests
[KFServing benchmark test comparing Knative and Kubernetes Deployment with HPA](test/benchmark/README.md)

### Contributor Guide
[Contributor Guide](./CONTRIBUTING.md)

### KFServing Adopters
[KFServing Adopters](./ADOPTERS.md)
