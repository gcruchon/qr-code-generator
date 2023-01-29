# QR Code Generator

A short utility to build custom QR Codes

## Install

```zsh
pipenv install
```

## Usage

```zsh
pipenv run python qr.py -t https://www.url-to-encode.com
```

Optionally, you can specify a name for your QR code:

```zsh
pipenv run python qr.py -t https://www.url-to-encode.com -o my_qr_code.png
```

Optionally, you can add a logo on top of QR code:

```zsh
pipenv run python qr.py -t https://www.url-to-encode.com -l logo.png
```

Please note that:

- QR codes are generated in the `output` folder.
- logo file should be in the `logos` folder.
