from _socket import gaierror

from argparse import ArgumentParser

from smtp_client import Client

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-f', '--from', type=str, default='<>', dest='sender', help='Sender\'s mailing address')
    parser.add_argument('-t', '--to', type=str, help='Recipient\'s mailing address')
    parser.add_argument('-d', '--directory', type=str, default='.', help='Directory with images (default $pwd)')
    parser.add_argument('--subject', type=str, default='Happy pictures',
                        help='Optional parameter specifying the subject of the email, '
                             'the default subject is “Happy Pictures”')
    parser.add_argument('-s', '--server', type=str, default='smtp.mail.ru:25',
                        help='Address (or domain name) of the SMTP server in the format address[:port]')
    parser.add_argument('--ssl', action='store_true',
                        help='Allow the use of ssl if the server supports (do not use by default)')
    parser.add_argument('--auth', action='store_true', help='Whether to request authorization (not by default)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Displaying the work protocol')

    args = parser.parse_args()
    try:
        client = Client(args.sender, args.to, args.subject, args.ssl, args.auth, args.verbose, args.directory,
                        args.server)
        client.run()
    except ValueError as e:
        print(e)
    except gaierror:
        print('DNS Error')
    except ConnectionError:
        print('Connection error')
