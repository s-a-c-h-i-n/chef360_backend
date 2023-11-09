from dbInstance import db
from sqlalchemy import Column, String, Integer, DateTime
from JWTInstance import jwt


class TokenBlocklist(db.Model):
    id = Column(Integer, primary_key=True)
    # as jti values are 36 chars long
    jti = Column(String(36), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)

    # Callback function to check if a JWT exists in the database blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None
