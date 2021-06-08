**Enable Netboot image in Grub boot menu:**

Edit `/etc/grub.d/40_custom` to look like:

```bash
#!/bin/sh
exec tail -n +3 $0
# This file provides an easy way to add custom menu entries.  Simply type the
# menu entries you want to add after this comment.  Be careful not to change
# the 'exec tail' line above.
menuentry "Ubuntu 19.04 Netboot Install" {
  set root='hd0,gpt2'
  linux /linux
  initrd /initrd.gz
}
```

Enable the Grub menu by default through commenting out the following line `/etc/default/grub`:

```bash
#GRUB_TIMEOUT=0
```

Finalize the updates:

```bash
sudo update-grub
```
