# DevOps Mini Project - Flask App on AWS

A 3-day hands-on DevOps project demonstrating containerization, cloud deployment, CI/CD automation, and AWS service integration (EC2, S3, CloudWatch, IAM).

## 🚀 What You'll Build

- **Day 1**: Dockerize a Flask application
- **Day 2**: Deploy to AWS EC2 with S3 logging integration
- **Day 3**: Automate deployment with GitHub Actions
- **Bonus**: Implement CloudWatch Logs with S3 export for log management

## 📋 Prerequisites

- Python 3.10+
- Docker Desktop installed
- AWS Account
- GitHub Account
- Basic knowledge of Git, Docker, and AWS

---

## ✅ Day 1 - Build & Dockerize App

### Step 1: Create Flask App

The app is already created in `app.py`:
- Main route `/` - Returns welcome message
- Health check route `/health` - Returns application status and S3 logging status
- Test logging route `/test-log` - Generates sample logs for testing S3 integration

### Step 2: Install Dependencies Locally (Optional)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

Visit: http://localhost:5000

### Step 3: Build Docker Image

```bash
docker build -t devops-mini-app .
```

### Step 4: Run Docker Container

```bash
docker run -p 5000:5000 devops-mini-app
```

Visit: http://localhost:5000

**✅ Day 1 Success**: If you see "Hello from DevOps on AWS 🚀", you're ready for Day 2!

---

## ✅ Day 2 - Deploy to AWS EC2

### Step 0: Create S3 Bucket & Setup IAM (Optional but Recommended)

#### Create S3 Bucket for Logs

1. Go to AWS Console → S3 → Create bucket
2. **Bucket name**: `devops-mini-app-logs` (must be globally unique, add your name/number if needed)
3. **Region**: Choose same region as your EC2 (e.g., `us-east-1`)
4. **Settings**: Keep defaults (Block all public access = ON)
5. Click **Create bucket**

#### Create IAM Role for EC2

Your EC2 instance needs permissions to write logs to CloudWatch (which can be exported to S3).

1. Go to AWS Console → IAM → Roles → Create role
2. **Trusted entity type**: AWS service
3. **Use case**: EC2 → Next
4. **Permissions**: Attach these policies:
   - `CloudWatchLogsFullAccess` (for CloudWatch Logs)
   - `AmazonS3FullAccess` (for S3 - or create custom policy for specific bucket)
5. **Role name**: `EC2-DevOps-App-Role`
6. Click **Create role**

#### Attach IAM Role to EC2 (After instance creation)

1. Go to EC2 Dashboard → Select your instance
2. Actions → Security → Modify IAM role
3. Select `EC2-DevOps-App-Role`
4. Click **Update IAM role**

> **Note**: If you skip this step, the app will run without S3 logging (logs will only appear in console)

### Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2 → Launch Instance
2. Choose **Ubuntu Server 22.04 LTS**
3. Instance type: **t2.micro** (Free tier eligible)
4. Create or select a key pair (download `.pem` file)
5. **Security Group Settings**:
   - SSH (Port 22) - Your IP only
   - Custom TCP (Port 5000) - 0.0.0.0/0 (for testing)
   - HTTP (Port 80) - 0.0.0.0/0 (optional)
6. Launch instance

### Step 2: SSH Into EC2

```bash
# Change key permissions (Mac/Linux)
chmod 400 your-key.pem

# SSH into instance
ssh -i your-key.pem ubuntu@YOUR-EC2-PUBLIC-IP
```

**On Windows**: Use PuTTY or WSL, or use PowerShell directly.

### Step 3: Install Docker on EC2

```bash
# Update packages
sudo apt update

# Install Docker
sudo apt install docker.io -y

# Add user to docker group
sudo usermod -aG docker ubuntu

# IMPORTANT: Logout and login again for group changes to take effect
exit
```

SSH back in:
```bash
ssh -i your-key.pem ubuntu@YOUR-EC2-PUBLIC-IP
```

Verify Docker:
```bash
docker --version
```

### Step 4: Clone Repository on EC2

