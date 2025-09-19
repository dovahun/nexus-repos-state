# Nexus state repos

# go v1.22

## local build

```
go build -o nexus_repos_state main.go
```

## Example structure
    nexus-repost-state/
    ├── .bin/
    │   └── nexus_repos_state
    ├── src/
    │   ├── readFiles.go
    │   └── workWithApi.go
    │── configs/
    │   └── repositories/
    │        │── maven/
    │        │    │── a_proxy/
    │        │    │    └── foo-maven-proxy.json
    │        │    └── z_proxy/
    │        │        └── foo-group.json
    │        └── npm/
    │            └── a_proxy/
    │                └── foo-npm-proxy.json
    ├── Dockerfile
    └── README.md

## FLAGS

| FLAG      |                    description                    |                example                 |
|:----------|:-------------------------------------------------:|:--------------------------------------:|
| -url      | Set nexus url with base api path and version /v1/ | http://127.0.0.1:8081/service/rest/v1/ |
| -username |           Set nexus user for basic auth           |                 admin                  |
| -password |       Set password from user for basic auth       |                 admin                  |
| -configs  |       Set path to dir with all json configs       |               ./configs/               |
| -help     |                       help                        |                   -                    |

## Recomendation: try to name files using alphabet prefix between group and repos. Repos have to create first then groups.

