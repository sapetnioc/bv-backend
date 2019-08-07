import binascii
import datetime
import hashlib
import os
import secrets
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
    class NewIdentity:
        login: str
        password: bytes
        email: str
        first_name: Optional[str]
        last_name: Optional[str]
        institution: Optional[str]

    @api.schema
    class Identity(NewIdentity):
        registration_time: Optional[datetime.datetime]
        email_verification_time: Optional[datetime.datetime]
        activation_time: Optional[datetime.datetime]
        deactivation_time: Optional[datetime.datetime]


    @api.path('/public_key')
    def get() -> str:
        '''Return the public key of the authorization server'''
        return open('/bv_auth/id_rsa.pub').read()
    
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
                    sql = 'SELECT role, given_to, inherit FROM granting'
                    cur.execute(sql)
                    grantings = {}
                    links = {}
                    for role, given_to, inherit in cur:
                        grantings.setdefault(given_to, set()).add(role)
                        if inherit:
                            links.setdefault(given_to, set()).add(role)
                    user_role = f'${login}'
                    roles = {user_role}
                    roles.update(grantings.get(user_role, set()))
                    new_roles = set()
                    while True:
                        for role in roles:
                            new_roles.add(role)
                            for linked_role in links.get(role, set()):
                                new_roles.update(grantings.get(linked_role, set()))
                        if new_roles == roles:
                            break
                        roles = new_roles
                    session_id = secrets.token_urlsafe()
                    sql = 'DELETE FROM session WHERE login=%s'
                    cur.execute(sql, [login])
                    sql = 'INSERT INTO session (id, login, roles) VALUES (%s, %s, %s)'
                    cur.execute(sql, [session_id, login, list(roles)])
                    now = datetime.datetime.utcnow()
                    obsolete = now + datetime.timedelta(minutes=30)
                    payload = {'sub': session_id,
                            'iss': 'bv_auth',
                            'iat': now,
                            'exp': obsolete,
                            }
                    private_key = open('/bv_auth/id_rsa').read()
                    api_key = jwt.encode(payload, private_key, algorithm='RS256').decode('utf8')
                    return api_key
        flask.abort(401, 'Invalid login or password')

    @api.path('/sessions')
    @api.require_role('identity_admin')
    def get() -> List[str]:
        '''List all identities'''
        with get_cursor('bv_services', as_dict=True) as cur:
            sql = 'SELECT * FROM session'
            cur.execute(sql)
            return cur.fetchall()
    
    
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
    def post(identity : NewIdentity) -> Identity:
        '''Create a new identity'''
        with get_cursor('bv_services') as cur:
            time = datetime.datetime.now()
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
