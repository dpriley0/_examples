#%% PROPER DOCUMENTATION
class ClassName:
    def __init__(self, param1, param2=True, **kwargs):
        """
        Description...

        Parameters
        ----------
        param1
        param2

        Parameters
        ----------
        param1 (type): Description...
        param2 (type, optional): Description...

        Returns
        -------
        None.

        """
#     """
#     {Description}

#     Attributes:
#         attribute1 (type): Description of attribute1.
#         attribute2 (type): Description of attribute2. Optional; default is X.
#         attribute3 (type): Description of attribute3.

#     Methods:
#         method1: Brief description of what method1 does.
#         method2: Brief description of what method2 does.
#     """

#         """
#         Brief summary of what the constructor does.

#         Args:
#             param1 (type): Description of param1.
#             param2 (type, optional): Description of param2. Default is X.

#         Raises:
#             ExceptionType: Condition when it’s raised.
#         """
#         # Initialize attributes here

# #%%
# class Person:
#     """__init__ & inheritance practice example"""

#     def __init__(self, name):
#         self.firstname= name.split()[0]
#         self.lastname= name.split()[1]

#     def printname(self):
#         print(self.firstname, self.lastname)


# class Student(Person):
#     def __init__(self, name, year):
#         # This by itself *overrides* the parent's __init__
#         super().__init__(name)
#         # SUPER() will have child inherit ALL
#         # of parent's attributes and methods
#         self.graduationyear= year

#     def welcome(self):
#         print(
#             f"Welcome, {self.firstname} {self.lastname}, to the class of {self.graduationyear}.")