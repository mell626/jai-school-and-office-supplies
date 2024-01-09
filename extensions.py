from flask import Flask, redirect, flash, render_template, jsonify, session, url_for, request
import csv
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from collections import Counter
import os
from datetime import datetime
from sqlalchemy import func, text
import time
import webbrowser