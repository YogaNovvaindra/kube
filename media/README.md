# Media Stack

The media stack provides automated media management, downloading, and streaming capabilities.

## Components

- **[Plex](file:///home/yoga/Documents/kube/media/player.yml)**: High-performance media server with transcoding support.
- **[Arr Suite](file:///home/yoga/Documents/kube/media/arr.yml)**: Automation tools for movies and TV shows (Radarr, Sonarr, Bazarr).
- **[Download Clients](file:///home/yoga/Documents/kube/media/download.yml)**: Transmission (torrents) and Aria2 (general downloads).
- **[qBittorrent + Qui](file:///home/yoga/Documents/kube/media/qbittorrent.yml)**: qBittorrent torrent client with Qui multi-instance Web UI.
- **[Overseerr](file:///home/yoga/Documents/kube/media/arr.yml)**: Request management for library additions.
- **[Tautulli](file:///home/yoga/Documents/kube/media/player.yml)**: Monitoring and analytics for Plex.

## Automation Workflow

The Arr suite monitors for new releases and sends download commands to Transmission/Aria2/qBittorrent. Once complete, files are automatically moved to the Plex library.
