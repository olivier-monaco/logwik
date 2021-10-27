# Logwik

Compute statistics from HTTP(S) request handled by Nginx.

## My use case

This tool is used to provide statistics of HTTP(S) requests handled by Nginx as
a reverse proxy installed on multiple indenpent servers. It parses my own access
log format and aggregates requests based on multiple facets. Statistics are
saved to a MariaDB database version 10.5 with Aria storage engine. Rsyslog is
used to centralize all logs to one dedicated server which send back Nginx access
logs to the server running logwik.

Logs received are also saved to /volumes/data/nginx-logs/access_YYYYMMDDHH.log
files. Each file contains requests of one hour, based on date and time from rsyslog
(and not from Nginx).

All servers are Debian from Buster to Bullseye.

My Nginx log format is:
```
log_format yowik '$server_name $host $remote_addr $remote_port '
                 '$remote_user [$time_iso8601] $request_id "$request" $status '
                 '$body_bytes_sent "$http_referer" "$http_user_agent" '
                 '$hostname $request_time $gzip_ratio '
                 '"$sent_http_content_type" $upstream_addr $upstream_status '
                 '$upstream_connect_time $upstream_header_time '
                 '$upstream_response_time';
```

Logwik includes two binaries:
* logwik-rslg: programm called by rsyslog
* lowik: tools providing a "bulk" subcommand to import existing files

## My installation

Logwik is installed using PIP.

/etc/rsyslog.d/000-imrelp.conf
```
# Enable RELP network input
module(load="imrelp")
input(type="imrelp" port="2514")
```

/etc/rsyslog.d/000-omprog.conf
```
# Enable Program Output Module
module(load="omprog")
```

/etc/rsyslog.d/142-logwik.conf
```
# Template to output only message
template(
    name="LogwikMessageOnly"
    type="string"
    string="%msg:R,ERE,1,ZERO:^ nginx: (.*)$--end%\n"
)

# Template for access logs filename
template(name="LogwikAccessLog" type="list") {
    constant(value="/volumes/data/nginx-logs/")
    constant(value="access_")
    property(name="timereported" dateformat="year")
    property(name="timereported" dateformat="month")
    property(name="timereported" dateformat="day")
    property(name="timereported" dateformat="hour")
    constant(value=".log")
}

# Process access log
if ($syslogfacility-text == 'local6') and ($msg startswith ' nginx: ') then {
    if  ($syslogseverity-text == 'info') then {
        action(
            type="omfile"
            template="LogwikMessageOnly"
            dynafile="LogwikAccessLog"
            dircreatemode="0775"
            filecreatemode="0664"
        )
        action(
            type="omprog"
            binary="/usr/local/bin/logwik-rslg"
            confirmMessages="on"
            reportFailures="on"
            useTransactions="on"
            template="NgxMessageOnly"
            queue.type="LinkedList"
            queue.saveOnShutdown="on"
            queue.workerThreads="1"
            queue.filename="logwik"
            queue.maxDiskSpace="2G"
            forceSingleInstance="on"
            output="/var/log/logwik-rslg.log"
        )
    }

    # No more processing
    stop
}
```

/etc/rsyslog.d/399-drop-remote-logs.conf
```
# Ignore logs from remote system for all remaining rules
if $fromhost-ip != '127.0.0.1' then stop
```

/etc/logrotate.d/logwik
```
/var/log/logwik-rslg.log
{
        rotate 4
        weekly
        missingok
        notifempty
        compress
        delaycompress
        sharedscripts
        postrotate
                /usr/lib/rsyslog/rsyslog-rotate
        endscript
}
```

/etc/cron.daily/lowik-compress-nginx-logs
```
#! /bin/bash

set -e

find {{ logwik_nginx_logs_path }} -type f -name '*.log' -mtime +2 -exec bzip2 {} \;
```

/etc/logwik/logwik.conf
```
database:
  host: localhost
  user: logwik
  password: ***
  name: logwik

```
