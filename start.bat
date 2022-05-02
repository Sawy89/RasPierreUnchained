@REM Batch file for launching the fastapi service inside docker with API for SII downloader
if not exist "_backup" mkdir _backup
if not exist "_backup\log" mkdir _backup\log

@REM Start docker services
docker-compose -f docker-compose.windev.yml down
docker-compose -f docker-compose.windev.yml build
docker-compose -f docker-compose.windev.yml up