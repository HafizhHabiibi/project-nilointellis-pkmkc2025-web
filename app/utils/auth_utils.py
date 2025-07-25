from functools import wraps
from flask import request, jsonify, session, flash, redirect, url_for, current_app
from datetime import datetime, timedelta
import uuid
import hashlib

# Session controller

def generate_session_id():
    """Generate unique session ID dengan timestamp"""
    timestamp = str(datetime.utcnow().timestamp())
    random_uuid = str(uuid.uuid4())
    combined = f"{timestamp}_{random_uuid}"
    return hashlib.md5(combined.encode()).hexdigest()

def web_session_required(f):
    """Decorator untuk memerlukan session pada web routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not check_session():
            flash('Silakan login terlebih dahulu!', 'warning')
            return redirect(url_for('main.index'))

        if is_session_expired():
            clear_session()
            flash('Session Anda telah berakhir. Silakan login kembali!', 'warning')
            return redirect(url_for('main.index'))

        # Refresh session activity
        refresh_session_activity()
        return f(*args, **kwargs)

    return decorated

def check_session():
    """Check apakah user sudah login"""
    return 'user_id' in session and 'username' in session

def is_session_expired():
    """Check apakah session sudah expired berdasarkan config timeout"""
    if 'last_activity' not in session:
        return True

    try:
        last_activity = datetime.fromisoformat(session['last_activity'])
        current_time = datetime.utcnow()
        time_diff = current_time - last_activity

        # Ambil timeout dari config
        timeout_hours = getattr(current_app.config, 'SESSION_TIMEOUT_HOURS', 1)
        return time_diff > timedelta(hours=timeout_hours)
    except Exception as e:
        # Jika ada error dalam parsing, anggap session expired
        return True

def refresh_session_activity():
    """Refresh session activity timestamp"""
    if check_session():
        session['last_activity'] = datetime.utcnow().isoformat()

def clear_session():
    """Clear semua data session"""
    session.clear()

def create_user_session(user):
    """Create session untuk user yang berhasil login"""
    session.permanent = True
    session['user_id'] = str(user['_id'])
    session['username'] = user['username']
    session['session_id'] = generate_session_id()
    session['last_activity'] = datetime.utcnow().isoformat()

def check_session_and_timeout():
    """Check session dan handle timeout - untuk backward compatibility"""
    if not check_session():
        return False

    if is_session_expired():
        clear_session()
        return False

    # Refresh session activity
    refresh_session_activity()
    return True