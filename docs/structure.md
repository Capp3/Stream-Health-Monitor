# Application Structure

```bash
|- .github
|    |- dependabot.yml          # Dont know this cute guy yet
|- config                       # Data collection configuration  
|    |- config.yml              # configuration file for the application
|    |- sample.env
|    |- .env                    # .env file
|- docker                       # Docker for backend services, grafana and database
|    |- grafana
|    |    |- datasource.yml     # Grafana config
|    |- prometheus
|    |    |- prometheus.yml     # Prometheus configuration
|    |- docker-compose.yml      # External Services for script
|- docs
|    |- scratch.md              # notes / prompts / crap
|    |- structure.md            # This here, the only way I can think
|- src                          # The application
|    |- attributes              # configuration information
|    |    |- providers.py       # definitions for interacting with different streaming providers, retrieve url to be probed
|    |- main.py                 # Python application basics/ setup logging & log rotation
|    |- threads.py              # program actions, probe stream, return results as json
|- .gitignore                   # Git ignore file
|- LICENSE                      # Pretty straight forward
|- README.md                    # Readme... yep
|- requirements.txt
```
