# Create bootable usb

This process **erases everything** on the USB drive. Double-check the device name to avoid data loss.

Identify the USB drive and unount its partitions (check in `lsblk` under “MOUNTPOINT”):

```bash
lsblk
sudo umount /dev/sdX*
```

Replace `X` with the USB device letter (e.g., `b` for `/dev/sdb`).

Write the ISO to the USB drive

```bash
sudo dd if=/path/to/your.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

* `if=` → path to your ISO file
* `of=` → your USB device (e.g., `/dev/sdb`)
* `bs=4M` → block size
* `status=progress` → show progress
* `oflag=sync` → flush writes properly

It may take a few minutes. Once it's done, you'll see the prompt return.

Safely remove the USB

```bash
sync
sudo eject /dev/sdX
```
