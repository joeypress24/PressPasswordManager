from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    # function that generates encryption key and saves to file
    def create_key(self, path= 'mykey.key'):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as key_file:
            key_file.write(self.key)

    #function that loads key from existing file
    def load_key(self, path):
        with open(path, 'rb') as key_load:
            self.key=  key_load.read()

    # initial values passed into this in case we have predetermined values
    def create_password_file(self, path, initial_values=None):
        self.password_file = path

        # add passwords to the password file
        if initial_values is not None: #if something is provided
            for key, value in initial_values.items(): #iterate over dictionary
                self.add_password(key, value)

    def load_password_file(self, path):
        self.password_file = path
        with open(path, 'r') as f:
            for line in f: #decrypt each file
                site, encryptedPassword = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encryptedPassword.encode()).decode()

    # add a password to the manager
    def add_password(self, site, password):
        self.password_dict[site] = password
        if self.password_file is not None:
            with open(self.password_file, "a+") as f: # in appending mode so that I don't overright
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

    def get_password(self, site):
        return self.password_dict[site] # returns cyphertext of password

def main() -> int:
    password=  {
        'email':'1234567',
        'facebook':'helloworld123',
        'youtube':'myfavoritepassword'
    }
    pm = PasswordManager()
    #simple menu
    print("""What do you want to do?
    (1) Create a new key
    (2) Load an existing key
    (3) Create new password file
    (4) Load existing password file
    (5) Add a new password
    (6) Get a password
    (q) Quit    
    """)

    done = False 
    while not done:

        choice = input("Enter your choice: ")
        if choice == '1':
            path = input("Enter path: ")
            pm.create_key(path) #this will be the key that we now use for encryption and decryption
        elif choice == '2':
            path = input("enter path: ")
            pm.load_key(path)
        elif choice == '3':
            path = input('Enter path: ')
            pm.create_password_file(path, password)
        elif choice == '4':
            path = input('Enter path: ')
            pm.load_password_file(path)
        elif choice == '5':
            site = input("Enter the site: ")
            pwd = input('Enter the password: ')
            pm.add_password(site, pwd)
        elif choice == '6':
            site = input('what site do you want: ')
            print(f'Password for {site} is {pm.get_password(site)}')
        elif choice == 'q':
            done = True
            print("bye!")
        else:
            print('invalid choice!')


if __name__ == '__main__':
    main()
