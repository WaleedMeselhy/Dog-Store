#!/usr/bin/env bash
docker-compose up -d
status=$(docker-compose ps --services --filter 'status=stopped' | grep api)
while [[ -z $status ]];do
  sleep 5
  status=$(docker-compose ps --services --filter 'status=stopped' | grep api)

done
docker-compose down
