# Credentials Directory

Do not store real credentials in this directory if they can live in a password manager or `.env`.

This folder exists only as a documented placeholder for rare cases where a tool expects local credential material.

## Rules

- Prefer password manager + `.env` over files here.
- Do not commit files placed here.
- If a tool requires a local credential file, keep it here temporarily and remove it when done.
- Treat this directory as ignored local state.

## Examples

Examples of files that might temporarily appear here:
- OAuth client JSON
- temporary service account file
- exported token cache

But again: prefer not to use this folder unless a tool truly requires it.
