# NMC Automation (Vertiv UPS Network Management Cards)

A Python tool that automates the initial configuration of Vertiv UPS network management cards (NMCs) — replacing a manual, per-device setup process with a scripted one.

## What it does

Network management cards let you monitor and manage a UPS remotely, but setting one up by hand means logging into each device individually and clicking through the same set of configuration screens. This tool automates that setup across two different NMC models, each of which exposes a different, undocumented API:

- **System configuration** — device name, site identifier, contact info
- **Networking** — static IP, subnet, gateway, DNS
- **Time** — NTP server and time zone
- **Email alerting** — SMTP server and alert recipient
- **User management** — creates an admin-level user account

## Why I built it

I made this because I got tired of having to configure network management cards. The RDU101 api doc doesn't show how to set email settings which is why SessionToken exists.

## Design

- **Authentication is kept as standalone functions** (`rdu120_get_token`, `rdu101_get_token`, `get_act_token`) rather than methods, since auth is a stateless "give me credentials, get back a token" operation — separating it from the stateful device classes keeps it easy to test and reason about independently.
- **`NMCDevice`** is the base class holding shared device configuration (IP, protocol, credentials, network settings) as instance attributes, set once at construction.
- **`RDU101`** and **`RDU120`** subclass `NMCDevice`, each implementing the configuration methods (`set_network`, `set_system_info`, `add_user`, etc.) against that model's specific API shape.
- **`SessionToken`** wraps an `NMCDevice` instance to handle the second, browser-scraped auth flow needed for certain settings (site identifier, email config) — implemented via composition rather than inheritance, since it uses a device rather than being one.

## Tech stack

Python, `requests`, `dataclasses` (for structured user input)

## Project structure

```
http_request.py          # standalone authentication functions
user_input.py              # UserInfo dataclass + interactive input collection
nmc_device.py                # NMCDevice base class
rdu101/
    rdu101.py                  # RDU101(NMCDevice)
    rdu101_main.py               # entry point for RDU101 devices
rdu120/
    rdu120.py                  # RDU120(NMCDevice)
    rdu120_main.py               # entry point for RDU120 devices
```

## Setup

1. Install dependencies:
   ```bash
   pip install requests
   ```
2. Run the entry point for your device model:
   ```bash
   python rdu120/rdu120_main.py
   ```
3. Follow the interactive prompts for device IP, credentials, and network settings.

## Possible next steps

- Add error handling around failed authentication instead of letting a bad response raise a raw `KeyError`
- Reduce duplication between the RDU101 and RDU120 configuration methods where the underlying operation is conceptually the same
- Move interactive `input()` prompts behind a config file option for non-interactive/batch use
- Create a gui for easier use
