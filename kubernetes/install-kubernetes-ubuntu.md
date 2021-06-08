This document details how to install and configure Kubernetes and Docker on a Ubuntu server.

---
# **1. Install Kubernetes**

**The following steps must be completed on the master-node and each worker-node.**

First update the server repository and update packages:

```bash
sudo apt update
sudo apt upgrade
```

Add the following list of IP addresses and hostnames to the `/etc/hosts` file on each master and worker node. Replace the IP addresses with those for your nodes:

```bash
52.70.79.113	k8s-starlord
52.70.50.41	k8s-gamora
52.70.50.42	k8s-rocket
52.70.50.43	k8s-groot
52.70.50.44	k8s-drax
```

Test that all IP addresses get resolved as a hostname:

```bash
ping -c 3 k8s-starlord
ping -c 3 k8s-gamora
ping -c 3 k8s-rocket
ping -c 3 k8s-groot
ping -c 3 k8s-drax
```

### **Install Docker**
---

Install Docker using the Ubuntu software repository:

```bash
sudo apt install docker.io -y
```

After installation completes, start the Docker service and enable it to launch on system boot:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### **Disable swap memory**
---

Check the swap table list, and then disable swap:

```bash
sudo swapon -s
sudo swapoff -a
```

To disable swap permanently, edit the `/etc/fstab` file by commenting out the swap line:

```bash
# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
#
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
# / was on /dev/sda3 during installation
UUID=29d135eb-faaf-4dcb-9a5b-c1271a6cb075 /               ext4    errors=remount-ro 0       1
# /boot/efi was on /dev/sda1 during installation
UUID=6229-6C02  /boot/efi       vfat    umask=0077      0       1
#/swapfile                                 none            swap    sw              0       0
```

Reboot the system:

```bash
sudo reboot
```

### **Install kubeadm packages**
---

Install `apt-transport-https`:

```bash
sudo apt install -y apt-transport-https
```

Add the Kubernetes repository key:

```bash
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
```

Add the Kubernetes repository to the `/etc/apt/sources.list.d` directory:

```bash
cd /etc/apt/
sudo vim sources.list.d/kubernetes.list
```

Paste the following repository into the source list file:

```bash
deb http://apt.kubernetes.io/ kubernetes-xenial main
```

Note: the 16.04 Xenial is still the latest supported repository for kubeadm at the time this document was created.

Update the repository, and then install kubeadm packages:

```bash
sudo apt update
sudo apt upgrade
sudo apt install -y kubeadm kubelet kubectl
```

---
# **2. Initialize the Kubernetes cluster**

**The following commands apply only to the master-node.**

Initialize the kubeadm cluster:

```bash
sudo kubeadm init \
--pod-network-cidr=52.70.79.0/24 \
--apiserver-advertise-address=52.70.79.113 \
--kubernetes-version "1.15.3"
```

`--apiserver-advertise-address`:

    This is the IP address that Kubernetes should advertise its API on (default: master-node)

`--pod-network-cidr`:

    The range of IP addresses for the pod network

Take note of the command and token that may be used to added worker-nodes to the Kubernetes cluster:

```bash
Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 52.70.79.113:6443 --token hhh4r6.1c7zwu2krhk0k5ya \
    --discovery-token-ca-cert-hash sha256:e003c568d5e57124f39997b16e421c7202948fd27a0be20d084fcadf9af1da09 
```

Create a new `.kube` directory and copy the configure `admin.conf` file from `/etc/kubernetes/`:

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Next, deploy the `flannel` network to the Kubernetes cluster using the `kubectl` command:

```bash
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

Wait a few minutes, then check the Kubernetes cluster:

```bash
kubectl get nodes
kubectl get pods --all-namespaces
```

---
# **3. Adding worker nodes to the Kubernetes cluster**

Connect to each worker-node and run the kubeadm join command provided earlier:

```bash
kubeadm join 52.70.79.113:6443 --token hhh4r6.1c7zwu2krhk0k5ya \
    --discovery-token-ca-cert-hash sha256:e003c568d5e57124f39997b16e421c7202948fd27a0be20d084fcadf9af1da09 
```

Wait a few minutes, then on the master-node check the Kubernetes cluster:

```bash
kubectl get nodes
```

---
# **4. Deploy Kubernetes web UI (Dashboard)**

By default, the web dashboard is not deployed. To deploy the dashboard:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta1/aio/deploy/recommended.yaml
```

The dashboard may then be accessed by running the command:

```bash
kubectl proxy
```

This will open a login screen at:

     http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/

However, we do not yet have the credentials to access the dashboard. Therefore we will need to make an account to administer the Kubernetes cluster through the dashboard.

First, save the following snippet into a file called `dashboard-adminuser.yml`:

```bash
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kube-system
```

Then run the command:

```bash
kubectl apply -f dashboard-adminuser.yml
```

Next, save the following into a file called `admin-role-binding.yml`:

```bash
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kube-system
```

Then run the command:

```bash
kubectl apply -f admin-role-binding.yml
```

Finally, get the admin-user token using the following command:

```bash
kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}')
```

The result should look something like:

     Name:         admin-user-token-bmmrdNamespace:    kube-system
     Labels:       <none>
     Annotations:  kubernetes.io/service-account.name: admin-user
                   kubernetes.io/service-account.uid: a164478c-4545-11e9-a69b-0800276c3e95
     Type:              kubernetes.io/service-account-tokenData
     ====
     ca.crt:     1025 bytes
     namespace:  11 bytes
     token:      <your token will be shown here>

Copy and paste the token into the dashboard log-in screen, and you should then be logged in with administrator-level privileges to create, modify and deploy pods and services in your cluster.

---
# **Recommended resources**

Kubernetes:
```bash
https://tutorials.ubuntu.com/tutorial/install-a-local-kubernetes-with-microk8s#3
https://virtualizationreview.com/articles/2019/01/30/microk8s-part-2-how-to-monitor-and-manage-kubernetes.aspx
https://www.howtoforge.com/tutorial/how-to-install-kubernetes-on-ubuntu/
```

GitLab:
```bash
https://www.techrepublic.com/article/how-to-set-up-a-gitlab-server-and-host-your-own-git-repositories/
```

