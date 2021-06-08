# **GitLab**

**First update package manager and repositories:**

```bash
sudo apt update
sudo apt upgrade
```

**Install required dependencies:**

```bash
sudo apt-get install ca-certificates curl openssh-server postfix mailutils
```

**Add GitLab to the list of apt repositories:**

```bash
curl -LO https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh
cd /tmp
# Not yet available for 19.04, change bionic to disco:
sudo os=ubuntu dist=bionic bash /tmp/script.deb.sh
```

**Install GitLab:**

```bash
sudo apt-get install gitlab-ce
```

**Edit the GitLab configuration file:**

```bash
sudo vi /etc/gitlab/gitlab.rb
```

**Point the configuration script to the desired domain or IP address:**

If using an IP address, edit the following line:

```bash
external_url 'http://<ip-address>'
```
If using a domain server:
```bash
external_url 'https://<domain-address>'
# Uncomment and edit the following also:
letsencrypt['enable'] = true
letsencrypt['contact_emails'] = ['user1@email.com','user2@email.com']
```

**Save the changes to the configuration, exit, and then run the following command to finish the install:**

```bash
sudo gitlab-ctl reconfigure
```

**Setup administrator password:**

After (re-)configuration has completed, open a browser and navigate to [https://<domain-address>]() or [https://<ip-address>](). Set the administrator password using the provided interface.

![Admin Password](https://github.com/stonyc/gists/blob/master/gitlab/assets/gitlaba-800x600.jpg)

**Register user accounts:**

Create an account, log in, and the GitLab web interface is ready to be used.

**Adding SSH keys:**

In order to push and pull your projects, remote machine account ssh-keys must be added to your account profile. If not already generated, create private and public keys using the following command on each remote machine:

```bash
ssh-keygen -t rsa
```

When prompted, press Enter to accept the default location to store the keys. By default, they are in the user's home directory in the hidden .ssh folder:

```bash
groot@starlord:~$ ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/groot/.ssh/id_rsa): Enter
Created directory '/home/groot/.ssh'.
Enter passphrase (empty for no passphrase): Enter
Enter same passphrase again: Enter
Your identification has been saved in /home/groot/.ssh/id_rsa.
Your public key has been saved in /home/groot/.ssh/id_rsa.pub.
```

Navigate to the `Settings` menu using the `Profile` drop-down menu in the upper-right of the GitLab interface, enter the `SSH Keys` interface, and copy the output of the following command to the `Key` entry, then click `Add key`:

```bash
cat ~/.ssh/id_rsa.pub
```

![SSH Keys](https://github.com/stonyc/gists/blob/master/gitlab/assets/gitlabb-800x600.jpg)

You should now have all of the familiar `git` commands available to use through GitLab.
