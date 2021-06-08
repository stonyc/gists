This document details how to install GitLab as a service in a Kubernetes cluster.

---
# **1. Install Helm and Tiller**

The easiest method to install `helm` for Ubuntu-server is:

```bash
sudo snap install helm --classic
```

**NOTE**: On a single node cluster, the following command must be run to enable deployment of Tiller:

```bash
kubectl taint nodes --all node-role.kubernetes.io/master- 
```

**NOTE**: In some clusters, Tiller must be granted permissions in order to be deployed and update packages:

```bash
# kubernetes-tiller-deply.yml
apiVersion: v1
kind: Service
metadata:
  name: tiller-deploy
  namespace: kube-system
  labels:
    app: helm
    name: tiller
spec:
  ports:
  - name: tiller
    port: 44134
    protocol: TCP
    targetPort: tiller
  selector:
    app: helm
    name: tiller
  type: ClusterIP
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: tiller-deploy
  namespace: kube-system
  labels:
    app: helm
    name: tiller
  annotations:
    deployment.kubernetes.io/revision: "5"
spec:
  replicas: 1
  selector:
    matchLabels:
      app: helm
      name: tiller
  template:
    metadata:
      labels:
        app: helm
        name: tiller
    spec:
      containers:
      - env:
        - name: TILLER_NAMESPACE
          value: kube-system
        - name: TILLER_HISTORY_MAX
          value: "0"
        name: tiller
        image: gcr.io/kubernetes-helm/tiller:v2.8.2
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 44134
          name: tiller
          protocol: TCP
        - containerPort: 44135
          name: http
          protocol: TCP
        livenessProbe:
          failureThreshold: 3
          httpGet:
            path: /liveness
            port: 44135
            scheme: HTTP
          initialDelaySeconds: 1
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        readinessProbe:
          failureThreshold: 3
          httpGet:
            path: /readiness
            port: 44135
            scheme: HTTP
          initialDelaySeconds: 1
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      serviceAccount: tiller
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tiller
  namespace: kube-system
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: tiller-cluster-rule
subjects:
- kind: ServiceAccount
  name: tiller
  namespace: kube-system
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: ""
```

Save the file `kubernetes-tiller-deploy.yml` then run the command `kubectl apply -f kubernetes-tiller-deploy.yml` to grant permissions to Tiller.

Upgrade Helm and Tiller to the latest versions, then deploy to the cluster:

```bash
helm init --upgrade
```

Check the status of the Tiller service:

```bash
kubectl get pods --namespace kube-system
```

---
# **2. Deploy GitLab Enterprise Edition using Helm**

```bash
helm repo add gitlab https://charts.gitlab.io/
helm repo update
# Dry run of the GitLab deployment:
helm upgrade \
--install gitlab gitlab/gitlab \
    --timeout 600 \
    --set global.edition=ee \
    --set global.hosts.https=true \
    --set global.hosts.domain=52.70.79.113 \
    --set global.hosts.externalIP=52.70.79.113 \
    --set global.ingress.class= \
    --set certmanager-issuer.email=stonyc@cj.net \
    --dry-run # Remove to proceed with the installation.
```

Get the initial root password and log-in:

```bash
kubectl get secret gitlab-gitlab-initial-root-password -ojsonpath='{.data.password}' | base64 --decode ; echo
```



kubectl -n kube-system delete deployment tiller-deploy
kubectl delete serviceaccount -n kube-system tiller
kubectl delete clusterrolebindings.rbac.authorization.k8s.io -n kube-system tiller-cluster-rule
kubectl delete services -n kube-system tiller-deploy

kubectl create -f kubernetes-tiller-deploy.yml 

