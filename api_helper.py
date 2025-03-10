import uuid
from fastapi import HTTPException, Query
from models import User
from database import get_table

class ApiHelper:
    def __init__(self):
        self.table = get_table()

    def get_users(self, limit: int = 5, last_evaluated_key: dict = None):
        """Fetch limited users from the database with optional pagination."""
        try:
            scan_kwargs = {"Limit": limit}

            if last_evaluated_key:
                scan_kwargs["ExclusiveStartKey"] = last_evaluated_key

            response = self.table.scan(**scan_kwargs)

            return {
                "users": response.get("Items", []),
                "last_evaluated_key": response.get("LastEvaluatedKey", None)

            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error accessing DynamoDB: {str(e)}")

    def add_user(self, user: User):
        """Add a new user to the database, ensuring no duplicate emails."""
        try:
            existing_user = self.table.scan(
                FilterExpression="email = :email",
                ExpressionAttributeValues={":email": user.email}
            )

            if existing_user.get("Items"):  # If a user is found
                raise HTTPException(status_code=400, detail="User already exists")

            user_id = str(uuid.uuid4())


            new_item = {
                "uuid": user_id,
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
                "company": user.company,
                "jobTitle": user.jobTitle,
            }

            self.table.put_item(Item=new_item)
            return new_item
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving user: {str(e)}")

    def update_user(self, uuid: str, user: User):
        """Update an existing user in the database."""
        try:
            response = self.table.get_item(Key={"uuid": uuid})
            if "Item" not in response:
                raise HTTPException(status_code=404, detail="User not found")

            updated_item = {
                "uuid": uuid,
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
                "company": user.company,
                "jobTitle": user.jobTitle,
            }

            self.table.put_item(Item=updated_item)
            return updated_item
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

