import binascii
import datetime
import hashlib
import os
import re
import secrets
import subprocess
from typing import Optional, NoReturn, List

import flask
import jwt

from bv_rest.database import get_cursor

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(hashed_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = hashed_password[:64]
    hashed_password = hashed_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == hashed_password

def init_api(api):
    @api.schema
    class Identity:
        login: str
        email: str
        first_name: Optional[str]
        last_name: Optional[str]
        institution: Optional[str]
        registration_time: Optional[datetime.datetime]
        email_verification_time: Optional[datetime.datetime]
        activation_time: Optional[datetime.datetime]
        deactivation_time: Optional[datetime.datetime]

    @api.schema
    class NewIdentity:
        login: str
        password: str
        email: str
        first_name: Optional[str]
        last_name: Optional[str]
        institution: Optional[str]

    @api.path('/public_key')
    def get() -> str:
        '''Return the public key of the authorization server'''
        return open('/bv_admin/id_rsa.pub').read()
    
    @api.path('/api_key')
    @api.may_abort(401)
    def post(login : str, password : str) -> str:
        '''
        Return an API key for this user to use in api_key header.
        '''
        with get_cursor('bv_services') as cur:
            sql = 'SELECT password FROM identity WHERE login=%s'
            cur.execute(sql, [login])
            if cur.rowcount:
                password_hash = cur.fetchone()[0]
                if verify_password(password_hash, password):
                    session_id = secrets.token_urlsafe()
                    sql = 'DELETE FROM session WHERE login=%s'
                    cur.execute(sql, [login])
                    now = datetime.datetime.utcnow()
                    sql = 'INSERT INTO session (id, login, creation_time) VALUES (%s, %s, %s)'
                    cur.execute(sql, [session_id, login, now])
                    now = datetime.datetime.utcnow()
                    payload = {'sub': session_id,
                            'iss': 'bv_admin',
                            'iat': now,
                            'login': login,
                            }
                    private_key = open('/bv_admin/id_rsa').read()
                    api_key = jwt.encode(payload, private_key, algorithm='RS256').decode('utf8')
                    return api_key
        flask.abort(401, 'Invalid login or password')

    @api.path('/identities')
    @api.require_role('identity_admin')
    def get() -> List[Identity]:
        '''List all identities'''
        with get_cursor('bv_services', as_dict=True) as cur:
            sql = 'SELECT login, email, first_name, last_name, institution, registration_time, email_verification_time, activation_time, deactivation_time FROM identity'
            cur.execute(sql)
            return cur.fetchall()


    @api.path('/identities')
    @api.require_role('identity_admin')
    @api.param_in_body
    def post(identity : NewIdentity) -> Identity:
        '''Create a new identity'''
        with get_cursor('bv_services') as cur:
            time = datetime.datetime.utcnow()
            identity['activation_time'] = time
            identity['email_verification_time'] = time
            identity['registration_time'] = time
            return identity
            sql = 'UPDATE identity SET activation_time = %s, email=%s, email_verification_time = %s WHERE login = %s;'
            cur.execute(sql, [time, user.email, time, user.login])
            sql = 'INSERT INTO cati_portal.granting (login, project, credential) VALUES (%s, %s, %s);'
            cur.executemany(sql, [[user.login, 'cati_portal', 'server_admin'],
                                    [user.login, 'cati_portal', 'user_moderator']])
            flash(f'Administrator {form.login.data} succesfully registered and activated with server and user management rights', 'success')
            user = User.get(user.login, bypass_access_rights=True)
            login_user(user)
            os.remove(hash_file)
            flask.abort(403)
        flask.abort(404)


    @api.path('/sessions')
    @api.require_role('identity_admin')
    def get() -> List[str]:
        '''List all identities'''
        with get_cursor('bv_services', as_dict=True) as cur:
            sql = 'SELECT * FROM session'
            cur.execute(sql)
            return cur.fetchall()


    @api.path('/databases')
    #@api.require_role('database_admin')
    def get() -> List[str]:
        '''List all dtabases'''
        with get_cursor('bv_services') as cur:
            sql = "SELECT datname FROM pg_database WHERE datistemplate IS FALSE AND datname != 'postgres'"
            cur.execute(sql)
            return [row[0] for row in cur]
    
    @api.path('/databases/<database>/tables')
    #@api.require_role('database_admin')
    def get(database: str) -> List[str]:
        '''List all tables of a database'''
        with get_cursor('bv_services') as cur:
            sql = '''SELECT schemaname, tablename 
                     FROM pg_tables 
                     WHERE schemaname NOT IN ('pg_catalog', 
                                              'information_schema')'''
            cur.execute(sql)
            return [(row[1] if row[0] == 'public' else f'{row[0]}.{row[1]}') for row in cur]
    

    @api.path('/databases/<database>/schema')
    #@api.require_role('database_admin')
    def get(database: str) -> str:
        '''Return the schema of a database in SQL format'''
        output = subprocess.check_output([
            'docker', 'exec', 'bv_postgres', 'pg_dump','-U', 
            flask.current_app.postgres_user, '-d', 'bv_services', '-s'])
        return re.sub(r'^--[^\n]*\n', '', output.decode('utf8'), 0, re.MULTILINE).strip().replace('\n\n\n', '\n\n')
    
