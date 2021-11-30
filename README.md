# OAuth2 Device Flow (LAB)

This is an experimental Python script for OAuth2 device flow tryouts.

## Preparation

You need to have access on an authorization server which supports the device flow. I ran tests with [Okta](https://developer.okta.com/) and [Github](https://github.com/settings/developers).

Some dependencies are required which can be easily installed with `pipenv`:

```shell
$ pipenv install
Installing dependencies from Pipfile.lock (a4f09b)...
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 9/9 — 00:00:03
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

## Usage

First exchange the client id and the authorization server endpoints in the script. These are my properties for running tests against GitHub:

```python
authorize_endpoint = 'https://github.com/login/device/code'
token_endpoint = 'https://github.com/login/oauth/access_token'
client_id = 'd7ad6beea9f98fd6adef'  # Just this test script.
scopes = 'read:user user:email read:gpg_key read:public_key'
```

Then simply run it and follow the instructions printed on the console. As a result you should see a valid access token which can be used, now.

```shell
$ python device_flow.py
Initiating device flow...
Navigate to https://github.com/login/device and type in your activation code: 8A8A-64DC
Waiting for activation (max 899 seconds)...
{
  "access_token": "gho_sCJG47YoU4AWIroJwQ7O4xRMLbiBWt4I6Z8e",
  "token_type": "bearer",
  "scope": "read:gpg_key,read:public_key,read:user,user:email"
}
```