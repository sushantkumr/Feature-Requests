from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABcMB5CdnFU6H8wJjJ9f9LXz7gI3sj7jExPfXK147vaaMC--z6E86MIZAr7uuu_bRTHcQ8BUBhCBFGEGWD7PAKBSy-PbtYw27rozT9p9gOWyp61fom9ZCKDW89uveD9xnZzvMYMPzavg41wkQQm1Mh1MaDhdUgiu6Lg3u_0dTd_ehAKfeImYRzteBHRF8B4LP0Jq7oT'


def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
