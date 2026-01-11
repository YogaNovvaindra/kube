# Media Stack

The media stack provides automated media management, downloading, and streaming capabilities.

## Components

- **[Plex](media/player.yml)**: High-performance media server with transcoding support.
- **[Arr Suite](media/arr.yml)**: Automation tools for movies and TV shows (Radarr, Sonarr, Bazarr).
- **[Download Clients](media/download.yml)**: Transmission (torrents) and Aria2 (general downloads).
- **[qBittorrent + Qui](media/qbittorrent.yml)**: qBittorrent torrent client with Qui multi-instance Web UI.
- **[Overseerr](media/arr.yml)**: Request management for library additions.
- **[Tautulli](media/player.yml)**: Monitoring and analytics for Plex.

## Automation Workflow

The Arr suite monitors for new releases and sends download commands to Transmission/Aria2/qBittorrent. Once complete, files are automatically moved to the Plex library.
