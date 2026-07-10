**Bare Minimum Skills for Neo4j + Linkurious Server Maintainer**

**Role focus (as clarified):** Ongoing maintenance, monitoring, troubleshooting, and sysadmin tasks only. No server provisioning, Neo4j/Linkurious installation, configuration from scratch, or data migration/transfer. The person will work from existing runbooks (including the installation guides we already created) and escalate complex graph-specific issues.

Deep Neo4j or Linkurious expertise is **not** required (and is rare). The goal is a solid mid-level Linux/cloud sysadmin who can keep the services healthy, follow procedures, and learn the light application-specific commands.

### 1. Core Linux System Administration (Must-have)
- Strong proficiency with Linux (RHEL/CentOS/Rocky/Alma or Ubuntu LTS equivalents).
- Service management with **systemd** (`systemctl start/stop/restart/status/enable`, journalctl).
- File system & storage: mounting, fstab, permissions/ownership (`chown`/`chmod`), disk space monitoring (`df`, `du`), basic LVM or EBS volume awareness.
- User/group management and privilege escalation (`sudo`, service accounts like `neo4jcam` / `linkurious`).
- Package management and OS patching (yum/dnf or apt) following corporate change windows.
- Basic networking: checking ports (`ss`/`netstat`/`curl`/`telnet`), firewall rules (firewalld/iptables or security groups), DNS, connectivity tests between Linkurious and Neo4j.

### 2. Cloud / Infrastructure Basics (AWS-focused)
- Working knowledge of EC2 instance management (start/stop/reboot, console access, security groups, tagging).
- Ability to interpret CloudWatch metrics/alarms or equivalent corporate monitoring.
- Understanding of private networking / VPC connectivity (Linkurious → Neo4j bolt port).
- Snapshot / backup awareness for EBS volumes (even if actual backups are handled by another tool or team).

### 3. Monitoring, Logging & Observability
- Ability to check service health, resource usage (CPU, memory, disk I/O, network) using standard tools (`top`/`htop`, `free`, `iostat`, `vmstat`) or corporate agents.
- Log analysis: reading application logs (`/NEO4J/logs`, Linkurious logs), `journalctl`, and basic grepping/tailing.
- Understanding of key health indicators for these services (e.g., Neo4j page cache hit ratio, heap usage, query latency; Linkurious process uptime and UI availability).
- Responding to alerts and escalating when thresholds are breached.

### 4. Backup, Recovery & Maintenance Procedures
- Following documented backup/restore runbooks (e.g., `neo4j-admin database backup` / restore, Linkurious data directory backups).
- Performing routine maintenance windows: controlled restarts, log rotation, disk cleanup.
- Verifying backups (checksums, test restores on non-prod if required).
- Handling certificate renewals or basic TLS issues if HTTPS is in use.

### 5. Application-Specific Light Touch (Minimal – can be learned on the job)
- Neo4j:
  - Start/stop/status via systemd or `neo4j` commands.
  - Checking configuration and memory settings (`SHOW SETTINGS` via Cypher shell or Browser).
  - Viewing logs and basic status.
  - Restarting after OS patches.
  - Understanding the custom mount points and ownership (`neo4jcam:neo4jcam`).
- Linkurious:
  - Start/stop via systemd or start scripts.
  - Accessing the web UI for basic admin tasks (user management, checking datasources).
  - Restarting the service and verifying connectivity to Neo4j.
- Ability to follow existing runbooks and configuration files without rewriting them.

### 6. Security, Compliance & Soft Skills
- Applying OS and application security patches in controlled fashion.
- Following corporate change management, access control, and least-privilege principles.
- Documenting actions and updating runbooks when needed.
- Clear communication and escalation (know when a problem is OS-level vs. graph-database-level vs. application-level).
- Comfort with ticket systems and on-call rotation if required.

### Recommended Experience Level
- **Bare minimum**: 2–4 years of Linux system administration experience in a production environment (preferably with services that have high memory/disk requirements).
- Bonus (but not required): Any experience with Java-based services, Node.js services, monitoring tools (Prometheus/Grafana, CloudWatch, ELK), or databases (any RDBMS or NoSQL).
- The person should be able to become productive within 1–2 weeks using the existing documentation (Neo4j and Linkurious guides we prepared).

### Skills That Are **Not** Required
- Deep Cypher query writing or graph data modeling.
- Advanced Neo4j clustering, GDS, or APOC development.
- Linkurious plugin development or custom visualization coding.
- Infrastructure-as-code (Terraform/CloudFormation) for initial provisioning.
- Full-stack or application development skills.

### Suggested Hiring / Screening Approach
- Screen for solid Linux + systemd + basic cloud skills first.
- Give a short practical exercise: “Given this runbook, restart Neo4j safely, check memory settings, verify disk space on the custom mounts, and confirm Linkurious can still connect.”
- Prefer candidates who ask good clarifying questions about monitoring and escalation paths.
