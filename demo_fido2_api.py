# This demo calls the server API and prints the details
# See demo_fido2 to get a high-level overview

import local_server
from device import MockDevice 
from io import BytesIO
from fido2 import cbor

def register():
    client = local_server.app.test_client()
    device = MockDevice()
    
    pkcco = cbor.decode(client.post('/api/register/begin').data)
    print('publicKeyCredentialCreationOptions: ', pkcco)
    print("\n\n")

    attestation = device.create(pkcco, 'https://localhost')
    print('new credential attestation: ', attestation)
    print("\n\n")

    attestation_data = cbor.encode({
        'clientDataJSON': attestation['response']['clientDataJSON'],
        'attestationObject': attestation['response']['attestationObject']
    })
    raw_response = client.post(
        '/api/register/complete',
        input_stream=BytesIO(attestation_data),
        content_type='application/cbor'
    )
    registration_response = cbor.decode(raw_response.data)
    print('registration response:', registration_response)


def authenticate():  
    client = local_server.app.test_client()

    device = MockDevice()
    device.cred_init('localhost', b'customhandle')
    local_server.credentials = [device.cred_as_attested()]

    raw_response = client.post(
        '/api/authenticate/begin'
    )
    pkcro = cbor.decode(raw_response.data)
    print('publicKeyCredentialRequestOptions: ', pkcro)
    print("\n\n")

    assertion = device.get(pkcro, 'https://localhost')
    print('credential assertion: ', assertion)
    print("\n\n")

    assertion_data = cbor.encode({
        'credentialId': assertion['rawId'],
        'clientDataJSON': assertion['response']['clientDataJSON'],
        'authenticatorData': assertion['response']['authenticatorData'],
        'signature': assertion['response']['signature'],
        'userHandle': assertion['response']['userHandle']
    })
    print('assertion data:', assertion_data)
    print("\n\n")

    raw_response = client.post(
        '/api/authenticate/complete',
        input_stream=BytesIO(assertion_data),
        content_type='application/cbor'
    )
    authentication_response = cbor.decode(raw_response.data)
    print('authentication response:', authentication_response)

def main():  
    print("REGISTER FIDO2")
    print("\n\n\n\n")
    register()
    print("\n\n\n\n")

    print("AUTH FIDO2")
    print("\n\n\n\n")
    authenticate()
    print("\n\n\n\n")

if __name__ == "__main__":
    main()

