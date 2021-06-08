Install Docker in Ubuntu v18.04+:

```bash
# Remove existing Docker installations:
sudo apt-get remove docker docker-engine docker.io
# Install Docker:
sudo apt-get update
sudo apt install docker.io
# Start and automate loading of Docker:
sudo systemctl start docker
sudo systemctl enable docker
```

Add user to docker group to eliminate `sudo` requirement:

```
# Add the docker group:
sudo groupadd docker # Probably not necessary.
# Add a user to the docker group:
sudo usermod -aG docker <username>
```
