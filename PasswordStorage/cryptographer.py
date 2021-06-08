# -*- coding: utf-8 -*-

from base64 import urlsafe_b64encode, urlsafe_b64decode


class Cryptographer:
    """ Cryptographer

    Methods
    -------
    encode_text : `staticmethod`
    decode_text : `staticmethod`
    """

    @staticmethod
    def encode_text(string, key):
        """
        Parameters
        ----------
        string : |str| or |bytes|, required
            The string to encode
        key : |str|, required
            A special key that is used for encryption

        Returns
        -------
        :class:`bytes`
            Encoded text

        Examples
        --------
        >>> Cryptographer.encode_text(string="Text for encryption", key="SuperSecret_key")
        """

        string = string if isinstance(string, str) else string.decode("UTF-8")

        encoded_chars = []
        for chr_num in range(len(string)):
            key_char = key[chr_num % len(key)]
            encoded_char = chr(ord(string[chr_num]) + ord(key_char) % 256)
            encoded_chars.append(encoded_char)

        encoded_string = "".join(encoded_chars).encode("latin")

        return urlsafe_b64encode(encoded_string).rstrip(b"=")

    @staticmethod
    def decode_text(string, key):
        """
        Parameters
        ----------
        string : |str| or |bytes|, required
            The string to decode
        key : |str|, required
            A special key that is used for decryption

        Returns
        -------
        :class:`str`
            Decoded text

        Examples
        --------
        >>> Cryptographer.encode_text(string=b"p9ro2ZK51NWSyuLC3d7px97f0w", key="SuperSecret_key")
        """

        string = string if isinstance(string, bytes) else string.encode("UTF-8")
        string = urlsafe_b64decode(string + b"===").decode("latin")

        encoded_chars = []
        for chr_num in range(len(string)):
            key_char = key[chr_num % len(key)]
            encoded_char = chr((ord(string[chr_num]) - ord(key_char) + 256) % 256)
            encoded_chars.append(encoded_char)

        return "".join(encoded_chars)
