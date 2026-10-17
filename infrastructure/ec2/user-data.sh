
#!/bin/bash
set -euo pipefail

exec > >(tee /var/log/coditude-user-data.log | logger -t user-data -s 2>/dev/console) 2>&1

echo "Installing application dependencies..."

dnf update -y
dnf install -y git python3 python3-pip nginx

# Install Node.js 22
dnf install -y nodejs22 nodejs22-npm

# Create application user
id coditude &>/dev/null || useradd --system --create-home coditude

mkdir -p /opt/coditude
chown coditude:coditude /opt/coditude

# Download application source
sudo -u coditude git clone \
  https://github.com/dishadkamble-design/coditude-aws-devops-assessment.git \
  /opt/coditude/app

# Set up Python backend
cd /opt/coditude/app/backend

python3 -m venv /opt/coditude/venv
/opt/coditude/venv/bin/pip install -r requirements.txt

# Configure backend service
cat > /etc/systemd/system/coditude-backend.service <<'EOF'
[Unit]
Description=Coditude FastAPI Backend
After=network-online.target
Wants=network-online.target

[Service]
User=coditude
WorkingDirectory=/opt/coditude/app/backend
EnvironmentFile=/etc/coditude/backend.env
ExecStart=/opt/coditude/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Set up Next.js frontend
cd /opt/coditude/app/frontend

npm install
npm run build

cat > /etc/systemd/system/coditude-frontend.service <<'EOF'
[Unit]
Description=Coditude Next.js Frontend
After=network-online.target
Wants=network-online.target

[Service]
User=coditude
WorkingDirectory=/opt/coditude/app/frontend
Environment=NODE_ENV=production
ExecStart=/usr/bin/npm run start -- --hostname 0.0.0.0 --port 3000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload

echo "EC2 application setup completed."
