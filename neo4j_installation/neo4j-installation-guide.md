# Provisioning and Configuration of Single-Instance Neo4j Server (r6.32xlarge)

**Document Owner:** [Your Name / Team]  
**Version:** 1.0  
**Date:** [Insert Date]  
**Purpose:** This document provides standardized, step-by-step instructions for provisioning and configuring a single-instance Neo4j database server on AWS EC2 r6.32xlarge (128 vCPU, 1024 GiB RAM) optimized for high-performance graph workloads. This is a standalone (non-clustered) deployment.

## Overview

- **Instance Type:** `r6.32xlarge` (Memory-optimized)
- **Storage:**
  - `/NEO4J` — 100 GB (Application binaries, logs, plugins, configuration)
  - `/NEO4J_DATA` — 3 TB (Database files, transaction logs)
  - `/NEO4J_APPS` — 10 GB (Automation scripts, import files for LOAD CSV)
- **Service User/Group:** `neo4jcam:neo4jcam`
- **Neo4j Version:** 5.x (Enterprise or Community)
- **Key Optimizations:** Large page cache for graph data, balanced heap, custom directory layout for performance and separation of concerns.

This configuration prioritizes performance, security, observability, and maintainability while following corporate security and operational standards.

## Prerequisites

- AWS account with appropriate IAM permissions for EC2 provisioning, EBS volumes, and tagging.
- Approved security group allowing inbound traffic on required ports (Bolt 7687, HTTP 7474 if needed) from trusted sources only.
- SSH access using approved key pair.
- Corporate Linux hardening baseline applied to the AMI.
- Backup and monitoring agents (e.g., CloudWatch, Prometheus, or corporate tooling) ready for deployment.
- Neo4j license (if Enterprise).

## Step-by-Step Provisioning and Configuration

### 1. Provision EC2 Instance and Attach Storage

1. Launch an `r6.32xlarge` instance in the approved VPC and subnet.
2. Attach the following EBS volumes (use gp3 or io2 for performance as required):
   - 100 GB volume → mount point `/NEO4J`
   - 3 TB volume → mount point `/NEO4J_DATA`
   - 10 GB volume → mount point `/NEO4J_APPS`
3. Tag all resources per corporate tagging policy.
4. Ensure the instance is launched with the approved AMI and security group.

### 2. Mount and Configure Filesystems

1. SSH into the instance as an administrator.
2. Format and mount the volumes (example using `xfs`):

   ```bash
   sudo mkfs -t xfs /dev/nvme1n1   # Adjust device names as needed (use lsblk)
   sudo mkfs -t xfs /dev/nvme2n1
   sudo mkfs -t xfs /dev/nvme3n1

   sudo mkdir -p /NEO4J /NEO4J_DATA /NEO4J_APPS

   sudo mount /dev/nvme1n1 /NEO4J
   sudo mount /dev/nvme2n1 /NEO4J_DATA
   sudo mount /dev/nvme3n1 /NEO4J_APPS
   ```

3. Add entries to `/etc/fstab` for persistence (use UUIDs for reliability):

   ```bash
   sudo blkid   # Note UUIDs
   # Then edit /etc/fstab accordingly
   ```

4. Disable swap (recommended for dedicated Neo4j servers):

   ```bash
   sudo swapoff -a
   sudo sed -i '/ swap / s/^/#/' /etc/fstab
   ```

### 3. Create Service User and Set Permissions

```bash
sudo useradd -m -s /bin/bash neo4jcam
sudo groupadd neo4jcam
sudo usermod -aG neo4jcam neo4jcam   # or appropriate group

sudo mkdir -p /NEO4J/logs /NEO4J/plugins /NEO4J_DATA/{databases,transactions,dumps} /NEO4J_APPS

sudo chown -R neo4jcam:neo4jcam /NEO4J /NEO4J_DATA /NEO4J_APPS
sudo chmod -R 750 /NEO4J /NEO4J_DATA /NEO4J_APPS
```

### 4. Install Neo4j

1. Download and install Neo4j 5.x following official documentation (tar.gz or package manager).
2. Set environment variables in the service definition or shell profile:
   - `NEO4J_HOME=/NEO4J/neo4j` (adjust to actual installation path)
   - `NEO4J_CONF=/NEO4J/conf`

### 5. Configure Neo4j (`neo4j.conf`)

Copy the following configuration into `$NEO4J_CONF/neo4j.conf` (or the appropriate location):

```conf
# =============================================================================
# Neo4j Configuration - Single Instance (Standalone)
# Optimized for: AWS r6.32xlarge (128 vCPU, 1024 GiB RAM)
# =============================================================================

# Memory Configuration
server.memory.heap.initial_size=32g
server.memory.heap.max_size=32g
server.memory.pagecache.size=850g

# Directory Configuration
server.directories.data=/NEO4J_DATA
server.directories.logs=/NEO4J/logs
server.directories.import=/NEO4J_APPS
server.directories.plugins=/NEO4J/plugins
server.directories.transaction.logs.root=/NEO4J_DATA/transactions

# Connectors
server.bolt.enabled=true
server.bolt.listen_address=0.0.0.0:7687

server.http.enabled=true
server.http.listen_address=0.0.0.0:7474
server.https.enabled=false

# Production Settings
dbms.usage_report.enabled=false
server.config.strict_validation.enabled=false

dbms.logs.query.enabled=true
dbms.logs.query.threshold=10s

dbms.tx.logs.rotation.retention_policy=30 days
```

**Note:** Review and adjust memory settings after initial data loading using `neo4j-admin server memory-recommendation`.

### 6. Create and Enable Systemd Service (Recommended)

Create `/etc/systemd/system/neo4j.service` with `User=neo4jcam` and appropriate `ExecStart`.

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now neo4j
```

### 7. Verification and Validation

1. Check service status: `sudo systemctl status neo4j`
2. Verify memory allocation via Cypher:  
   `SHOW SETTINGS YIELD name, value WHERE name CONTAINS 'memory'`
3. Run `neo4j-admin server memory-recommendation` and tune as needed.
4. Test connectivity with Neo4j Browser or Cypher Shell.
5. Validate page cache hit ratio and query performance under load.

### 8. Monitoring, Backup, and Maintenance

- **Monitoring:** Integrate with corporate monitoring (CloudWatch, Prometheus/Grafana). Key metrics: page cache hit ratio, heap usage, disk I/O, query latency.
- **Backup:** Use `neo4j-admin database backup` to `/NEO4J_DATA/backups` or corporate backup solution. Schedule regular full and incremental backups.
- **Logging:** Review `/NEO4J/logs` regularly. Forward logs to corporate SIEM if required.
- **Security:** Enforce least privilege, rotate credentials, keep Neo4j and OS patched. Disable unnecessary ports.
- **Scaling Note:** This is a single-instance setup. Future clustering requires additional configuration review.

## Approval and Change Management

All changes must follow corporate change management process. Contact [DBA/Platform Team] for production deployment.

**Related Documents:**  
- Corporate EC2 Provisioning Standard  
- Neo4j Operations Runbook  
- AWS Security Baseline

---
*This document is for internal use only. Last reviewed: [Date]*
