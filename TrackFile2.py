import sys
import os
import shelve


class TrackFile(object):
    def __init__(self):
        program_dir = os.path.dirname(os.path.abspath(__file__))
        self.tracking_file_name = os.path.join(program_dir,"test_shelf")

    def add_tech_file(self, tech_file_number, tech_file_name):
        s = shelve.open(self.tracking_file_name, flag='c', writeback=True)
        try:
            s['file' + str(tech_file_number)] = {'file_name': tech_file_name}
            s.sync()
        finally:
            s.close()

    def get_tech_file(self, tech_file_number=0):
        s = shelve.open(self.tracking_file_name, flag='c')
        if tech_file_number==0:
            for file in s :
                print file + " : " + s[file]['file_name']
        else:
            try:
                tech_file_name = s['file' + str(tech_file_number)]['file_name']
            except KeyError:
                tech_file_name = -1
            finally:
                s.close()
                return tech_file_name


def parse_arguments():

    tf = TrackFile()

    if len(sys.argv) >= 3:
        tech_file_name = sys.argv[2]
        tech_file_number = sys.argv[1]
        if os.path.exists(tech_file_name):
            tf.add_tech_file(tech_file_number, tech_file_name)
        else:
            print "The show-tech " + tech_file_name + " does not exist"
            exit()
    else:
        tf.get_tech_file()




def main():
      parse_arguments()



if __name__ == "__main__":
    main()
