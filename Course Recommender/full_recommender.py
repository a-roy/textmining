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

class GradeItem(object):
    """ One data entry: 1 course taken by 1 student in 1 semester.
    """

    def __init__(self, id_num = "", name = "", period = "", activity = 0,
                 partial = 0, semester = 0, status = "", faculty = "",
                 course_id = "", course_title = "", lettergrade = "",
                 subplan = ""):
        self.entry_id = id_num
        self.name = str(name)
        self.period_num = int(period)
        self.activity = int(activity)
        self.partial = str(partial)
        self.semester = self.__convert_period(semester, 'semester')
        self.period = self.__convert_period(semester, 'period')
        self.status = str(status)
        self.faculty = str(faculty)
        self.course_nr = self.__convert_course_id(course_id, 'nr')
        self.course_acc = self.__convert_course_id(course_id, 'acc')
        self.course_cpi = self.__convert_course_id(course_id, 'cicy')
        self.course_hum = self.__convert_course_id(course_id, 'hum')
        self.course_ssc = self.__convert_course_id(course_id, 'ssc')
        self.course_sci = self.__convert_course_id(course_id, 'sci')
        self.course_title = self.__clean_course_title(course_title)
        self.grade = self.__convert_grade(lettergrade)
        self.subplan = subplan
        self.corruption = self.__check_integrity()
        self.entry_hash = self.__hash_entry()

    def get_entry_id(self):
        return self.entry_id

    def set_entry_id(self, entry_id):
        self.entry_id = entry_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        self.entry_hash = self.__hash_entry()

    def get_period_num(self):
        return self.period_num

    def set_period_num(self, period_num):
        self.period_num = period_num
        self.entry_hash = self.__hash_entry()

    def get_activity(self):
        return self.activity

    def set_activity(self, activity):
        self.activity = activity
        self.entry_hash = self.__hash_entry()

    def get_partial(self):
        return self.partial

    def set_partial(self, partial):
        self.partial = partial
        self.entry_hash = self.__hash_entry()

    def get_semester(self):
        return self.semester

    def set_semester(self, semester):
        self.semester = semester
        self.entry_hash = self.__hash_entry()

    def get_period(self):
        return self.period

    def set_period(self, period):
        self.period = period
        self.entry_hash = self.__hash_entry()

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status
        self.entry_hash = self.__hash_entry()

    def get_faculty(self):
        return self.faculty

    def set_faculty(self, faculty):
        self.faculty = faculty
        self.entry_hash = self.__hash_entry()

    def get_course_nr(self):
        return self.course_nr

    def set_course_nr(self, course_nr):
        self.course_nr = course_nr
        self.entry_hash = self.__hash_entry()

    def get_course_acc(self):
        return self.course_acc

    def set_course_acc(self, course_acc):
        self.course_acc = course_acc
        self.entry_hash = self.__hash_entry()

    def get_course_cpi(self):
        return self.course_cpi

    def set_course_cpi(self, course_cpi):
        self.course_cpi = course_cpi
        self.entry_hash = self.__hash_entry()

    def get_course_hum(self):
        return self.course_hum

    def set_course_hum(self, course_hum):
        self.course_hum = course_hum
        self.entry_hash = self.__hash_entry()

    def get_course_ssc(self):
        return self.course_ssc

    def set_course_ssc(self, course_ssc):
        self.course_ssc = course_ssc
        self.entry_hash = self.__hash_entry()

    def get_course_sci(self):
        return self.course_sci

    def set_course_sci(self, course_sci):
        self.course_sci = course_sci
        self.entry_hash = self.__hash_entry()

    def get_coursetitle(self):
        return self.course_title

    def set_coursetitle(self, course_title):
        self.course_title = course_title
        self.entry_hash = self.__hash_entry()

    def get_grade(self):
        return self.grade

    def set_grade(self, grade):
        self.grade = grade
        self.entry_hash = self.__hash_entry()

    def get_subplan(self):
        return self.subplan

    def set_subplan(self, subplan):
        self.subplan = subplan
        self.entry_hash = self.__hash_entry()

    def get_corruption(self):
        return self.corruption

    def set_corruption(self, corruption = None):
        if corruption is None:
            self.corruption = self._check_integrity()
        else:
            self.corruption = corruption

    def get_entry_hash(self):
        return self.entry_hash

    def set_entry_hash(self, entry_hash = None):
        if entry_hash is None:
            self.entry_hash = self.__hash_entry()
        else:
            self.entry_hash = entry_hash

    def __check_integrity(self):
        """ Verify integrity of the data by checking the type of every entry.
        """

        test = []

        if not (type(self.name) is str and len(self.name) > 0):
            test.append("name")
        if not (type(self.period_num) is int and self.period_num > 0):
            test.append("period_num")
        if not (type(self.activity) is int and self.activity > 0):
            test.append("activity")
        if not (type(self.partial) is str and len(self.partial) > 0):
            test.append("partial")
        if not (type(self.semester) in (1, 2)):
            test.append("semester")
        if not (type(self.period) in ('main', 'intensive')):
            test.append("period")
        if not (type(self.status) is str and len(self.status) > 0):
            test.append("status")
        if not (type(self.faculty) is str and len(self.faculty) > 0):
            test.append("faculty")
        if not (type(self.course_nr) is str and len(self.course_nr) == 6):
            test.append("course_nr")
        if not (type(self.course_acc) is bool):
            test.append("course_acc")
        if not (type(self.course_cpi) is bool):
            test.append("course_cpi")
        if not (type(self.course_hum) is bool):
            test.append("course_hum")
        if not (type(self.course_ssc) is bool):
            test.append("course_ssc")
        if not (type(self.course_sci) is bool):
            test.append("course_sci")
        if not (type(self.course_title) is str and
                len(self.course_title) > 0):
            test.append("course_title")
        if not (type(self.grade) is int and (0 <= self.grade <= 14)):
            test.append(''.join(["grade: ", str(self.grade)]))
        if not (type(self.subplan) is str and len(self.subplan) > 0):
            test.append("subplan")

        if len(test) > 0:
            return test
        else:
            return None

    def __convert_period(self, semester, part):
        """ Takes a semester name and splits it into actual semester and period.
        """
        if part == 'semester':
            return int(semester[1])
        elif part == 'period':
            if len(semester) == 2:
                return 'main'
            else:
                return 'intensive'
        else:
            raise ValueError('You used an incorrect string as part.')

    def __convert_course_id(self, course_id, element):
        """ Takes a course id and extracts either the nr or a bool for the type.
        """

        if element is "nr":
            return course_id[:6]

        else:
            return element in course_id.lower()

    def __clean_course_title(self, course_title):
        """ Returns the cleanede course title.
            If the supplied course title starts with '<L> ', this is removed.
        """

        if course_title.startswith('<L> '):
            return course_title[4:]
        return course_title

    def __convert_grade(self, letter_grade):
        """ Convert a letter grade to a numerical grade between 0 and 14.
            F = 0, D- = 3, D = 4, D+ = 5, ..., A = 13, A+ = 14
            This representation is chosen for easier learning.
        """


        grades = ["NA", "", "F", "F", "F", "D-", "D", "D+", "C-", "C", "C+", "B-", "B",
                  "B+", "A-", "A", "A+"]

        try:
            return float(grades.index(letter_grade) - 2)

        except ValueError:
            print "You were trying to import a grade data entry with no grade\
                   or an improperly formatted grade. Please check the data you\
                   were trying to import to spot and remove those entries."
            raise

    def __hash_entry(self):
        """ Hashes the data entry. Disregards self.entry_id and self.corruption.
        """

        import hashlib

        elements = (self.name, self.period_num, self.activity, self.partial,
                    self.semester, self.period, self.status, self.faculty,
                    self.course_nr, self.course_acc, self.course_cpi,
                    self.course_hum, self.course_ssc, self.course_sci,
                    self.course_title, self.grade, self.subplan)

        hashes = ''.join(hashlib.md5(str(e).encode()).hexdigest()
                         for e in elements)
        return hashlib.md5(hashes.encode()).hexdigest()

    def __str__(self):
        from collections import OrderedDict
        data = OrderedDict()
        data["entry_id"] = self.entry_id
        data["name"] = self.name
        data["period_num"] = self.period_num
        data["activity"] = self.activity
        data["partial"] = self.partial
        data["semester"] = self.semester
        data["period"] = self.period
        data["status"] = self.status
        data["faculty"] = self.faculty
        data["course_nr"] = self.course_nr
        data["course_acc"] = self.course_acc
        data["course_cpi"] = self.course_cpi
        data["course_hum"] = self.course_hum
        data["course_ssc"] = self.course_ssc
        data["course_sci"] = self.course_sci
        data["course_title"] = self.course_title
        data["grade"] = self.grade
        data["subplan"] = self.subplan
        data["corruption"] = self.corruption
        data["entry_hash"] = self.entry_hash
        string = ""
        for k, v in data.items():
            string = string + k + ": " + str(v) + "\n"
        return string
