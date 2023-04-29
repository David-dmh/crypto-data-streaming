#!/bin/bash

export PGPASSWORD='pwd'
psql -U 'usr' -d 'crypto' -a -f /sql/seed.psql
