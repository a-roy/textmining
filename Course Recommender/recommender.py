class Recommender(object):
    """ AUC Course Recommender. Initialize with Recommender('name') where 'name'
        is the name by which you want to identify the Recommender object.
    """

    def __init__(self, name):
        self.name = name
        self.grade_data = [] # list of GradeItem objects
        self.grade_entries = {} # dict with ids and names
        self.course_data = [] # list of CourseItem objects
        self.course_entries = {} # dict with ids course titles

    def import_grades(self, filepath = None, anonymize = True):
        """ Import grade data into the recommender.
            Supports Excel and CSV files.
            If no filepath is supplied, calls self.__load_grades().
            If filepath is referring to a directory import all Excel and CSV
            files from that directory.
        """

        if not filepath:
            self.__load_grades()
        else:
            from os.path import isfile, isdir
            files = []
            if isdir(filepath):
                from os import listdir
                # Find all Excel and CSV files in the directory at filepath
                for file in listdir(filepath):
                    if (file.endswith(".xls") or file.endswith(".xlsx")
                        or file.endswith(".csv")):
                        files.append(filepath + "/" + file)
                if files == []:
                    raise Exception("No importable files in supplied directory")

            elif isfile(filepath):
                if (filepath.endswith(".xls") or filepath.endswith(".xlsx")
                    or filepath.endswith(".csv")):
                    files.append(filepath)
                else:
                    raise Exception("Incompatible file supplied")

            else:
                raise Exception("Incorrect path supplied")

            # Import all files
            for file in files:
                if file.endswith(".csv"):
                    self.__import_grades_csv(file)
                elif file.endswith(".xls") or file.endswith(".xlsx"):
                    self.__import_grades_excel(file)

            if anonymize:
                self.anonymize_grades()

            self.__dedupe_grades()
            self.__create_grade_entries()
            self.__save_grades()

    def __save_grades(self, filepath = None):
        """ Saves the grades to a pickle file at the specified filepath.
        """
        print "Saving grades..."

        import pickle

        if not filepath:
            filepath = self.name +  '.grade_data'

        pickle.dump([self.grade_data, self.grade_entries], open(filepath, "wb"))

        print "Grades saved to '", filepath, "'."
        print

    def __load_grades(self, filepath = None):
        """ Loads the grades to a pickle file at the specified filepath.
            If no path is supplied, will load from name.grade_data where
            name is the value of self.name
        """
        print "Loading grades..."

        import pickle

        if not filepath:
            filepath = self.name +  '.grade_data'

        both = pickle.load(open(filepath, "rb"))
        self.grade_data = both[0]
        self.grade_entries = both[1]

        print "Grades loaded from'", filepath, "'."
        print

    def __import_grades_csv(self, filepath):
        """ Import grade data into the recommender from CSV.
        """
        print "Starting CSV import..."

        raise NotImplementedError("CSV import is not ready yet; try Excel")

    def __import_grades_excel(self, filepath):
        """ Import grade data into the recommender from Excel.
            Expects the data in the first sheet of a .xls or .xlsx file.
        """
        print "Starting Excel import..."

        import xlrd

        workbook = xlrd.open_workbook(filepath)
        worksheet = workbook.sheet_by_index(0)

        assert worksheet.ncols == 11

        for row in xrange(1, worksheet.nrows):
            e = []
            for col in xrange(11):
                e.append(worksheet.cell_value(row, col))
            if not (e[9] == "" or e[9] == "NA"):
                item = GradeItem(row, e[0], e[1], e[2], e[3], e[4], e[5], e[6],
                                 e[7], e[8], e[9], e[10])
                self.grade_data.append(item)

        print "Successfully imported", str(worksheet.nrows - 1), "rows."
        print

    def anonymize_grades(self, seed = "+16", filepath = None):
        """ Anonymize the imported grade data. Use seed to enable lookup of
            names. Seed can be an alphanumeric string that initializes a
            specific hashing order or an integer specifying the length of a new
            random seed preceded by '+'. Seed is saved at filepath.
        """
        print "Starting the anonymization..."

        import random

        # if no seed is supplied, create and save one for future use
        if seed.startswith("+"):
            length = seed[1:]
            if not length.isdigit():
                raise TypeError("The supplied length is not a valid digit")
            else:
                length = int(length)
            seed = self.__get_seed(length)
            if not filepath:
                filepath = self.name + '.grade_seeds'
            # write the new seed to a file
            with open(filepath, 'a') as out:
                out.write(self.name + ': ' + seed + '\n')

        self.__shuffle(seed)

        print "Data successfully anonymized."
        print


    def __get_seed(self, length):
        """ Generate a random alphanumeric seed of the given length.
        """
        import random
        import string

        rand = random.SystemRandom()
        chars = string.letters + string.digits
        key = ''.join(rand.choice(chars) for _ in xrange(length))
        return key

    def __shuffle(self, key):
        """ Does the actual data anoymization based on a given key.
        """
        import hashlib

        for entry in self.grade_data:
            name = entry.get_name()
            hashed_name = hashlib.md5(name.encode()).hexdigest()
            base = hashed_name + key
            hashed_base = hashlib.sha1(base.encode()).hexdigest()
            entry.set_name(hashed_base)

    def __create_grade_entries(self):
        """ Populates self.grade_entries().
        """
        for entry in self.grade_data:
            num_id = entry.get_entry_id()
            name = entry.get_name()
            self.grade_entries[num_id] = name

    def __dedupe_grades(self):
        """ Hash each grade data entry and remove the duplicates.
        """
        print "Starting deduplication..."

        hashes = []
        dupes = []

        for i in xrange(len(self.grade_data)):
            h = self.grade_data[i].get_entry_hash()
            if not h in hashes:
                hashes.append(h)
            else:
                dupes.append(i)

        if len(dupes) == 0:
            print "No duplicates found."
        else:
            for i in xrange(len(dupes)):
                del self.grade_data[dupes[i] - i]
            print str(len(dupes)), "duplicates removed."
        print
