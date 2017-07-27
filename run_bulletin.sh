#!/usr/bin/env bash


start() {
    cp -rf config_bulletin.py config.py
	sh run.sh start
}

stop() {
	sh run.sh stop
}

restart() {
    sh run.sh restart
}

status() {
    sh run.sh status
}

case "$1" in
	start|stop|restart|status)
  		$1
		;;
	*)
		echo $"Usage: $0 {start|stop|status|restart}"
		exit 1
esac
