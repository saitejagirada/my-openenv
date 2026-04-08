---
title: Customer Support Triage
emoji: 🎧
colorFrom: blue
colorTo: indigo
sdk: docker
sdk_version: "1.0.0"
python_version: "3.10.0"
app_file: app.py
pinned: false
---
# Customer Support Triage Environment

A real-world customer support simulation environment requiring information extraction, system actions, and routing. 
Built using the official OpenEnv interface specification.

## Overview
This environment simulates a text-based customer support chat system. The agent acts on incoming support tickets and chooses actions such as asking the user for missing info, processing refunds, or routing the ticket to specialized teams. 

## Action & Observation Spaces
- **Observation:** `ticket_id`, `customer_message`, `history`, `missing_info`, `status`, `refund_processed`, `done`, `reward`.
- **Action:** 
  - `action_type`: One of 'ROUTE', 'ASK_INFO', 'REFUND', 'CLOSE'
  - `argument`: The specific queue (e.g., 'BILLING'), the info to ask for (e.g., 'serial_number'), or order to refund.

## Tasks
1. **easy_password_reset** (Easy): A simple IT support routing task requiring no additional info.
2. **medium_hardware_issue** (Medium): Requires the agent to first ask for the `serial_number` before routing to hardware support.
3. **hard_refund_processing** (Hard): Requires the agent to ask for `order_id` and `photo_evidence`, process a refund by taking the REFUND action, and finally route the ticket to billing.

## Usage
Start the environment server using Docker:
```bash
docker build -t customer-support-env .
docker run -p 8000:8000 customer-support-env
```
Or start directly via python:
```bash
uvicorn server.app:app --port 8000
```
Run the baseline baseline inference script:
```bash
python inference.py
```
