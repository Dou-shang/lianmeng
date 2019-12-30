#!/bin/bash
kill -9 $(ps -aux | grep nginx | awk '{ print $2 }' | sed -n '1p')
kill -9 $(ps -aux | grep nginx | awk '{ print $2 }' | sed -n '1p')
kill -9 $(ps -aux | grep uwsgi | awk '{ print $2 }' | sed -n '1p')
kill -9 $(ps -aux | grep uwsgi | awk '{ print $2 }' | sed -n '1p')
kill -9 $(ps -aux | grep uwsgi | awk '{ print $2 }' | sed -n '1p')
kill -9 $(ps -aux | grep uwsgi | awk '{ print $2 }' | sed -n '1p')
