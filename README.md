# Camera Timelapse Collector

A Docker-based timelapse camera system that automatically captures hourly frames from multiple IP cameras and provides a web interface for viewing the collected images.

### Currently tested and working with HIKVISION cameras.

</br>

## Features

- **Automated Frame Collection**: Captures frames from multiple cameras every hour
- **Web Interface**: Browse and view collected frames through a user-friendly filebrowser
- **Basic Authentication**: Secure access to the web interface with password protection
- **Multi-Camera Support**: Configure up to 20 cameras simultaneously
- **Organized Storage**: Frames are automatically organized by camera IP and timestamp
- **Docker-Based**: Easy deployment with Docker Compose

</br>

## Architecture

The system consists of three main components:

1. **Collector**: Python service that fetches frames from cameras on an hourly basis
2. **File Browser**: Web interface for browsing and viewing saved frames
3. **Endpoint**: Caddy reverse proxy with basic authentication

</br>

## Prerequisites

- Docker and Docker Compose installed
- Network access to IP cameras
- Cameras must support HTTP snapshot API

</br>

## Quick Start

1. Clone this repository:
   ```bash
   git clone https://github.com/kaunofakultetas/timelapse-collector.git
   cd timelapse-collector
   ```

2. Copy the sample configuration:
   ```bash
   cp docker-compose.yml.sample docker-compose.yml
   ```

3. Edit `docker-compose.yml` and configure:
   - Camera IPs and credentials in the `timelapse-collector` environment section
   - Basic auth username and password hash in the `timelapse-endpoint` environment section

4. Generate a password hash for basic authentication:
   ```bash
   docker run --rm caddy:2.10.2-alpine caddy hash-password --plaintext 'YourPassword'
   ```
   
   **Important**: When adding the hash to `docker-compose.yml`, escape all `$` symbols by doubling them (`$$`):
   ```yaml
   - BASIC_AUTH_HASH=$$2a$$12$$yourHashHere
   ```

5. Run the deployment script:
   ```bash
   ./runUpdateThisStack.sh
   ```

6. Access the web interface at port 80.

</br>

## Configuration

### Camera Configuration

Configure cameras in the `timelapse-collector` service environment variables:

```yaml
environment:
  # Camera 1
  - CAMERA_TYPE_0=HIKVISION
  - CAMERA_IP_0=192.168.1.100
  - CAMERA_USERPASS_0=admin:password
  
  # Camera 2
  - CAMERA_TYPE_1=HIKVISION
  - CAMERA_IP_1=192.168.1.101
  - CAMERA_USERPASS_1=admin:password
```

- Use sequential numbering starting from 0 (e.g., `_0`, `_1`, `_2`, etc.)
- Maximum 20 cameras supported
- Currently only HIKVISION camera type is supported

</br>

### Basic Authentication

Configure access credentials in the `timelapse-endpoint` service:

```yaml
environment:
  # username:password
  - BASIC_AUTH_USER=admin
  - BASIC_AUTH_HASH=$$2a$$12$$YourBcryptHashHere
```

Generate new password hashes using:
```bash
docker run --rm caddy:2.10.2-alpine caddy hash-password --plaintext 'YourPassword'
```

</br>


## How It Works

1. **Frame Collection**: The collector service runs continuously and checks every second if a new hour has begun
2. **Hourly Capture**: At the start of each hour, it attempts to fetch a snapshot from each configured camera
3. **Storage**: Frames are saved in `SAVED_FRAMES/<camera-ip>/YYYY-MM-DD HHMM.jpg` format
4. **Web Access**: The file browser serves these frames through a web interface protected by Caddy's basic authentication

</br>

## File Structure

```
.
├── collector/
│   ├── Dockerfile
│   └── main.py              # Camera frame collection logic
├── endpoint/
│   └── Caddyfile           # Reverse proxy configuration
├── filebrowser/
│   ├── Dockerfile
│   ├── filebrowser.json
│   └── branding/           # Custom branding files
├── SAVED_FRAMES/           # Collected frames (created automatically)
├── docker-compose.yml      # Main configuration (not in repo)
├── docker-compose.yml.sample  # Sample configuration
└── runUpdateThisStack.sh   # Deployment script
```

</br>

## Maintenance

### View Logs

```bash
# All services
sudo docker-compose logs -f

# Specific service
sudo docker-compose logs -f timelapse-collector
sudo docker-compose logs -f timelapse-filebrowser
sudo docker-compose logs -f timelapse-endpoint
```

</br>

### Restart Services

```bash
./runUpdateThisStack.sh
```

</br>

### Stop Services

```bash
sudo docker-compose down
```

</br>

## Troubleshooting

### Camera Connection Issues

- Verify camera IP addresses are correct
- Check network connectivity to cameras
- Verify camera credentials
- Ensure cameras support HTTP snapshot API at `/Streaming/channels/101/picture`

### Authentication Not Working

- Verify the password hash is correctly escaped with `$$` in docker-compose.yml
- Regenerate the hash if needed
- Check Caddy logs: `docker-compose logs timelapse-endpoint`

### Missing Frames

- Check collector logs for errors: `docker-compose logs timelapse-collector`
- Verify cameras are accessible from the collector container
- Ensure sufficient disk space in `SAVED_FRAMES` directory
