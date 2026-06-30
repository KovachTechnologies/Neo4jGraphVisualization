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
