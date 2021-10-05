class Employee:
    raise_amt = 1.04

    def __init__(self, first, last, pay):
        print ('sdfasdfsd')
        self.first = first
        self.last = last
        self.email = first + '.' + last + '@company.com'
        self.pay = pay

    def raise_pay(self):
        self.pay = int(self.pay * self.raise_amt)

    @classmethod
    def update_raise_Amt(cls, new_raise_amt):
        cls.raise_amt = new_raise_amt

    def fullname(self):
        return self.first + ' ' + self.last

    def __init__(self, emp_string):
        self.first, self.last, self.pay = emp_string.split('-')

class Developer(Employee):
    raise_amt = 1.10

    def __init__(self, first, last, pay, lang):
        super().__init__(first, last, pay)
        self.lang = lang

class Manager(Employee):

    def __init__(self, first, last, pay, employees = None):
        super().__init__(first, last, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)

    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)

    def print_emps(self):
        for emp in self.employees:
            print('-->', emp.fullname(), '-->', emp.pay)

#dev1 = Employee('Vijaya', 'kumari', 50000)
#dev2 = Employee('Ravi', 'Prakash', 50000)
dev3 = Employee('Pitty-Lakshya-30000')

print (dev3.fullname())

