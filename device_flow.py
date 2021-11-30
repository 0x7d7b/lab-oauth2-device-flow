import requests
import json
import webbrowser

from time import sleep
from colorama import init, Fore
from halo import Halo

if __name__ == '__main__':

    init(autoreset=True)


    # Okta
    # See: https://developer.okta.com/docs/guides/device-authorization-grant/main/
    # authorize_endpoint = 'https://dev-xxxxxxxx.okta.com/oauth2/default/v1/device/authorize'
    # token_endpoint = 'https://dev-xxxxxxxx.okta.com/oauth2/default/v1/token'
    # client_id = 'xxxxxxxxxxxxxxxxxxxx'
    # scopes = 'openid profile email'

    # GitHub
    # See: https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps
    authorize_endpoint = 'https://github.com/login/device/code'
    token_endpoint = 'https://github.com/login/oauth/access_token'
    client_id = 'd7ad6beea9f98fd6adef'  # Just this test script.
    scopes = 'read:user user:email read:gpg_key read:public_key'


    print(Fore.LIGHTBLACK_EX + 'Initiating device flow...')
    authorize_response = requests.post(
        authorize_endpoint,
        headers={
            'Accept': 'application/json'
        },
        data={
            'client_id': client_id,
            'scope': scopes
        }
    )
    device_flow = authorize_response.json()

    if not authorize_response.status_code == 200:
        # See: https://datatracker.ietf.org/doc/html/rfc6749#section-5.2
        if 'error' in device_flow:
            if 'error_description' in device_flow:
                print(Fore.LIGHTRED_EX + device_flow['error_description'])
            else:
                print(Fore.LIGHTRED_EX + device_flow['error'])
        exit(1)

    expires_in = int(device_flow['expires_in'])

    print(
        Fore.LIGHTWHITE_EX + 'Navigate to ',
        Fore.LIGHTYELLOW_EX + device_flow['verification_uri'],
        Fore.LIGHTWHITE_EX + ' and type in your activation code: ',
        Fore.LIGHTYELLOW_EX + device_flow['user_code'],
        Fore.LIGHTBLACK_EX +
        f'\nWaiting for activation (max {expires_in} seconds)...',
        sep=''
    )
    if 'verification_uri_complete' in device_flow:
        webbrowser.open_new_tab(device_flow['verification_uri_complete'])

    interval = int(device_flow['interval'])

    spinner = Halo(
        spinner='dots',
        interval=150,
        placement='left',
        color="grey"
    )
    spinner.start()

    while True:
        try:
            sleep(interval)
        except KeyboardInterrupt:
            spinner.stop()
            print(Fore.LIGHTBLACK_EX + 'Aborting...')
            exit(1)
        response = requests.post(
            token_endpoint,
            headers={
                'Accept': 'application/json'
            },
            data={
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
                'client_id': client_id,
                'device_code': device_flow['device_code']
            }
        )
        pending_response = response.json()
        # See: https://datatracker.ietf.org/doc/html/rfc8628#section-3.5
        if ('error' in pending_response
                and pending_response['error'] == 'authorization_pending'):
            continue
        elif ('error' in pending_response
                and pending_response['error'] == 'slow_down'):
            interval = interval + 5
            continue
        elif 'error' in pending_response:
            spinner.stop()
            if 'error_description' in pending_response:
                print(Fore.LIGHTRED_EX +
                    pending_response['error_description'])
            else:
                print(Fore.LIGHTRED_EX + pending_response['error'])
            exit(1)
        else:
            spinner.stop()
            print(Fore.LIGHTYELLOW_EX + json.dumps(
                pending_response,
                indent=2)
            )
            exit(0)
