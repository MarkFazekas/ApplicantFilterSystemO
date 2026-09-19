#!/bin/bash
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PIDFILE="$SCRIPT_DIR/dynamodb-local.pid"
LOGFILE="$SCRIPT_DIR/dynamodb-local.log"

start() {
    if [ -f "$PIDFILE" ]; then
        PID=$(cat "$PIDFILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "DynamoDB service is already running with PID: $PID"
            return 0
        fi
    fi
    (
        cd "$SCRIPT_DIR" || exit 1
        exec java -Djava.library.path=DynamoDBLocal_lib -jar DynamoDBLocal.jar -dbPath databases -optimizeDbBeforeStartup -delayTransientStatuses -disableTelemetry -port 8000
    ) > "$LOGFILE" 2>&1 &
    echo $! > "$PIDFILE"
    echo "DynamoDB service is started with PID $(cat $PIDFILE)"
}

migrate(){
    if [ -f "$PIDFILE" ]; then
        export AWS_PAGER=""
        aws dynamodb create-table \
          --table-name ApplicantFilterSystemDev \
          --attribute-definitions \
            AttributeName=pk,AttributeType=S \
            AttributeName=sk,AttributeType=S \
          --key-schema \
            AttributeName=pk,KeyType=HASH \
            AttributeName=sk,KeyType=RANGE \
          --provisioned-throughput \
            ReadCapacityUnits=2,WriteCapacityUnits=2 \
          --profile afsd1_dev

        aws dynamodb update-time-to-live \
          --table-name ApplicantFilterSystemDev \
          --time-to-live-specification Enabled=true,AttributeName=expire_at \
          --profile afsd1_dev
        aws dynamodb list-tables --profile afsd1_dev
    else
        echo "Service not running"
    fi
}

stop() {
    if [ -f "$PIDFILE" ]; then
        PID=$(cat "$PIDFILE")
        kill "$PID" 2>/dev/null
        rm -f "$PIDFILE"
        echo "Service stopped"
    else
        echo "Service not running"
    fi
}

clean(){
  stop
  cd "$SCRIPT_DIR" && rm -rf databases/*.db
  cd "$SCRIPT_DIR" && rm dynamodb-local.log
  echo "Databases deleted."
}

case "$1" in
    clean-start)
        clean
        start
        sleep 2
        migrate
        ;;
    start)
        start
        ;;
    migrate)
        migrate
        ;;
    stop)
        stop
        ;;
    clean)
        clean
        ;;
    restart)
        stop
        sleep 2
        start
        ;;
    status)
        if [ -f "$PIDFILE" ] && kill -0 $(cat "$PIDFILE") 2>/dev/null; then
            echo "Running PID: $(cat $PIDFILE)"
            ps -aux | grep java
        else
            echo "Stopped"
            ps -aux | grep java
        fi
        ;;
    *)
        echo "Usage: $0 {clean-start|start|migrate|stop|clean|restart|status}"
        exit 1
esac
