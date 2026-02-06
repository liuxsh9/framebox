module.exports = {
  apps: [{
    name: 'framebox',
    script: 'uv',
    args: 'run python main.py',
    interpreter: 'none',
    cwd: './',
    env: {
      PORT: process.env.PORT || 8001,
      HOST: process.env.HOST || '0.0.0.0',
      DATA_DIR: process.env.DATA_DIR || './data'
    },
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,
    min_uptime: '10s',
    max_restarts: 10,
    restart_delay: 4000
  }]
};
