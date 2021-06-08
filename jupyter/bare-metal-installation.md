### **`BARE METAL INSTALL OF JUPYTER HUB`**

Requirements:
* Ubuntu v20.04

##### **`SETUP`**

Setup JupyterHub and JupyterLab in a virtual environment:

```bash
sudo python -m venv /opt/jupyterhub/
```

Install required minimal required packages:

```bash
sudo /opt/jupyterhub/bin/python3 -m pip install wheel
sudo /opt/jupyterhub/bin/python3 -m pip install jupyterhub jupyterlab
sudo /opt/jupyterhub/bin/python3 -m pip install ipywidgets

# Install dependencies for configurable-http-proxy:
sudo apt install nodejs npm

# Install configurable-http-proxy:
npm install -g configurable-http-proxy
```

Generate the default configuration for JupyterHub:

```bash
# Create a directory for the configuration file:
sudo mkdir -p /opt/jupyterhub/etc/jupyterhub/
cd /opt/jupyterhub/etc/jupyterhub/

# Generate the configuration file:
sudo /opt/jupyterhub/bin/jupyterhub --generate-config

# Enable domain name and configure port access:
c.JupyterHub.bind_url = 'http://<your-domain-name>:8080'

# Start-up after login should default to JupyterLab:
c.Spawner.default_url = '/lab'
```

Setup JupyterHub to run as a system service upon server restart:

```bash
# First create a folder for the service file:
sudo mkdir -p /opt/jupyterhub/etc/systemd

# Create the following service file:
vim /opt/jupyterhub/etc/systemd/jupyterhub.service
```

Define the service:

```bash
[Unit]
Description=JupyterHub
After=syslog.target network.target

[Service]
User=root
Environment="PATH=/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/opt/jupyterhub/bin"
ExecStart=/opt/jupyterhub/bin/jupyterhub -f /opt/jupyterhub/etc/jupyterhub/jupyterhub_config.py

[Install]
WantedBy=multi-user.target
```

Link the service to `systemd` and enable JupyterHub as a service:

```bash
# Create a symbolic link to the service file:
sudo ln -s /opt/jupyterhub/etc/systemd/jupyterhub.service /etc/systemd/system/jupyterhub.service

# Direct systemd to reload its configuration files:
sudo systemctl daemon-reload

# Enable the service and start JupyterHub:
sudo systemctl enable jupyterhub.service
sudo systemctl start jupyterhub.service
```

In case of error, restart the service:

```bash
# Restart the service in case of error:
systemctl restart jupyterhub
```

