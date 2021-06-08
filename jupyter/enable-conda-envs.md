##### **`SYSTEM ACCESS TO CONDA`**

Install `conda` for the whole system:

```bash
# Add the Anaconda gpg key:
curl https://repo.anaconda.com/pkgs/misc/gpgkeys/anaconda.asc | gpg --dearmor > conda.gpg 
sudo install -o root -g root -m 644 conda.gpg /etc/apt/trusted.gpg.d/

# Add the Debian repository:
sudo echo "deb [arch=amd64] https://repo.anaconda.com/pkgs/misc/debrepo/conda stable main" > /etc/apt/sources.list.d/conda.list

# Install conda:
sudo apt update
sudo apt install conda

# Link the conda shell for execution at login:
sudo ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh
```

Install a default `conda` environment for all users:

```bash
# Create a folder for conda envs:
sudo mkdir -p /opt/conda/envs/

# Create a new conda environment:
sudo /opt/conda/bin/conda create --prefix /opt/conda/envs/python python=3.7 ipykernel
```

Enable access to the kernel in one of two ways:

```bash
# JupyterHub only:
sudo /opt/conda/envs/python/bin/python -m ipykernel install --prefix=/opt/jupyterhub/ --name 'python' --display-name "Python (default)"

# Permanent system access:
sudo /opt/conda/envs/python/bin/python -m ipykernel install --prefix /usr/local/ --name 'python' --display-name "Python (default)"
```

Instructions for user-created `conda` environments:

```bash
# First create a conda environment to your liking, then enable kernel access:
/path/to/kernel/env/bin/python -m ipykernel install --name 'python-my-env' --display-name "Python My Env"
```

##### **`QUICK START`**

Go to the following website: `http://<your-domain-name>:8080` and log-in with your server username and password.

##### **`REFERENCES`**

https://jupyterhub.readthedocs.io/en/stable/installation-guide-hard.html
