# mock_fido2
Demo of fido2 APIs without requiring a physical device.

## what it does

The project mocks a device and authenticates against a local FIDO2 server.

```
def authenticate():
    device = MockDevice()
    device.cred_init('localhost', b'customhandle')
    registered_credential = device.cred_as_attested()

    fido_server = Fido2Server(PublicKeyCredentialRpEntity('localhost', 'test server'))
    options, state = fido_server.authenticate_begin([registered_credential])
    assertion = device.get(options, 'https://localhost')
    
    fido_server.authenticate_complete(
        state,
        [registered_credential],
        assertion['rawId'],
        ClientData(assertion['response']['clientDataJSON']),
        AuthenticatorData(assertion['response']['authenticatorData']),
        assertion['response']['signature']
    )
```

## install

### requirements

This project has been tested with python 3. It builds on yubico's implementation of [fido2](https://github.com/Yubico/python-fido2). 

You need to install the requirements first:
> pip install -r requirements.txt

### start the demo

You may start the demo with the following command:
> python demo_fido2_api.py

It will print out the steps for registration and authentication.




