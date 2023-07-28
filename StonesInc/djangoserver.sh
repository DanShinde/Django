#!/bin/bash

# Navigate to the specified path
cd /home/givakik/Desktop/Pravin/20230327/DjangoE/StonesInc

# Run the Django server in the background
python manage.py runserver 0.0.0.0:8000 &

# Wait for a few seconds to ensure the server starts up properly
sleep 5

# Open Chromium and visit the specified address
chromium-browser --noerrdialogs --disable-session-crashed-bubble --kiosk localhost:8000/home
