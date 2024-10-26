# sync_follows

### Run the server
To start the server, use the following command:
```bash
docker-compose up --build -d
```

### Usage
You can use curl to send a request to the server:
```bash
curl -X POST https://domain.com/align \
-H "Content-Type: application/json" \
-d '{"username": "", "token": "", "exceptions": [""]}'
```

### Set up Scheduler for Automation
To automate the follow/unfollow synchronization, configure GitHub Actions as follows.

- Configuration files:
    - Workflow file: .github/workflows/follow_sync.yml
    - Secrets: secrets.GITHUB_TOKEN (PAT, user:follow)
    - Variables: vars.EXCEPTIONS

- github action code (follow_sync.yml)
    ```yml
    name: Follow Sync

    on:
      schedule:
        - cron: "0 0 * * *" # at midnight every day
      workflow_dispatch: 

    jobs:
      follow_sync:
        runs-on: ubuntu-latest

        steps:
          - name: Check out repository
            uses: actions/checkout@v2
          - name: Send Follow Sync Request
            env:
              USERNAME: ${{ github.actor }}
              TOKEN: ${{ secrets.TOKEN }}
              EXCEPTIONS: ${{ vars.EXCEPTIONS }}
            run: |
              curl -X POST "https://domain.com/align" \
                -H "Content-Type: application/json" \
                -d "{\"username\": \"$USERNAME\", \"token\": \"$TOKEN\", \"exceptions\": $EXCEPTIONS}"
    ```

- Variables (vars.EXCEPTIONS)
    ```json
    ["user1", "user2", "user3"]
    ```

- Result
    ```
    USERNAME: hwan001
    TOKEN: ***
    EXCEPTIONS: ["ssup2", "WireGuard", "666Lab", "Yeri-Kim"]
                                     Dload  Upload   Total   Spent    Left  Speed
    
      0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
      0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
    100   136    0     0  100   136      0     88  0:00:01  0:00:01 --:--:--    88
    100   168  100    32  100   136     20     87  0:00:01  0:00:01 --:--:--   108
    {"followed":[],"unfollowed":[]}
    ```