import linecache
import TrackFile2
from optparse import OptionParser
import os
import tempfile
import subprocess
import TweakOutput
import filterplatformcounters

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
    swap_commands = {"show ip route":"show ip route detail", "show interface":"show interfaces --"}
    print search_text
    if search_text in swap_commands:
        return swap_commands[search_text]
    else:
        return search_text

def truncate_command_output(command_to_truncate,tech_file_number):
    reducible_commands=["show lldp neighbors", "show ip interface"]
    for command in reducible_commands:
        if command_to_truncate in command:
            command_output = gettempoutput(tech_file_number, command)
            if command == "show lldp neighbors":
                TweakOutput.tweaklldp(command_output)
                exit()
            if command == "show ip interface":
                TweakOutput.tweakipint(command_output)
                exit()
    
    print "Cannot truncate this command's output. Displaying complete output"
    return


def get_show(args, opts):
    """ Takes the search string entered as arguments to the function call, creates a polished search string, parses
     the show-tech for the corresponding terms and displays the output.

    :return:Calls the print_between function to display the required output.
    """
    if not opts.show_differences:

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
                if opts.print_all:
                    command = "cat "+str(file_name)
                    os.system(command )
                    exit()

                elif (len(args) > 0):  # Check if there are at least 2 arguments. sys.argv considers function call as 1 argument.
                    for x in args[1:]:
                        word = swap_terms(x)  # Replace shortened terms with the expanded words.
                        search_text = search_text + " " + word
                    search_text = find_better_search(search_text.strip())
                    if opts.list_similar:
                        search_text=trs.find_similar_commands(search_text)
                    search_text_index = trs.find_output_indexes(search_text)
                    if opts.show_brief:
                        truncate_command_output(search_text, tech_file_number)
                    if opts.analyze_tech_support:
                        analyze_tech_support(tech_file_number)
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
    else:
        find_differences(args)

# Add shortened search terms to the end of the dictionary to customize the tool as per your favorite search patterns
swap_words = {"sh": "show", "sho": "show", "int": "interface", "br": "brief", "ro": "route", "ver": "version",
              "nei": "neighbor"}

def find_differences(args):
    if len(args)>=1:
        file_numbers=args[0].split(',')
    first_tech_file_number=file_numbers[0]
    second_tech_file_number=file_numbers[1]
    common_command=""
    for word in args[1:]:
        common_command=common_command + " " + word
    try:
        file1=gettempoutput(first_tech_file_number, common_command)
        file2=gettempoutput(second_tech_file_number, common_command)
        vim_command="vimdiff " + file1.name + " " + file2.name
        os.system(vim_command)
    finally:
        # Automatically cleans up the file
        file1.close()
        file2.close()


def gettempoutput(tech_file_number, command):
        """
        :param tech_file_number: Show tech file number where command needs to be executed
        :param command: Command to be executed
        :return: Temporary file object with output of 'command'
        """
        temp_file=tempfile.NamedTemporaryFile()
        command="python  " + __file__ + " " +  str(tech_file_number) + " " + command
        print command
        proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
        (output, err) = proc.communicate()
        temp_file.write(str(output))
        temp_file.seek(0)
        return temp_file


def analyze_tech_support(tech_file_number):
    print ("""What would like to analyze in the tech-support?
    1. Platform fap counters
    2. Platform interrupts""")
    selection=raw_input("Please Select: ")

    if selection == '1':
        analyze_platform_fap(tech_file_number)
    elif selection == '2':
        analyze_platform_interrupts(tech_file_number)
    else:
        exit()

def analyze_platform_fap(tech_file_number):

    clock_output = gettempoutput(tech_file_number, "show clock")
    platform_cnt_output = gettempoutput(tech_file_number, "'show platform fap counters | nz'")
    filterplatformcounters.filter(platform_cnt_output.name, clock_output.name)
    exit()

def analyze_platform_interrupts(tech_file_number):
    pass

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


    tool_desc ="Tool to parse show-tech files"
    parser=OptionParser(usage="usage: %prog [flags] file_number search_string", description= tool_desc,
                          version="%prog 1.0")

    list_desc = "List all possible commands containing the search terms. Usage: gt -l <file_number> <search_string>"
    diff_desc = "Shows the difference between outputs for the same command across 2 different show-tech files. Usage: gt -d <file_number1>,<file_number2> <search_string>"
    cat_desc =  "Prints entire show-tech file. Usage: gt -c <file_number1>"
    brief_desc = "Print brief format of selected output, if available"
    analyze_desc="Analyze the show-tech"
    parser.add_option("-l", "--list",
                      action="store_true",
                      dest="list_similar",
                      default=False,
                      help=list_desc)

    parser.add_option("-c", "--cat",
                      action="store_true",
                      dest="print_all",
                      default=False,
                      help=cat_desc)

    parser.add_option("-d", "--diff",
                      action="store_true",
                      dest="show_differences",
                      default=False,
                      help=diff_desc)

    parser.add_option("-b", "--brief",
                      action="store_true",
                      dest="show_brief",
                      default=False,
                      help=brief_desc)

    parser.add_option("-a", "--analyze",
                      action="store_true",
                      dest="analyze_tech_support",
                      default=False,
                      help=analyze_desc)


    (opts,args) = parser.parse_args()

    get_show(args, opts)


if __name__ == "__main__":
    main()
