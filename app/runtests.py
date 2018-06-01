from subprocess import call
import organization
import sys, inspect
tests_to_run = []
params = []
def choose_arguments():
    print("\nToo few arguments. You can use : \n\n -all : to run all mezzo tests\n -mezzanine : to run only mezzanine tests")
    print(" -agenda : to run mezzanine-agenda tests \n -organization : to run mezzanine-organization tests\n -cartridge : to run cartridge tests ")
    print(" --front : to run only front tests \n --back : to run only back tests \n [PATH] = to run a test yourself")
    print("\n You can also use all manage.py options ( as --failfast)")
    return input("\n'yes' to run all tests, 'no' to cancel : ")

def execute():
    for test in tests_to_run:
        print("\n\n****" + test + "****")
        call(["python", "manage.py","test" , test , "--keepdb", "--liveserver=app:8082"] + params)

def add_all_tests():
    tests_to_run.append("/srv/lib/mezzanine-agenda")
    tests_to_run.append("/srv/lib/mezzanine")
    tests_to_run.append("/srv/lib/mezzanine-organization")
    tests_to_run.append("/srv/lib/cartridge")

def bad_arguments():
    if choose_arguments()=='yes':
        add_all_tests()
    else:
        sys.exit()

if len(sys.argv)==1:
    bad_arguments()
else:
    for arg in sys.argv:
        if "--front" in arg:
            params.append("--pattern=*front.py")
        elif "--back" in arg:
            params.append("--pattern=*back.py")
        elif arg == "-all":
            add_all_tests()
        elif "/" in arg:
            tests_to_run.append(arg) 
        elif arg == "-agenda":
            tests_to_run.append("/srv/lib/mezzanine-agenda")
        elif arg == "-mezzanine":
            tests_to_run.append("/srv/lib/mezzanine")
        elif arg == "-organization":
            tests_to_run.append("/srv/lib/mezzanine-organization")
        elif arg == "-cartridge":
            tests_to_run.append("/srv/lib/cartridge")
        elif "-" in arg:
            params.append(arg)
        elif arg!= "runtests.py":
            tests_to_run.append(arg)
        
if len(tests_to_run)>0:
    execute()
else:
    print("You have to specify a test suite")    


# All : python manage.py test /srv/lib/cartridge /srv/lib/mezzanine /srv/lib/mezzanine-agenda /srv/lib/mezzanine-organization --keepdb
# example above does not work for a strange reason  

# Cartridge : python manage.py test /srv/lib/cartridge --keepdb
# Mezzanine : python managy.py test /srv/lib/mezzanine --keepdb
# Mezzanine-agenda : python manage.py test /srv/lib/mezzanine-agenda --keepdb
# Mezzanine-organization : python manage.py test /srv/lib/mezzanine-organization --keepdb