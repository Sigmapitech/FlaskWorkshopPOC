import secrets
from typing import Dict, Tuple

from flask import Blueprint, request, session

from .consts import Response, Method
from .database import open_cursor
from .security import blake2b_with_salt

api = Blueprint("api", __name__)


@api.route("/", methods=(Method.GET,))
def index() -> Tuple[Dict[str, str], int]:
    return {
        "message": "Hello, world!",
    }, Response.OK


@api.route("/register", methods=(Method.POST,))
def register() -> Tuple[Dict[str, str], int]:
    if session.get("user_id"):
        return {
            "message": "You are already logged in.",
        }, Response.BAD_REQUEST

    email: str = request.form.get("email")
    password: str = request.form.get("password")

    if not email or not password:
        return {
            "message": "Email and password are required.",
        }, Response.BAD_REQUEST

    salt = secrets.token_hex(16)
    digest = blake2b_with_salt(password, salt)
    with open_cursor() as cursor:
        cursor.execute(
            "INSERT INTO user (email, password) VALUES (%s, %s)",
            (email, f"{digest}:{salt}"),
        )

    return {"message": "User registered successfully!"}, Response.OK


@api.route("/login", methods=(Method.POST,))
def login() -> Tuple[Dict[str, str], int]:
    email: str = request.form.get("email")
    password: str = request.form.get("password")

    if not email or not password:
        return {
            "message": "Email and password are required.",
        }, Response.BAD_REQUEST

    if session.get("user_id"):
        return {"message": "You are already logged in."}, Response.BAD_REQUEST

    with open_cursor() as cursor:
        cursor.execute(
            "SELECT password FROM user WHERE email = %s",
            (email,),
        )
        result = cursor.fetchone()

    if result is None:
        return {"message": "Invalid email or password."}, Response.UNAUTHORIZED

    digest, salt = result[0].split(":")
    state = digest == blake2b_with_salt(password, salt)

    if not state:
        return {"message": "Invalid email or password."}, Response.UNAUTHORIZED

    session["user_id"] = email
    return {"message": "Logged in successfully."}, Response.OK
