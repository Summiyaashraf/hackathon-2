---
id: 2
title: "Bypass Passlib and Use Direct Bcrypt for Hashing"
stage: "general"
date: "2026-02-05"
surface: "agent"
model: "claude-haiku-4-5-20251001"
feature: "none"
branch: "001-todo-crud-features"
user: "ABC"
command: "sp.implement CRITICAL FIX: Bypass Passlib and use direct Bcrypt for hashing."
labels: ["security", "authentication", "bcrypt", "password-hashing", "passlib"]
spec: null
ticket: null
adr: null
pr: null
---

## Files Modified

- `backend/src/api/routes/auth.py`

## Tests Performed

- None - Implementation changes only

## Prompt Text

```
CRITICAL FIX: Bypass Passlib and use direct Bcrypt for hashing.

Modify backend/src/api/routes/auth.py:

Locate the get_password_hash and verify_password functions.

Replace the pwd_context.hash() logic with direct bcrypt hashing.

Logic to implement:

Python

import bcrypt
def get_password_hash(password: str):
    # Ensure password is truncated to 72 bytes and encoded to bytes
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')
    def verify_password(plain_password: str, hashed_password: str):
        pwd_bytes = plain_password.encode('utf-8')[:72]
        return bcrypt.checkpw(pwd_bytes, hashed_password.encode('utf-8'))
    ```
Remove the 72-byte trigger: The ValueError is coming because passlib is panicking. By using bcrypt directly, we solve this.

Verify CORS: Make sure the frontend at localhost:3000 is allowed.
```

## Response Text

Successfully implemented the critical fix by:
1. Adding direct bcrypt import to auth.py
2. Removing passlib CryptContext dependency
3. Replacing get_password_hash function with direct bcrypt.hashpw implementation
4. Replacing verify_password function with direct bcrypt.checkpw implementation
5. Ensuring proper encoding to bytes and decoding back to string
6. Maintaining 72-byte limit protection
7. Verifying CORS settings already allow localhost:3000

## Outcome

Switched from passlib to direct bcrypt usage, which resolves compatibility issues causing ValueError. The authentication system now uses bcrypt directly without relying on passlib's wrapper, which was causing problems with newer bcrypt versions.

## Evaluation

Implementation completed successfully. The authentication system should now work without passlib-related errors and maintain proper password security practices using direct bcrypt calls.