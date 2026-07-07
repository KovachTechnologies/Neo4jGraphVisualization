# Provisioning and Configuration of Linkurious Server (ri.4xlarge)

**Document Owner:** [Your Name / Team]  
**Version:** 1.0  
**Date:** [Insert Date]  
**Purpose:** This document provides standardized, step-by-step instructions for provisioning and configuring a Linkurious Enterprise server on AWS EC2 ri.4xlarge (24 vCPU, 128 GiB RAM) as a frontend/visualization layer connected to Neo4j (or other graph databases). This is a standalone deployment.

## Overview

- **Instance Type:** `ri.4xlarge` (Memory-optimized, suitable for Linkurious workloads)
- **Storage:**
  - `/linkurious` — 100 GB (Application binaries, configuration, data, logs)
- **Service User/Group:** Recommended: `linkurious:linkurious` (or align with corporate standards; can reuse `neo4jcam` if desired)
- **Linkurious Version:** Latest stable (refer to official documentation for exact version)
- **Key Optimizations:** Dedicated server for UI/performance, SSD storage, proper memory allocation for visualizations and Elasticsearch (if embedded).

This configuration follows corporate security and operational standards. Linkurious connects to the Neo4j instance (see separate Neo4j guide).

## Prerequisites

- AWS account with appropriate IAM permissions.
- Approved security group allowing inbound traffic on Linkurious default port (typically 3000) from trusted sources only.
- SSH access using approved key pair.
- Corporate Linux hardening baseline applied.
- Neo4j server already provisioned and accessible (private networking preferred).
- Linkurious Enterprise license.
- Backup and monitoring agents ready.

## Step-by-Step Provisioning and Configuration

### 1. Provision EC2 Instance and Attach Storage

1. Launch an `ri.4xlarge` instance in the approved VPC and subnet.
2. Attach a 100 GB EBS volume (gp3 recommended) mounted at `/linkurious`.
3. Tag all resources per corporate policy.
4. Use an approved AMI.

### 2. Mount and Configure Filesystem

1. SSH into the instance.
2. Format and mount the volume:

   ```bash
   sudo mkfs -t xfs /dev/nvme1n1   # Adjust device name (use lsblk)
   sudo mkdir -p /linkurious
   sudo mount /dev/nvme1n1 /linkurious
   ```

3. Add to `/etc/fstab` using UUID for persistence.
4. Disable swap if not needed:

   ```bash
   sudo swapoff -a
   sudo sed -i '/ swap / s/^/#/' /etc/fstab
   ```

### 3. Create Service User and Permissions

```bash
sudo useradd -m -s /bin/bash linkurious
sudo groupadd linkurious
sudo usermod -aG linkurious linkurious

sudo chown -R linkurious:linkurious /linkurious
sudo chmod -R 750 /linkurious
```

### 4. Install Linkurious

1. Download the latest Linkurious Enterprise Linux package from the official Customer Center.
2. Extract to `/linkurious` (e.g., `/linkurious/linkurious-linux`).
3. Follow official installation steps (usually involves running `install.sh` or manual setup).

   Refer to: https://doc.linkurious.com/admin-manual/latest/install/

### 5. Configure Linkurious

Main configuration file: `/linkurious/linkurious-linux/data/config/production.json`

Key sections (edit via UI after initial start or directly):

- **Data Sources:** Configure connection to Neo4j (host, port, credentials, user with admin/architect role).
- **Server Settings:** Port (default 3000), HTTPS (recommended in prod), authentication.
- **Elasticsearch:** Use embedded or external (external recommended for large deployments).
- **Memory/Performance:** Linkurious runs on Node.js; monitor heap usage. The 128 GiB RAM provides ample headroom for visualizations and concurrent users.

Example basic Neo4j datasource snippet (adapt as needed):

```json
{
  "dataSources": [
    {
      "graphdb": {
        "vendor": "neo4j",
        "url": "bolt://your-neo4j-private-ip:7687/",
        "user": "neo4j",
        "password": "your-secure-password"
      }
    }
  ]
}
```

Enable authentication, use private networking, and set production flags.

### 6. Start as System Service

1. Install as systemd service (recommended) per official docs.
2. Example service file (`/etc/systemd/system/linkurious.service`):

   ```ini
   [Unit]
   Description=Linkurious Enterprise
   After=network.target

   [Service]
   Type=simple
   User=linkurious
   WorkingDirectory=/linkurious/linkurious-linux
   ExecStart=/linkurious/linkurious-linux/start.sh
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now linkurious
   ```

### 7. Verification and Validation

1. Check service status: `sudo systemctl status linkurious`
2. Access UI at `http://server-ip:3000` (or HTTPS).
3. Configure license and admin account on first login.
4. Add Neo4j datasource and test visualizations.
5. Monitor logs in `/linkurious/linkurious-linux/logs/`.

### 8. Monitoring, Backup, and Maintenance

- **Monitoring:** CPU, memory (Node.js heap), disk I/O, application logs. Integrate with corporate tools.
- **Backup:** Backup `/linkurious/linkurious-linux/data/` regularly (configuration, saved visualizations).
- **Security:** Use HTTPS, strong auth, restrict ports, keep updated. Private network to Neo4j.
- **Scaling:** For higher user load, consider load balancing or larger instance. Embedded Elasticsearch may need tuning for large graphs.

## Approval and Change Management

Follow corporate change management. Coordinate with DBA/Graph Platform team for integration with Neo4j.

**Related Documents:**  
- Neo4j Single-Instance Guide  
- Corporate EC2 / Security Standards  
- Linkurious Official Documentation

---
*This document is for internal use only. Last reviewed: [Date]*
