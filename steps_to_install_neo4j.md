Here's a step-by-step guide to install and configure **Neo4j** on Ubuntu for your temporal graph setup, including environment variables (`NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`):

---

### **1. Install Neo4j on Ubuntu**
#### **Prerequisites**
- Ubuntu 20.04/22.04 LTS
- Java 11 (Neo4j 5.x requires Java 11+)

```bash
# Install OpenJDK 11
sudo apt update
sudo apt install openjdk-11-jdk -y

# Verify Java version
java -version
```

#### **Install Neo4j**
```bash
# Add Neo4j repository
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list

# Install Neo4j Community Edition
sudo apt update
sudo apt install neo4j -y

# Start Neo4j service
sudo systemctl enable neo4j.service
sudo systemctl start neo4j.service
```

---

### **2. Configure Neo4j**
#### **Allow Remote Connections**
By default, Neo4j only listens to `localhost`. Modify the config to allow external connections (if needed):
```bash
sudo nano /etc/neo4j/neo4j.conf
```

Uncomment/modify these lines:
```ini
# Listen on all interfaces
server.default_listen_address=0.0.0.0

# Bolt connector (for Python/Cypher)
server.bolt.listen_address=0.0.0.0:7687

# HTTP/HTTPS connectors (for browser access)
server.http.listen_address=0.0.0.0:7474
server.https.listen_address=0.0.0.0:7473
```

Restart Neo4j:
```bash
sudo systemctl restart neo4j.service
```

#### **Set Password**
The default credentials are `neo4j`/`neo4j`. Change the password:
```bash
cypher-shell -u neo4j -p neo4j
# Enter new password when prompted
```

---

### **3. Verify Installation**
Access the Neo4j Browser at `http://localhost:7474` (replace `localhost` with your server IP if remote).  
Log in with:
- **Username**: `neo4j`
- **Password**: [your new password]

---

### **4. Set Environment Variables**
Add these to your shell profile (e.g., `~/.bashrc`, `~/.zshrc`) or project `.env` file:
```bash
# Neo4j Credentials
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your_password_here"
```

Reload the profile:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

---

### **5. Test Connection (Python Example)**
Install the Neo4j Python driver:
```bash
pip install neo4j
```

Test connectivity:
```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    os.environ["NEO4J_URI"],
    auth=(
        os.environ["NEO4J_USER"],
        os.environ["NEO4J_PASSWORD"]
    )
)

with driver.session() as session:
    result = session.run("RETURN 'Neo4j is working!' AS message")
    print(result.single()["message"])  # Output: "Neo4j is working!"
```

---

### **6. Ingest FOMC/Beige Book Data**
Use the Python driver to create nodes/edges from your parsed data. Example:
```python
def create_fomc_node(tx, meeting_date, rate_change):
    tx.run(
        "CREATE (n:FOMC {date: $date, rate_change: $rate_change})",
        date=meeting_date,
        rate_change=rate_change
    )

with driver.session() as session:
    session.execute_write(
        create_fomc_node,
        meeting_date="2024-11-07",
        rate_change="-0.25%"
    )
```

---

### **Security Notes**
- Use a strong password for Neo4j (not `neo4j`).
- For production, enable SSL in `neo4j.conf` and restrict IP access via firewall.
- Avoid exposing ports `7474`, `7687`, or `7473` publicly without authentication.

---

### **Troubleshooting**
- **Service not starting**: Check logs at `/var/log/neo4j/neo4j.log`.
- **Connection issues**: Verify Neo4j is running: `sudo systemctl status neo4j.service`.
- **Firewall**: Allow ports `7474` (HTTP), `7687` (Bolt), and `7473` (HTTPS).

Once Neo4j is running, you can build your temporal graph with FOMC/Beige Book nodes and relationships! 🚀