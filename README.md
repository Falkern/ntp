# NTP Amplification DOS Attack

## Overview

- This Python script demonstrates an NTP amplification denial-of-service (DoS) attack. It uses a list of NTP servers to flood a specified target with NTP response packets. This can be used for educational purposes to understand the mechanics of NTP amplification attacks.

> **Warning:** This script should only be used in a controlled environment with explicit permission from the target. Unauthorized use of this script can lead to legal consequences.

## What is an NTP DoS Attack?
- An NTP DoS attack floods a target with traffic by tricking time servers into sending massive responses to the victim, causing slowdowns or crashes.
  
## Requirements

- Python 3.x
- Scapy library

You can install Scapy using pip:

```bash
pip install scapy
```

## Usage

To run the script, execute the following command in your terminal:

```bash
./ntp_ddos.py <target_ip> <ntp_server_list> <number_of_threads>
```

## Parameters

- <target_ip>: The IP address of the target you want to flood.
- <ntp_server_list>: A text file containing a list of NTP server IP addresses (one per line).
- <number_of_threads>: The number of threads to use for the attack. Ensure this is less than or equal to the number of servers in your list.

## Notes

- The NTP server list file should contain one IP address per line.
- Make sure your thread count is less than or equal to your number of servers to avoid the script terminating prematurely.

## How It Works

- The script reads the target IP, NTP server list, and the number of threads from the command line arguments.
- It creates a UDP packet directed at the NTP server with a random source port.
- Multiple threads are spawned to continuously send these packets, amplifying the flood towards the target.

## Stopping the Attack

- To stop the attack, you can use CTRL+C in the terminal. This will safely exit the script and stop the packet sending.

## Disclaimer

- This script is for educational and research purposes only. Ensure you have permission to test against the target IP address. Misuse of this tool may violate local laws and regulations.
