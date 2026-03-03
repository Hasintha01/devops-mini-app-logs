# AWS Setup Guide - Step by Step

Follow this guide to set up your DevOps project on AWS from scratch.

---

## 🎯 What We're Setting Up

1. **S3 Bucket** - For log storage
2. **IAM Role** - For EC2 permissions to access CloudWatch/S3
3. **EC2 Instance** - To host your Flask app
4. **Security Groups** - To allow traffic to your app

**Total time**: ~20-30 minutes

---

## Step 1: Create S3 Bucket for Logs

### 1.1 Open S3 Console
- Go to AWS Console → Search "S3" → Click **S3**
- Click **Create bucket**

### 1.2 Configure Bucket
```
Bucket name: devops-mini-app-logs-YOURNAME
(Replace YOURNAME with your name or random numbers - bucket names must be globally unique)

AWS Region: us-east-1 (or your preferred region)

Block Public Access: ✅ Block all public access (keep this ON)

Bucket Versioning: Disabled (default is fine)

Tags: (optional)
  Key: Project
  Value: DevOps-Interview

Default encryption: Enable (Server-side encryption with Amazon S3 managed keys)
```

### 1.3 Create
- Click **Create bucket**
- ✅ **Success**: You should see your bucket listed

📝 **Note down**: Your bucket name (you'll need it later)

---

## Step 2: Create IAM Role for EC2

### 2.1 Open IAM Console
- Go to AWS Console → Search "IAM" → Click **IAM**
- In left menu → Click **Roles**
- Click **Create role**

### 2.2 Select Trusted Entity
```
Trusted entity type: AWS service
Use case: EC2
```
- Click **Next**

### 2.3 Add Permissions
Search and select these policies:
- ✅ `CloudWatchLogsFullAccess` (for logging)
- ✅ `AmazonS3FullAccess` (for S3 access)

> **Production Note**: In real production, use more restrictive policies

- Click **Next**

### 2.4 Name and Create
```
Role name: EC2-DevOps-App-Role

Description: IAM role for DevOps Flask app to access CloudWatch and S3
```
- Click **Create role**
- ✅ **Success**: Role created

---

## Step 3: Launch EC2 Instance

### 3.1 Open EC2 Console
- Go to AWS Console → Search "EC2" → Click **EC2**
- Click **Launch instance**

### 3.2 Configure Instance

**Name and tags**
```
Name: DevOps-Flask-App
```

**Application and OS Images (AMI)**
```
Quick Start: Ubuntu
Amazon Machine Image: Ubuntu Server 22.04 LTS (Free tier eligible)
Architecture: 64-bit (x86)
```

**Instance type**
```
Instance type: t2.micro (Free tier eligible)
```

**Key pair (login)**
```
Option 1: Create new key pair
  - Click "Create new key pair"
  - Key pair name: devops-app-key
  - Key pair type: RSA
  - Private key file format: .pem (for Mac/Linux) or .ppk (for Windows PuTTY)
  - Click "Create key pair"
  - 📥 File will download automatically - SAVE IT SECURELY!

Option 2: Use existing key pair if you have one
```

**Network settings**
- Click **Edit**

```
Auto-assign public IP: Enable

Firewall (security groups): Create security group

Security group name: devops-app-sg
Description: Security group for DevOps Flask app

Inbound Security Group Rules:
  Rule 1 (SSH):
    Type: SSH
    Protocol: TCP
    Port: 22
    Source type: My IP
    Description: SSH from my computer

  Rule 2 (Flask App):
    Type: Custom TCP
    Protocol: TCP
    Port: 5000
    Source type: Anywhere (0.0.0.0/0)
    Description: Flask app access

  Rule 3 (Optional - HTTP):
    Type: HTTP
    Protocol: TCP
    Port: 80
    Source type: Anywhere (0.0.0.0/0)
    Description: Future HTTP access
```

**Configure storage**
```
Size: 8 GiB (default is fine)
Root volume type: gp3 (default)
```

**Advanced details**
```
IAM instance profile: EC2-DevOps-App-Role (select the role you created in Step 2)
```

### 3.3 Launch
- Review all settings
- Click **Launch instance**
- ✅ **Success**: Instance is launching!

### 3.4 Wait and Get Details
- Click **View all instances**
- Wait until **Instance state** = "Running" (2-3 minutes)
- Click on your instance
- 📝 **Note down** these details:
  - **Public IPv4 address** (e.g., 52.23.45.67)
  - **Instance ID** (e.g., i-0abc123def456)

---

## Step 4: Connect to EC2 and Setup Application

### 4.1 Connect via SSH

**On Mac/Linux:**
```bash
# Go to folder where you downloaded the .pem file
cd ~/Downloads

# Set correct permissions
chmod 400 devops-app-key.pem

# Connect to EC2
ssh -i devops-app-key.pem ubuntu@YOUR-EC2-PUBLIC-IP
```

**On Windows (PowerShell):**
```powershell
# Go to folder where you downloaded the .pem file
cd ~\Downloads

# Connect to EC2
ssh -i devops-app-key.pem ubuntu@YOUR-EC2-PUBLIC-IP
```

Type "yes" when asked about fingerprint

✅ **Success**: You should see Ubuntu welcome message

### 4.2 Install Docker on EC2

```bash
# Update package list
sudo apt update

# Install Docker
sudo apt install docker.io -y

# Add ubuntu user to docker group
sudo usermod -aG docker ubuntu

# Verify Docker installed
docker --version

# Log out and log back in for group changes
exit
```

### 4.3 Reconnect and Verify
```bash
# SSH back in
ssh -i devops-app-key.pem ubuntu@YOUR-EC2-PUBLIC-IP

# Test Docker (should work without sudo now)
docker ps
```

### 4.4 Setup Application Directory

```bash
# Install Git
sudo apt install git -y

# Create app directory
mkdir -p ~/app
cd ~/app

# Clone your repository (replace with your repo URL)
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git .

# If you don't have a repo yet, you can create files manually:
# We'll push to GitHub in Step 5
```

### 4.5 Build and Run Docker Container

```bash
# Make sure you're in the app directory
cd ~/app

# Build Docker image
docker build -t devops-mini-app .

# Run container with S3 logging enabled
docker run -d -p 5000:5000 --name devops-mini-app \
  -e ENABLE_S3_LOGGING=true \
  -e S3_BUCKET_NAME=devops-mini-app-logs-YOURNAME \
  -e AWS_REGION=us-east-1 \
  devops-mini-app

# Check if container is running
docker ps

# Check logs
docker logs devops-mini-app
```

### 4.6 Test Your Application

Open browser and go to:
```
http://YOUR-EC2-PUBLIC-IP:5000
```

You should see: **"Hello from DevOps on AWS 🚀 (with S3 Logging)"**

Test other endpoints:
```
http://YOUR-EC2-PUBLIC-IP:5000/health
http://YOUR-EC2-PUBLIC-IP:5000/test-log
```

✅ **Success**: Your app is live on AWS!

---

## Step 5: Verify CloudWatch Logs

### 5.1 Check CloudWatch
- Go to AWS Console → Search "CloudWatch" → Click **CloudWatch**
- In left menu → Click **Logs** → **Log groups**
- Look for `/devops-mini-app`
- Click on it → Click on a log stream
- You should see your application logs!

### 5.2 Export Logs to S3 (Optional)
- Select `/devops-mini-app` log group
- Click **Actions** → **Export data to Amazon S3**
- Choose your S3 bucket: `devops-mini-app-logs-YOURNAME`
- Select time range → Click **Export**
- Check your S3 bucket after a few minutes

---

## Step 6: Setup GitHub for CI/CD

### 6.1 Push Your Code to GitHub

**If you don't have a repo yet:**

```bash
# On your local computer (not EC2), in your project folder
cd "C:\Users\Hasin\Desktop\DevOps Interview"

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit with S3 logging"

# Create a new repo on GitHub (via web browser):
# Go to github.com → Click "+" → New repository
# Name: devops-flask-app
# Public/Private: Your choice
# DO NOT initialize with README
# Click "Create repository"

# Back in terminal, add remote and push
git remote add origin https://github.com/YOUR-USERNAME/devops-flask-app.git
git branch -M main
git push -u origin main
```

### 6.2 Add GitHub Secrets

Go to your GitHub repository:
1. Click **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**

**Secret 1: EC2_HOST**
```
Name: EC2_HOST
Secret: YOUR-EC2-PUBLIC-IP (e.g., 52.23.45.67)
```
Click **Add secret**

**Secret 2: EC2_KEY**
```
Name: EC2_KEY
Secret: [Paste entire content of your .pem file]
```
Open your `.pem` file in notepad, copy EVERYTHING including:
```
-----BEGIN RSA PRIVATE KEY-----
...all the content...
-----END RSA PRIVATE KEY-----
```
Click **Add secret**

✅ **Secrets configured!**

### 6.3 Test CI/CD

```bash
# On your local computer, make a small change
# Edit app.py - change the welcome message

# Commit and push
git add .
git commit -m "Test CI/CD pipeline"
git push origin main

# Go to GitHub → Your repo → Actions tab
# Watch the workflow run!
```

After it completes, refresh your browser at `http://YOUR-EC2-PUBLIC-IP:5000`

---

## 📋 Quick Reference

### Your AWS Resources

| Resource | Name/ID | Notes |
|----------|---------|-------|
| S3 Bucket | `devops-mini-app-logs-YOURNAME` | For log storage |
| IAM Role | `EC2-DevOps-App-Role` | CloudWatch + S3 permissions |
| EC2 Instance | `DevOps-Flask-App` | t2.micro Ubuntu |
| Security Group | `devops-app-sg` | Ports 22, 5000, 80 |
| Key Pair | `devops-app-key.pem` | Keep secure! |

### Important URLs
- **App**: `http://YOUR-EC2-PUBLIC-IP:5000`
- **Health**: `http://YOUR-EC2-PUBLIC-IP:5000/health`
- **Test Logs**: `http://YOUR-EC2-PUBLIC-IP:5000/test-log`

### Useful Commands

**SSH to EC2:**
```bash
ssh -i devops-app-key.pem ubuntu@YOUR-EC2-PUBLIC-IP
```

**On EC2 - Docker Commands:**
```bash
# View running containers
docker ps

# View logs
docker logs devops-mini-app

# Restart container
docker restart devops-mini-app

# Stop and remove
docker stop devops-mini-app
docker rm devops-mini-app

# Rebuild and run
docker build -t devops-mini-app .
docker run -d -p 5000:5000 --name devops-mini-app \
  -e ENABLE_S3_LOGGING=true \
  -e S3_BUCKET_NAME=devops-mini-app-logs-YOURNAME \
  -e AWS_REGION=us-east-1 \
  devops-mini-app
```

---

## 🛑 Common Issues & Solutions

### Can't SSH to EC2
- ✅ Check security group allows SSH (port 22) from your IP
- ✅ Verify you're using correct key file
- ✅ Key permissions: `chmod 400 devops-app-key.pem`
- ✅ Use correct username: `ubuntu`

### Can't access app on port 5000
- ✅ Check security group allows inbound TCP port 5000
- ✅ Verify container is running: `docker ps`
- ✅ Check EC2 instance is running in AWS console

### CloudWatch logs not appearing
- ✅ Verify IAM role is attached to EC2 instance
- ✅ Check `ENABLE_S3_LOGGING=true` environment variable
- ✅ View container logs: `docker logs devops-mini-app`

### GitHub Actions failing
- ✅ Verify both secrets (EC2_HOST and EC2_KEY) are set correctly
- ✅ Ensure app directory exists on EC2: `/home/ubuntu/app`
- ✅ Check GitHub Actions logs for specific error

---

## 💰 AWS Cost Information

**Free Tier (First 12 months):**
- ✅ EC2 t2.micro: 750 hours/month (1 instance 24/7)
- ✅ S3: 5GB storage, 20,000 GET requests, 2,000 PUT requests
- ✅ CloudWatch Logs: 5GB ingestion, 5GB storage

**After Free Tier:**
- EC2 t2.micro: ~$8-10/month
- S3: ~$0.023 per GB/month
- CloudWatch: First 5GB free, then ~$0.50/GB

**To minimize costs:**
- Stop EC2 instance when not using (EC2 console → Instance → Stop)
- Delete old logs from S3
- Use lifecycle policies to move old logs to cheaper storage

---

## 🎉 You're Done!

Your complete DevOps pipeline is now running on AWS!

**What you've built:**
- ✅ Containerized Flask application
- ✅ Running on AWS EC2
- ✅ Integrated with S3 and CloudWatch for logging
- ✅ IAM role for secure permissions
- ✅ CI/CD pipeline with GitHub Actions

**Next Steps:**
- Test making changes and watch auto-deployment
- Monitor logs in CloudWatch
- Experiment with exporting logs to S3
- Add monitoring and alerts

---

Need help? Check the main [README.md](README.md) for troubleshooting and interview prep!
