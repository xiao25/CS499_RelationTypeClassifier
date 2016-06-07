import cmd
import search
import time
import math
__author__ = 'ztx'

#TODO: refine raw data to get better result

class MyCmdInterpreter(cmd.Cmd):
    """use extend cmd object to implement Text UI"""
    intro = 'Welcome to the query system. Type help or ? to list commands.\n'

    def __init__(self):
        cmd.Cmd.__init__(self)








    def do_search(self,query_str):
        start = time.time()
        parts = query_str.split(" ")
        entity1 = parts[0][1:]
        entity2 = parts[1][1:]


        result = search.search_function(entity1.lower(),entity2.lower())
        if(result == -1):
            print("Sorry, no result found under current data")
        else:
            print("Rank Relationship RankScore TFScore PostionScore FullPhrase")
            for i in xrange(len(result)):
                item = result[i]
                print(str(i+1)+". %s %s"%(item[0],item[1]))

            end = time.time()
            print('Time spent on search:\t%fs'% math.fabs(end - start))






    def help_search(self):
        print('please type query format as type #entity such as:search #headache #aspirin')

    def do_exit(self, s):
        """Exit the system"""
        print('Thank you for using this query system!')
        return True


interpreter = MyCmdInterpreter()
interpreter.cmdloop()
