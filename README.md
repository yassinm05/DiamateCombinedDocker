<div align="center">

# DiamateCombinedDocker

Two FastAPI ML services running in a single Docker container, sharing one Python 3.11 environment.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136.1-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.11.0-EE4C2C?logo=pytorch&logoColor=white)
![YOLO](https://img.shields.io/badge/Ultralytics-YOLO-111F68?logo=ultralytics&logoColor=white)
![Git LFS](https://img.shields.io/badge/Git_LFS-enabled-F64935?logo=git&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_API-powered-8E44AD?logo=google&logoColor=white)

</div>

| Service | Description | Port |
|---|---|---|
| **Project A** | UNet-based segmentation API | `5000` |
| **Project B** | YOLO / VLM detection API | `8000` |

---

## Prerequisites

Make sure the following are installed on your machine before anything else.

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)
- [Git](https://git-scm.com/downloads)
- [Git LFS](https://git-lfs.com/) — required for the UNet model file

To verify everything is installed:

```bash
docker --version
docker compose version
git --version
git lfs --version
```

---

## Cloning the Repository

Git LFS must be installed **before** you clone, otherwise the model file will not download correctly.

```bash
# 1. Install Git LFS (only needed once per machine)
git lfs install

# 2. Clone the repo — LFS files download automatically
git clone https://github.com/yassinm05/DiamateCombinedDocker.git

# 3. Enter the project folder
cd DiamateCombinedDocker
```

> If you already cloned without Git LFS installed, run `git lfs pull` inside the repo to fetch the model files.

---

## Project Structure

```
DiamateCombinedDocker/
├── projectA/                   # UNet segmentation service
│   └── src/
│       ├── main.py
│       └── model/
│           └── unet.pth        # stored in Git LFS
├── projectB/                   # YOLO / VLM detection service
│   ├── VLMMain.py
│   └── ...                     # YOLO model files
├── requirements.txt            # shared Python 3.11 environment
├── supervisord.conf            # process manager config
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Environment Variables Setup

Project B requires a Gemini API key before the container can start.

**1. Navigate to the projectB folder**

```bash
cd projectB
```

**2. Rename `.env.example` to `.env`**

```bash
# Linux / macOS
cp .env.example .env

# Windows
copy .env.example .env
```

**3. Open `.env` and add your Gemini API key**

```env
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual key from [Google AI Studio](https://aistudio.google.com/app/apikey).

> Never commit `.env` to Git. It is already listed in `.gitignore` to prevent this.

---

## Building and Running

### Start both services

```bash
docker compose up --build
```

- `--build` compiles the Docker image from scratch. Only needed the first time, or after changing `requirements.txt` or the `Dockerfile`.
- Subsequent runs can skip it: `docker compose up`

### Run in the background (detached mode)

```bash
docker compose up --build -d
```

### Stop the container

```bash
docker compose down
```

---

## Accessing the APIs

Once the container is running, both services are available at:

| Service | Swagger Docs | Base URL |
|---|---|---|
| Project A (UNet) | http://localhost:5000/docs | http://localhost:5000 |
| Project B (YOLO) | http://localhost:8000/docs | http://localhost:8000 |

> The first startup takes longer than usual because both ML models are loading into memory simultaneously. Wait until you see both services ready in the logs before making requests.

---

## Viewing Logs

### Live logs for both services

```bash
docker compose logs -f
```

### Logs for a specific service only

```bash
# Project A logs
docker exec -it <container_name> cat /var/log/supervisor/projectA.out.log

# Project B logs
docker exec -it <container_name> cat /var/log/supervisor/projectB.out.log

# Error logs
docker exec -it <container_name> cat /var/log/supervisor/projectA.err.log
docker exec -it <container_name> cat /var/log/supervisor/projectB.err.log
```

To find the container name:

```bash
docker ps
```

---

## Health Check

The container automatically checks that both services are responding every 30 seconds.

```bash
# Manually check health status
docker inspect --format='{{.State.Health.Status}}' <container_name>
```

Expected output: `healthy`

---

## Rebuilding After Code Changes

If you change source code only (not `requirements.txt`):

```bash
docker compose up --build
```

Docker caches the dependency installation layer, so this will be fast — it only re-copies your source files.

If you change `requirements.txt`, the full pip install will re-run (slower).

---

## Troubleshooting

**`unet.pth` is 134 bytes after cloning**
Git LFS was not installed before cloning. Run:
```bash
git lfs install
git lfs pull
```

**Port already in use**
Another process is using port 5000 or 8000. Find and stop it:
```bash
# On Linux/macOS
lsof -i :5000
lsof -i :8000

# On Windows
netstat -ano | findstr :5000
netstat -ano | findstr :8000
```

**One service starts but the other doesn't**
Check the individual error logs (see Viewing Logs above). A common cause is one model taking too long to load — the health check `start-period` is set to 60 seconds to account for this.

**Out of memory during build**
Torch and Torchvision are large. Make sure Docker Desktop has at least **6 GB of RAM** allocated:
`Docker Desktop → Settings → Resources → Memory`

---

## Git LFS Notes

The UNet model (`unet.pth`) and any `.pt` YOLO model files are tracked by Git LFS. GitHub provides 1 GB of free LFS storage. You can check your usage at:

`github.com/settings/billing → Git LFS Storage`

To see which files are in LFS:

```bash
git lfs ls-files
<<<<<<< HEAD
```
=======
```
>>>>>>> fbaab7620fdfa7a3f6431c113bca2bb549c50532
