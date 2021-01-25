# Model Inference and Monitoring
A codebase to support model deployment to KFServing or any application that supports HTTPS or gRPC API requests. The goal is to be able to:
- Model Serving
- Model Monitoring.
- Out of distribution Detection, concept drift detection using [Alibi](https://github.com/SeldonIO/alibi) or [AIF360](https://github.com/Trusted-AI/AIF360#supported-bias-mitigation-algorithms)
- Logging with KNative, Istio, Prometheus and Grafana

## Getting Started

First, create a `virtualenv`:
```
virtualenv -p python3 .mapi
```
activate with
```
source .mapi/bin/activate
```
install the package in editable mode:
```
pip install -e .
```
and build a ipython kernel if you want to use jupyter notebook:
```
ipython kernel install --name "mapi" --user
```

## Docker
Feel free to build a Dockerfile to suppor this project. Keep [these](https://www.docker.com/blog/containerized-python-development-part-1/) things in mind.
