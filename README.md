# Model Inference and Monitoring
Entirely motivated by the paper [Underspecification Presents Challenges for Credibility in
Modern Machine Learning](https://arxiv.org/pdf/2011.03395.pdf) and bringing these concerns closer to production, the curiousity here is to explore some of the existing tooling to monitor models in production to detect and log:
- concept drift
- stress test and other evalution
- fairness and bias
- out of distribution Detection, concept drift detection using [Alibi](https://github.com/SeldonIO/alibi) or [AIF360](https://github.com/Trusted-AI/AIF360#supported-bias-mitigation-algorithms)
- Logging with KNative, Istio, Prometheus and Grafana

In order to get more familiar with [KFServing](https://github.com/kubeflow/kfserving), we will attempt to perform this monitoring, logging and evaluation with this tooling.

## Project Structure
For now, we have a simple codebase to support model development and deployment to KFServing. First goals:
- choose a model that is susceptible to underspecification
- propose method to alleviate bias and underspecification
- Use KFServing to serve model and 'pretend' this is production
- Eventually log metrics for production grade monitoring

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
