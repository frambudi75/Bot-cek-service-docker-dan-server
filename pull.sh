#!/bin/bash
cp .env /tmp/.env.bak
git reset --hard HEAD
git pull origin main
mv /tmp/.env.bak .env
systemctl restart telegrambot
