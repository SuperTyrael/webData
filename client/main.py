from ast import arg
from cmd import Cmd
import getpass
import sys
from urllib import response
import requests
import json
from prettytable import PrettyTable


from prompt_toolkit import prompt


class client(Cmd):
    prompt = "RateProf>"
    intro = "Welcome to RateProf!"
    url = "http://127.0.0.1:8000/rate"
    cookie = 0
    session=requests.session()

    def _init(self):
        Cmd.__init__(self)

    def default(self, line):
        print("Unknown command: " + line)

    def emptyline(self):
        print("Please input a command.")

    def loginCheck(self):
        if self.cookie == 0:
            return True
        else:
            return True

    def register(self, url):
        print("Welcome! You are registering, please input your username.")
        flag = 0
        while (flag == 0):
            username = input("Username: ")
            print("Please input your email.")
            email = input("Email: ")
            print("Please input your password.")
            password = getpass.getpass("Password: ")
            affirm_password = getpass.getpass("Confirm password: ")
            if (password == affirm_password):
                flag = 1
            else:
                print("Passwords do not match!")
        user_data = {'username': username,
                     'email': email, 'password': password}

        resp = self.session.post(url, json=user_data)
        print(resp.text)

    def login(self, url):
        print("Please input your username.")
        username = input("Username: ")
        print("Please input your password.")
        password = getpass.getpass("Password: ")
        user_data = {'username': username, 'password': password}
        resp = self.session.post(url, json=user_data)
        print(resp.text)

    def do_register(self, args):
        """
        Register a new user.
        """
        url = self.url+"/register/"
        self.register(url)

    def do_login(self, args):
        """
        Login to the system.
        """
        url = self.url+"/login/"
        self.login(url)

    def do_logout(self, args):
        """
        Logout from the system.
        """
        url = self.url+"/logout/"
        resp = self.session.get(url)._content.decode()
        print(resp)

    def do_list(self, args):
        """
        List all modules.
        """
        url = self.url+"/list_modules/"
        r = self.session.get(url)._content.decode()
        if (r == "You are not logged in"):
            print(r)
        else:
            data = json.loads(r)
            table = PrettyTable(
                ["Code", "Name", "Year", "Semester", "Taught by"])
            for m in data["modules"]:
                teacher = ''
                for i in range(len(m["module_professor"])):
                    teacher = teacher + \
                        (m["professor_id"][i]+", Professor " +
                            m["module_professor"][i])+"\n"
                table.add_row([m["module_id"], m["module_name"],
                                m["module_year"], m["module_semester"], teacher])
            print(table)

    def do_view(self, args):
        """
        View a user's profile.
        """
        url = self.url+"/view/"
        resp = self.session.get(url)._content.decode()
        if (resp == "You are not logged in"):
            print(resp)
        else:
            data = json.loads(resp)
            for prof in data:
                if (prof["average_rating"] == None):
                    print("No rating for "+prof["professor_name"])
                else:
                    print("The rating of Professor "+prof["professor_name"]+"("+prof["professor_id"]+") is "+ "*"*int(prof["average_rating"]))

    def do_average(self, args):
        """
        Calculate the average of a user's ratings.
        """
        url = self.url+"/average/"
        args = args.split()
        if len(args) == 2:
            professor_id = args[0]
            module_code = args[1]
            user_data = {"professor_id": professor_id, "module_code": module_code}
            resp = self.session.post(url=url, json=user_data)._content.decode()
            if (resp == "You are not logged in"):
                print(resp)
            else:
                data = json.loads(resp)
                if data["rating"] == None:
                    print("No rating for "+data["professor_name"])
                else:
                    print("The rating of Professor "+data["professor_name"]+"("+data["professor_id"]+") in module "+ data["module_name"]+"("+data["module_code"]+") is "+ "*"*int(data["rating"]))
        else:
            print("Wrong arguments!")

    def do_rate(self, args):
        """
        Rate a user.
        """
        url = self.url+"/rating/"
        args = args.split()
        if len(args) == 5:
            professor_id = args[0]
            module_code = args[1]
            year = args[2]
            semester = args[3]
            rating = args[4]
            rate_data = {"user_id": self.cookie,"professor_id": professor_id, "module_code": module_code,
                            "year": year, "semester": semester, "rating": rating}
            resp = self.session.post(url, json=rate_data)._content.decode()
            print(resp)
        else:
            print("Wrong arguments!")

    def do_exit(self, args):
        """
        Exit the program.
        """
        print("Bye!")
        sys.exit()


if __name__ == "__main__":
    cli = client()
    cli.cmdloop()