```bash
# Install git if not present
sudo apt install git -y

# Create app directory
mkdir -p /home/ubuntu/app
cd /home/ubuntu/app

# Clone your repository
git clone YOUR-GITHUB-REPO-URL .
```

### Step 5: Build and Run on EC2

```bash
# Build Docker image
docker build -t devops-mini-app .

# Run container WITHOUT S3 logging (simple mode)
docker run -d -p 5000:5000 --name devops-mini-app devops-mini-app

# OR Run container WITH S3 logging enabled (recommended)
docker run -d -p 5000:5000 --name devops-mini-app \
  -e ENABLE_S3_LOGGING=true \
  -e S3_BUCKET_NAME=devops-mini-app-logs \
  -e AWS_REGION=us-east-1 \
  devops-mini-app
```

**Note**: S3 logging requires IAM role attached to EC2 (see Step 0)

### Step 6: Access Your App

Open browser: `http://YOUR-EC2-PUBLIC-IP:5000`

**Test the endpoints**:
- `/` - Main page
- `/health` - Health check (shows S3 logging status)
- `/test-log` - Generate test logs (check CloudWatch Logs after)

**✅ Day 2 Success**: Your app is now live on the cloud with AWS service integration! 🎉

### Step 7: Verify S3 Logging (Optional)

1. Go to AWS Console → CloudWatch → Log groups
2. Find `/devops-mini-app` log group
3. Click on log stream to view logs
4. To export to S3:
   - Select log group → Actions → Export data to S3
   - Choose your S3 bucket
   - Set time range → Export

### Useful Docker Commands on EC2

```bash
# Check running containers
docker ps

# View logs
docker logs devops-mini-app

# Stop container
docker stop devops-mini-app

# Remove container
docker rm devops-mini-app

# Restart container
docker restart devops-mini-app
```

---

## ✅ Day 3 - Add CI/CD with GitHub Actions

### Step 1: Understand the Workflow

The `.github/workflows/deploy.yml` file automates:
1. Code checkout when you push to `main`
2. Docker image build
3. SSH into EC2
4. Pull latest code
5. Rebuild and restart container

### Step 2: Add GitHub Secrets

Go to your GitHub repository:
1. Settings → Secrets and variables → Actions → New repository secret

Add these secrets:

**EC2_HOST**
- Value: Your EC2 public IP address (e.g., `52.23.45.67`)

**EC2_KEY**
- Value: Content of your `.pem` private key file
- Open the `.pem` file in a text editor and copy the entire content including:
  ```
  -----BEGIN RSA PRIVATE KEY-----
  ...
  -----END RSA PRIVATE KEY-----
  ```

### Step 3: Test the CI/CD Pipeline

1. Make a change to `app.py`:
   ```python
   return "Hello from DevOps on AWS 🚀 - Auto-deployed!"
   ```

2. Commit and push:
   ```bash
   git add .
   git commit -m "Test CI/CD pipeline"
   git push origin main
   ```

3. Go to GitHub → Your Repo → Actions tab
4. Watch the workflow run
5. Once complete, visit `http://YOUR-EC2-PUBLIC-IP:5000`

**✅ Day 3 Success**: Automatic deployment is working! This is real DevOps! 🎉

---

## 🎯 Interview Talking Points

### What This Project Demonstrates

1. **Containerization**: Dockerizing applications for consistency across environments
2. **Cloud Deployment**: Deploying to AWS EC2, understanding security groups and SSH
3. **AWS Services Integration**: Using EC2, S3, CloudWatch Logs, and IAM roles
4. **CI/CD**: Automating deployments with GitHub Actions
5. **Infrastructure as Code**: Dockerfile and workflow YAML files
6. **Version Control**: Using Git for code management
7. **Logging & Monitoring**: Implementing centralized logging with CloudWatch

### Architecture Overview

```
Developer → Git Push → GitHub → GitHub Actions → SSH → EC2 (IAM Role) → Docker Container
                                                              ↓
                                                         CloudWatch Logs → S3 Bucket
```

### Key Skills Shown

