#!/bin/bash
cd ~/aegis-ai-os
source venv/bin/activate
python agents/aegis_supervisor.py "$@"
