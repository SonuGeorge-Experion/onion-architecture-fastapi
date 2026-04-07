---
name: Api-response-structure
description: Create a standsrd api response structure.
---

# Implement a consistent API response structure across the project using:

Separate Success & Error response models
Pagination support
Clean folder structure (aligned with Onion Architecture)

# This ensures:

Consistent API responses
Clean OpenAPI (Swagger)
Better frontend integration

# Folder Structure

Create the following structure inside app/:

app/
 ├── api/
 │    ├── v1/responses/
 │    │     ├── success.py
 │    │     ├── error.py
 │    │     └── pagination.py

Do not create error handler. Error handler is in app/api/exceptions/error_handler.py

# Note
This is to create a standard api response structure for the APIs. Do not update any API as part of this Skill.

# Final Response Formats Examples
✅ Success
{
  "success": true,
  "message": "User fetched successfully",
  "data": {
    "id": 1,
    "name": "Ajith"
  }
}
❌ Error
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "type": "DomainException",
    "message": "User does not exist",
    "details": null
  }
}
❌ Validation Error
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": [
      {
        "loc": ["body", "email"],
        "msg": "field required",
        "type": "value_error"
      }
    ]
  }
}