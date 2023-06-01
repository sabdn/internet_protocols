from file import File


class MailCreator:
    def __init__(self):
        self.boundary = 'kikiki'
        self.mail = ''

    def add_header(self, login_from: str, to: str, subject: str):
        self.mail += f'From: {login_from}\nTo: {to}\nSubject: {subject}'
        self.mail += f'\nContent-Type: multipart/mixed; ' \
                     f'boundary={self.boundary}'

    def add_content(self, file: File, is_last: bool):
        self.mail += f'\n\n--{self.boundary}'
        self.mail += f'\nMime-Version: 1.0'
        self.mail += f'\nContent-Type: image/{file.file_ext}; ' \
                     f'name="=?UTF-8?B?{file.encoded_name}?="'
        self.mail += f'\nContent-Disposition: attachment; ' \
                     f'filename="=?UTF-8?B?{file.encoded_name}?="'
        self.mail += '\nContent-Transfer-Encoding: base64\n\n'
        self.mail += file.get_encoded_file()
        self.mail += f'\n--{self.boundary}'
        if is_last:
            self.mail += '--'

    def get_mail(self):
        return f'{self.mail}\n.\n'

