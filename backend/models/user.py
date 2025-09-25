from ..extensions import db
from passlib.hash import bcrypt

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email_address = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    mbti = db.Column(db.String(4), nullable=True)
    attachment_style = db.Column(db.String(50), nullable=True)
    relationship_goal = db.Column(db.String(50), nullable=True)
    hobbies = db.Column(db.Text, nullable=True)

    @staticmethod
    def hash_password(plain_password: str) -> str:
        return bcrypt.hash(plain_password)
    
    def verify_password(self, plain_password: str) -> bool:
        return bcrypt.verify(plain_password, self.password_hash)

    def to_dict(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "emailAddress": self.email_address,
            "mbti": self.mbti,
            "attachmentStyle": self.attachment_style,
            "relationshipGoal": self.relationship_goal,
            "hobbies": self.hobbies,
        }