- Docker fundamentals (build, run, manage containers)
- AWS EC2 (compute, security groups, SSH access)
- AWS S3 (object storage for logs and data)
- AWS CloudWatch (centralized logging and monitoring)
- AWS IAM (roles and permissions management)
- GitHub Actions (workflow automation)
- Linux administration (package management, user permissions)
- Networking basics (ports, security)

### Common Interview Questions You Can Answer

**Q: Why use Docker?**
- Consistency across development and production
- Isolated environments
- Easy scaling and deployment
- Version control for infrastructure

**Q: Explain your CI/CD pipeline**
- "When I push to main, GitHub Actions triggers a workflow that builds my Docker image and SSH into EC2 to deploy the latest version automatically."

**Q: How do you handle secrets?**
- "I use GitHub Secrets for sensitive data like SSH keys and EC2 IP addresses, never hardcoding them in the repository."

**Q: How do you handle logging in a distributed system?**
- "I use CloudWatch Logs for centralized logging, which can be exported to S3 for long-term storage and analysis. This provides better observability and debugging capabilities."

**Q: Explain IAM roles vs IAM users**
- "IAM roles are assumed by AWS services like EC2, providing temporary credentials. IAM users are for people/applications with permanent credentials. Roles are more secure for EC2 instances."

**Q: Why use S3 for logs?**
- "S3 provides durable, cost-effective long-term storage for logs. It's cheaper than CloudWatch for retention, supports lifecycle policies, and integrates with analytics tools like Athena."

**Q: What would you improve in production?**
- Use a production WSGI server like Gunicorn
- Implement nginx as a reverse proxy
- Use container registry (Docker Hub or AWS ECR)
- Enhance monitoring with CloudWatch metrics and alarms
- Implement structured logging (JSON format) for better parsing
- Add log aggregation and analysis tools (ELK stack, AWS Athena)
- Use S3 lifecycle policies to archive old logs to Glacier
- Implement blue-green or rolling deployments
- Use HTTPS with SSL certificates
- Move to orchestration (ECS, Kubernetes)
- Implement proper IAM policies with least privilege principle

---

## 🔧 Troubleshooting

### Docker build fails
```bash
# Check Docker is running
docker ps

# Remove old images
docker image prune -a
```

### Can't SSH into EC2
- Check security group allows SSH (port 22) from your IP
- Verify key permissions: `chmod 400 your-key.pem`
- Ensure you're using the correct username (`ubuntu` for Ubuntu AMI)

### Container doesn't start
```bash
# Check logs
docker logs devops-mini-app

# Try running in foreground to see errors
docker run -p 5000:5000 devops-mini-app
```

### GitHub Actions fails
- Verify all secrets are correctly set
- Check EC2 is running and accessible
- Ensure app directory exists on EC2
- Review workflow logs in GitHub Actions tab

### Port 5000 not accessible
- Check EC2 security group allows inbound traffic on port 5000
- Verify container is running: `docker ps`
- Check if app is listening: `curl localhost:5000` from EC2

---

## 📚 Next Steps (Optional Day 4)

1. **Add Nginx Reverse Proxy**
   - Route port 80 to your app
   - Add SSL with Let's Encrypt

2. **Use Docker Hub**
   - Push images to registry
   - Pull from registry in deployment

3. **Environment Variables**
   - Add `.env` support
   - Manage different configs for dev/prod

4. **Add Tests**
   - Unit tests with pytest
   - Run tests in CI pipeline before deploy

5. **Monitoring**
   - Add CloudWatch for metrics
   - Implement health check endpoints
   - Set up alarms

---

## 📝 Project Structure

```
DevOps Interview/
├── .github/
│   └── workflows/
│       └── deploy.yml      # CI/CD pipeline
├── app.py                   # Flask application
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── .dockerignore           # Docker build exclusions
├── .gitignore              # Git exclusions
└── README.md               # This file
```

---

## 🎓 Learning Resources

- [Docker Documentation](https://docs.docker.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [AWS EC2 Guide](https://docs.aws.amazon.com/ec2/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

---

## 📄 License

This is a learning project - feel free to use and modify as needed.

---

**Good luck with your DevOps interview! 🚀**
