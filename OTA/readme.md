This directory store all Neviweb zigbee sniffing where we can find OTA update.

To view the different files you need wireshark and the following key to decode data

- Neviweb GT130 key: 60ccee07009651c60e1f8c1b05562f2c
- My ZHA key: bfaa6457733b88185b173089636238f6

In the file with wireshark look for the following steps:

- OTA: Query Next Image Request
- OTA: Query Next Image Response 
 - payload should be:
 - File Version: 0x01020001, firmware 1.2.0 exemple
 - Image Size xxxxxx [Bytes], file size
- OTA: Image Block Request
- OTA: Image Block Response
- OTA: Image Page Request
- OTA: Image Block Response
- OTA: Image Block Request
- OTA: Image Block Response
...
- OTA: Upgrade End Request
- OTA: Upgrade End Response
