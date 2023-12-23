from base64 import b64decode, b64encode

def decode_b64(text):
    try:
        print(f"Decoding: {text}")
        decoded_text = b64decode(text).decode("utf-8")
        if decoded_text:
            print(f"Decoded: {decoded_text}")
            return decoded_text
    except Exception as e:
        print(f"Error (Decoding): {e}")


def encode_b64(text): 
    try:
        print(f"Encoding: {text}")
        encoded_text = b64encode(text.encode("utf-8")).decode("utf-8")
        if encoded_text:
            print(f"Encoded: {encoded_text}")
            return encoded_text
    except Exception as e:
        print(f"Error (Encoding): {e}")
