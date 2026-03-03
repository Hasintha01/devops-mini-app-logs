# DevOps Mini Project - AWS Flask Application

A production-ready DevOps project demonstrating containerization, cloud deployment, CI/CD automation, and AWS service integration.

[![Deploy to EC2](https://github.com/Hasintha01/devops-mini-app-logs/actions/workflows/deploy.yml/badge.svg)](https://github.com/Hasintha01/devops-mini-app-logs/actions/workflows/deploy.yml)

## Live Demo

**Application URL:** http://51.21.149.34:5000

### Available Endpoints
- `/` - Welcome page
- `/health` - Health check with S3 logging status
- `/users` - Sample user data API
- `/test-log` - Generate test logs for CloudWatch

---

## Project Overview

This project implements a complete DevOps workflow featuring:

### Infrastructure & Cloud
- **AWS EC2** - Application hosting on Ubuntu 22.04
- **AWS S3** - Log storage and archival
- **AWS CloudWatch Logs** - Centralized logging
- **AWS IAM** - Role-based access control
- **Security Groups** - Network access management

### Development & Deployment
- **Docker** - Containerized Flask application
- **GitHub Actions** - Automated CI/CD pipeline
- **Git** - Version control and collaboration

### Tech Stack
- **Python 3.10** - Application runtime
- **Flask** - Web framework
- **Boto3** - AWS SDK for Python
- **Watchtower** - CloudWatch log handler

---

## Architecture

```
Developer → GitHub → GitHub Actions → EC2 (Docker) → CloudWatch Logs → S3
                                      ↓
                                   Internet Users
```

**CI/CD Flow:**
1. Code pushed to `master` branch
2. GitHub Actions triggers workflow
3. SSH into EC2 instance
4. Pull latest code from repository
5. Build Docker image
6. Deploy new container (zero-downtime)
7. Application logs sent to CloudWatch
8. Logs exported to S3 for long-term storage

---

## Technologies & Tools

| Category | Technology |
|----------|-----------|
| **Cloud Platform** | AWS (EC2, S3, CloudWatch, IAM) |
| **Containerization** | Docker |
| **CI/CD** | GitHub Actions |
| **Language** | Python 3.10 |
| **Framework** | Flask 3.0.0 |
| **Version Control** | Git & GitHub |
| **Logging** | CloudWatch Logs, Watchtower |

---

## Project Structure

```
devops-mini-app-logs/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD pipeline configuration
├── app.py                       # Flask application
├── Dockerfile                  # Container configuration
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git exclusions
├── .dockerignore              # Docker build exclusions
└── README.md                   # This file
```

---

## Quick Start

### Prerequisites
- AWS Account with EC2 access
- Docker installed
- Python 3.10+
- Git

### Local Development

```bash
# Clone repository
git clone https://github.com/Hasintha01/devops-mini-app-logs.git
cd devops-mini-app-logs

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

Visit: http://localhost:5000

### Docker Deployment

```bash
# Build image
docker build -t devops-mini-app .

# Run container
docker run -d -p 5000:5000 \
  -e ENABLE_S3_LOGGING=true \
  -e S3_BUCKET_NAME=your-bucket-name \
  -e AWS_REGION=eu-north-1 \
  --name devops-app \
  devops-mini-app
```

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_S3_LOGGING` | Enable CloudWatch/S3 logging | `false` |
| `S3_BUCKET_NAME` | S3 bucket for log exports | `devops-mini-app-logs` |
| `AWS_REGION` | AWS region | `us-east-1` |

### GitHub Secrets (for CI/CD)

| Secret | Description |
|--------|-------------|
| `EC2_HOST` | EC2 instance public IP |
| `EC2_KEY` | SSH private key (.pem format) |

---

## CI/CD Pipeline

Automated deployment triggered on every push to `master` branch:

1. **Checkout** - Clone repository
2. **Build** - Create Docker image
3. **Deploy** - SSH to EC2 and update container
4. **Verify** - Application running with latest changes

**Deployment Time:** ~30-40 seconds

---

## Monitoring & Logging

### CloudWatch Logs
- Log Group: `/devops-mini-app`
- Real-time application logs
- Searchable and filterable

### S3 Storage
- Long-term log archival
- Cost-effective storage
- Export from CloudWatch on-demand

---

## Security Features

- IAM role-based permissions (no hardcoded credentials)
- Security groups for network isolation
- GitHub Secrets for sensitive data
- Docker containerization for process isolation

---

## Key Features

- **Zero-downtime deployments** - Old container stopped only after new one starts  
- **Automatic rollback** - Failed deployments don't affect running application  
- **Centralized logging** - All logs aggregated in CloudWatch  
- **Infrastructure as Code** - Dockerfile and workflow YAML  
- **Version control** - Full Git history  
- **Health monitoring** - Health check endpoint  

---

## DevOps Best Practices Demonstrated

- **Containerization** - Consistent environments across dev/prod
- **CI/CD Automation** - Fast, reliable deployments
- **Infrastructure as Code** - Reproducible infrastructure
- **Monitoring & Logging** - Observability and debugging
- **Security** - Least privilege access, secrets management
- **Version Control** - Change tracking and collaboration

---

## Learning Outcomes

This project demonstrates practical knowledge of:
- AWS cloud services (EC2, S3, IAM, CloudWatch)
- Docker containerization
- CI/CD pipeline implementation
- GitHub Actions workflows
- Linux server administration
- Network security (Security Groups)
- Application logging and monitoring
- Git version control

---

## Support

For detailed setup instructions, see [GUIDE.md](GUIDE.md)

---

## License

This is a learning/demonstration project. Feel free to use and modify.

---

## Author

**Hasintha**  
GitHub: [@Hasintha01](https://github.com/Hasintha01)

---

**Built for DevOps Learning**
