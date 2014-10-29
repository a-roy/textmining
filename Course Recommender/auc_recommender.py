class Recommender(object):
    """ AUC Course Recommender.
    """

    def __init__(self, name):
        self.name = name
        self.grade_data = [] # list of GradeItem objects
        self.grade_entries = {} # dict with ids and names
        self.course_data = [] # list of CourseItem objects
        self.course_entries = {} # dict with ids course titles

    def import_data(self, filepath, anonymize = True):
        """ Import data into the recommender. Supports Excel and  CSV files.
        """
        if filepath.endswith(".csv"):
            print "Starting CSV import..."
            self.__import_csv(filepath)
        elif filepath.endswith(".xls") or filepath.endswith(".xlsx"):
            print "Starting Excel import..."
            self.__import_excel(filepath)
        else:
            raise Exception("Wrong path or filetype")

        print "Data successfully imported"

        if anonymize:
            self.anonymize_data()

        self.entries = self.__dedupe()

    def __import_csv(self, filepath):
        """ Import data into the recommender from CSV.
        """

        raise NotImplementedError("CSV import is not ready yet; try Excel")

    def __import_excel(self, filepath):
        """ Import data into the recommender from Excel.
            Expects the data in the first sheet of a .xls or .xlsx file.
        """
        import xlrd

        workbook = xlrd.open_workbook(filepath)
        worksheet = workbook.sheet_by_index(0)

        assert worksheet.ncols == 11

        for row in xrange(1, worksheet.nrows):
            e = []
            for col in xrange(11):
                e.append(worksheet.cell_value(row, col))
            self.data.append(GradeItem(e[0], e[1], e[2], e[3], e[4], e[5],
                                             e[6], e[7], e[8], e[9], e[10]))

        print "Successfully imported", str(worksheet.nrows - 1), "rows."

    def __dedupe(self):
        """ Hash each data entry and remove the duplicates.
        """
        pass

    def anonymize_data(self, seed = "+16"):
        """ Anonymize the imported data. Use seed to enable lookup of names.
            Seed can be an alphanumeric string that initializes a specific
            hashing order or an integer specifying the length of a new random
            seed preceded by '+'.
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
            # write the new seed to a file
            with open('GradeItem.seeds', 'a') as out:
                out.write(self.name + ': ' + seed + '\n')

        self.__shuffle(seed)

        print "Data successfully anonymized."


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

        for entry in self.data:
            name = entry.get_name()
            hashed_name = hashlib.md5(name.encode()).hexdigest()
            base = hashed_name + key
            hashed_base = hashlib.sha1(base.encode()).hexdigest()
            entry.set_name(hashed_base)
