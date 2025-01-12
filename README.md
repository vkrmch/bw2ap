# bw2ap
## Bitwarden to Apple password converter
This simple tool converts bitwarden exported `csv` file to format that can be imported in Apple Passwords app

Clone the repo

    git clone https://github.com/vkrmch/bw2ap.git

**Usage**

    pip install -r requirements.txt

    bw2ap.py <source_file>

Converted file should be created in the same folder as source file with `_converted` in the name.

## Understanding file formats

Format of Apple Passwords File

- Columns
    - Title
    - URL
    - Username
    - Password
    - Nptes
    - OTPAuth
- No way to export PassKeys
- Multiple URLs are represented as multiple lines with repeating values for Title, Username, Password, Notes, OTPAuth
    - Unfortunately, importing this back into Apple Passwords does not honor this and instead creates multiple items.

Format of Bitwarden File

- Columns
    - collections
    - type
    - name
    - notes
    - fields
    - reprompt
    - login_uri
    - login_username
    - login_password
    - login_totp
- Multiple URLs are separated by comma
- Custom field/value separated by newline in the fields column, e.g.
    - Line 1: Custom Field 1: Custom Field 1 Value
    - Line 2: Custom Field 2: Custom Field 2 Value

Migration from Bitwarden to Apple Passwords, mapping:

| Apple File Column | Bitwarden File Column | Transformations / Comments                                                                                                                                         |
| --- | --- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Title | name |                                                                                                                                                                    |
| URL | login_uri | If multiple URLs in bitwarden, create a new row. All these will get imported as individual items, unfortunately. |
| Username | login_username |                                                                                                                                                                    |
| Password | login_password |                                                                                                                                                                    |
| Notes | fields, notes | Recommended to combine both columns as there is custom fields are not supported by Apple Password                                                                  |
| OTPAuth | login_totp | Note: this is untested                                                                                                                                             |

https://blog.vikramchauhan.com/evolving-passwords-transitioning-from-bitwarden-to-apple-passwords/