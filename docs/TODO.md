# Features
0. [DONE] Resend feature
    - If servers responds with 429, resend the request with the same data.
    - Cleanup the delays in collect and schedule functions
1. [DONE] Send message function
    - Sends following message to the current channel:
2. [DONE] Bot Money bank and actions
    - Money transfer button and logic
    - Money withdraw button and logic
    - Money deposit button and logic
    - Bank account balance tracking
3. [DONE] Role collecter
    - Should run collect every 24 hours
    - Additional extractor logic (goes directly to bank acc)
    - depends on:
        1. Bot Money bank and actions
        2. Implement scheduling mechanism
4. [DONE] Role crime
    - Should run crime every 4 hours
    - Additional extractor logic (negative values)
5. Crime bugfix
6. Logging to the file
7. Image hub

# Logic
1. [DONE] Implement scheduling mechanism:
    - Celerybeat task execution every 5 minutes
    - New task with ETA should be added to the queue, based on data from the database