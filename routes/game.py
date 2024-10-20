from flask import Blueprint, jsonify, session, request
from models import db, User, Score
import json
import random

game_bp = Blueprint('game', __name__)