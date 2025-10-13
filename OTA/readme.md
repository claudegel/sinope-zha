# ZigBee OTA Image Extraction Guide

This repository contains Neviweb ZigBee captures that include over-the-air (OTA) updates. This guide will help you extract OTA images from these captures.

## Prerequisites

- [Wireshark](https://www.wireshark.org/) - For analyzing capture files
- [zigpy-cli](https://github.com/zigpy/zigpy-cli) - For reconstructing OTA images
- [tshark](https://www.wireshark.org/docs/man-pages/tshark.html) - Command-line utility for Wireshark (required by zigpy-cli)
- [editcap](https://www.wireshark.org/docs/man-pages/editcap.html) - Command-line utility for Wireshark to split pcapng file in smaller files

## Decryption Keys

To decode the encrypted ZigBee traffic, you'll need one of the following network keys:

| System | Network Key |
|--------|-------------|
| Neviweb GT130 | `60ccee07009651c60e1f8c1b05562f2c` |
| ZHA | `bfaa6457733b88185b173089636238f6` |

## Identifying OTA Updates in Wireshark

When analyzing the capture files with Wireshark, look for the following sequence of ZigBee OTA messages:

1. **OTA: Query Next Image Request** - Device checking for updates
2. **OTA: Query Next Image Response** - Server confirming update availability
   - Contains important metadata:
     - File Version: e.g., `0x01020001` (firmware version 1.2.0)
     - Image Size: Total size in bytes
3. **OTA: Image Block Request** - Device requesting specific blocks of the update
4. **OTA: Image Block Response** - Server sending the requested blocks
5. **OTA: Image Page Request** - Device requesting a page of blocks
6. **OTA: Image Block Response** - Server sending the requested blocks
7. **Multiple Request/Response cycles** - Transferring all blocks
8. **OTA: Upgrade End Request** - Device confirming full reception of the update
9. **OTA: Upgrade End Response** - Server confirming successful transfer

During the update you can follow the process by checking the file offset value in each OTA: Image Block Response. 
Once you know the last block number you can split the pcapng file it it is very large by using Wireshark editcap command.

## Reconstructing OTA Images

To extract the OTA image from capture files, use the zigpy-cli tool:

```bash
zigpy ota reconstruct-from-pcaps \
  --add-network-key aa:bb:cc:dd:ee:ff:00:11:22:33:44:55:66:77:88:99 \
  --output-root ./extracted/ \
  *.pcap
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `--add-network-key` | The ZigBee network key for decryption |
| `--output-root` | Directory where extracted images will be saved |
| `*.pcap` | Pattern matching capture files to process (can use `*` to process all files) |

## Understanding the Output

A successful extraction will produce output similar to:

```
Constructing image type=0x0034, version=0x00010300, manuf_code=0x119c: 316038 bytes
ota_t0x0034_m0x119c_v0x00010300.ota
Type: <class 'zigpy.ota.image.OTAImage'>
Header: OTAImageHeader(
  upgrade_file_id=200208670, 
  header_version=256, 
  header_length=56, 
  field_control=<FieldControl: 0>, 
  manufacturer_id=4508, 
  image_type=52, 
  file_version=66304, 
  stack_version=2, 
  header_string=<''>, 
  image_size=316038, 
  device_specific_file=False,
  hardware_versions_present=False, 
  security_credential_version_present=False
)
Number of subelements: 3
Validation result: ValidationResult.VALID
```

## Troubleshooting

If you see an error message like:

```
Missing 28 bytes starting at offset 0x00040D62: filling with 0xAB
```

This indicates that the capture is missing data blocks. The tool will attempt to fill the gaps with placeholder bytes (`0xAB`), but the resulting image will likely be corrupted. In this case, you'll need to capture a new, more complete OTA update session.

## Notes

- Successful extraction requires a complete capture of the entire OTA update process
- Any missing packets can result in a corrupted image
- The quality of your ZigBee sniffing hardware will impact capture completeness

---

*For more information about ZigBee OTA updates, refer to the [ZigBee OTA Upgrade Cluster specification](https://zigbeealliance.org/)*
