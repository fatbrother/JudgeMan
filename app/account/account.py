from app import db, bcrypt

class AccountCheckSystem():
    def addAccount(self, username: str, email: str, password: str) -> None:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db.User.insert(username, email, hashed)

    def deleteAccount(self, username: str) -> None:
        db.User.delete(username)

    def updateAccount(self, username: str, email: str, password: str) -> None:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db.User.update(username, email, hashed)

    def checkAccount(self, username: str, email: str, password: str) -> str:
        user = db.User.query(username)
        if not user:
            return "User not found"

        if user.email != email:
            return "Email not match"

        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            return "Success"
        
        return "Something went wrong"