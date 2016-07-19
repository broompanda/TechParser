import linecache
import TrackFile2
from optparse import OptionParser
import os

"""This class object parses the show-tech file for show commands and indexes them.
It also defines method for parsing the show-tech file for a specific command.
"""


class FileChar(object):
    def __init__(self, file_name):
        self.file_name = file_name  # show-tech file name
        self.show_index_lines = {}  # Dictionary with show commands and line number as key-value pairs
        self.show_index = []        # List with line numbers of all show commands in ascending order
        self.get_show_indexes()     # Function call to populate show_index_lines and show_index

    def get_show_indexes(self):
        """ Creates a dictionary with the show commands and line number as key-value pairs.
        Also creates a list with the line numbers in order to maintain a sorted reference
        """
        file_obj = open(self.file_name, "r")

        for num, lines in enumerate(file_obj, 1):  # Find all lines which contain "-------- show"
            if "-------- show" in lines or "-------- bash" in lines :
                self.show_index_lines[lines] = num
                self.show_index.append(num)

    def find_output_indexes(self, search_text):
        """
        :param search_text: String to be searched in the show-tech file. Ex: "show run"
        :return: Corresponding line number obtained by parsing the dictionary created in get_show_indexes
        """
        for lines in self.show_index_lines:
            if search_text in lines:
                return self.show_index_lines[lines]
        else:
            return -1

    def print_between(self, start_index, stop_index):
        """
        Prints part of the show-tech file between 2 line numbers.
        :param start_index: Starting line-number
        :param stop_index: Ending line-number
        :return: Prints the specified lines to console
        """
        for i in range(start_index, stop_index):
            print (linecache.getline(self.file_name, i)[:-1])

    def find_similar_commands(self, search_text):
        """
        Finds all commands which start with the search_text
        :param search_text:String to be searched in the show-tech file. Ex: "show run"
        :return:
        """
        similar_commands={}
        disp_count=1
        for line in self.show_index_lines:
            if search_text in line:
                print str(disp_count) + ": " +str(line)
                similar_commands[disp_count]=line
                disp_count+=1
        if disp_count==1:
            return search_text
        else:
            selection=input("Enter the desired command number: ")
            if int(selection)<=len(similar_commands):
                return similar_commands[int(selection)]
            else:
                print"Incorrect value entered. Exiting....."
                exit()

def find_better_search(search_text):
    swap_commands = {"show ip route":"show ip route detail"}
    print search_text
    if search_text in swap_commands:
        return swap_commands[search_text]
    else:
        return search_text

def format_output():
    pass

def get_show(list_similar, print_all, args, opts):
    """ Takes the search string entered as arguments to the function call, creates a polished search string, parses
     the show-tech for the corresponding terms and displays the output.

    :return:Calls the print_between function to display the required output.
    """
    search_text = ""
    tf = TrackFile2.TrackFile()
    if len(args)>=1:
        if args[0].isdigit():
            tech_file_number = int(args[0])
            file_name = tf.get_tech_file(tech_file_number)  # Gets show-tech file corresponding to the file-number.
        else:
            print "The show-tech file number entered is incorrect"
            exit()
        if file_name == -1:
            print "Tech-support not found for file number: " + str(tech_file_number)
            exit()
        elif os.path.exists(file_name.rstrip()):
            trs = FileChar(file_name)
            if print_all:
                command = "cat "+str(file_name)
                os.system(command )
                exit()
            elif (len(args) > 1):  # Check if there are at least 2 arguments. sys.argv considers function call as 1 argument.
                for x in args[1:]:
                    word = swap_terms(x)  # Replace shortened terms with the expanded words.
                    search_text = search_text + " " + word
                search_text = find_better_search(search_text.strip())
                if list_similar:
                    search_text=trs.find_similar_commands(search_text)
                search_text_index = trs.find_output_indexes(search_text)
                if search_text_index != -1:
                    start_index = search_text_index
                    stop_index = trs.show_index[trs.show_index.index(search_text_index) + 1]
                    trs.print_between(start_index, stop_index)
                else:
                    print "No match found for '" +str(search_text) + "'"
        else:
            print "The show-tech " + file_name + " does not exist"
            exit()

    else:
        print "The number of arguments if invalid. Please try again"
        exit()

# Add shortened search terms to the end of the dictionary to customize the tool as per your favorite search patterns
swap_words = {"sh": "show", "sho": "show", "int": "interface", "br": "brief", "ro": "route", "ver": "version",
              "nei": "neighbor"}



def swap_terms(word):
    """
    Replaces shortened search terms with the expanded terms as per the swap_words dictionary created
    :param word: Shortened string to be replaced
    :return: Corresponding word from dictionary if it exists, else return original word
    """
    if word in swap_words:
        return swap_words[word]
    else:
        return word


def main():

    desc ="Tool to parse show-tech files"
    parser=OptionParser(usage="usage: %prog [flags] file_number search_string", description= desc,
                          version="%prog 1.0")

    list_desc = "List all possible commands containing the search terms. Usage: gt -l file_number search_string"
    parser.add_option("-l", "--list",
                      action="store_true",
                      dest="list_similar",
                      default=False,
                      help=list_desc)

    parser.add_option("-c", "--cat",
                      action="store_true",
                      dest="print_all",
                      default=False,
                      help="Prints entire show-tech file. Any other flag used with this option will be invalid.")

    parser.add_option("-d", "--dummy",
                      action="store_true",
                      dest="test",
                      default=False,
                      help="Print entire file")


    (opts,args) = parser.parse_args()

    get_show(opts.list_similar, opts.print_all, args, opts)


if __name__ == "__main__":
    main()
