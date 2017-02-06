redis-server --daemonize yes & \\
celery -A application worker -l info & \\
