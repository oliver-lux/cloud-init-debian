# Hetzner Data Centers

| Code | Location          | Country | Example latency* |
|------|--------------------|---------|-------------------|
| NBG  | Nuremberg          | DE      | 15 ms             |
| FSN  | Falkenstein        | DE      | 17 ms             |
| HEL  | Helsinki           | FI      | 34 ms             |
| ASH  | Ashburn            | US      | 96 ms             |
| HIL  | Hillsboro          | US      | 163 ms            |

\* Measured from one reference location — re-run the check below from your own
network before picking a region.

## Measuring latency from your own location

```bash
sudo apt install nmap

nping -c 20 \
  nbg.icmp.hetzner.com \
  fsn.icmp.hetzner.com \
  hel.icmp.hetzner.com \
  ash.icmp.hetzner.com \
  hil.icmp.hetzner.com
```
