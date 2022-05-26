# Features
1. Bot Money bank and actions
    - Money transfer button and logic
    - Money withdraw button and logic
    - Money deposit button and logic
    - Bank account balance tracking
2. Role collecter
    - Should run collect every 24 hours
    - Additional extractor logic (goes directly to bank acc)
    - depends on:
        1. Bot Money bank and actions
        2. Implement scheduling mechanism
3. Role crime
    - Should run crime every 4 hours
    - Additional extractor logic (negative values)
4. Logging to the file

# Logic
1. [DONE] Implement scheduling mechanism:
    - Celerybeat task execution every 5 minutes
    - New task with ETA should be added to the queue, based on data from the database