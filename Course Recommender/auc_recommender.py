class RecommenderData(object):
    """ One data entry for the AUC Course Recommender.
    """

    def __init__(self, name = "", period = "", activity = 0, partial = 0,
                 semester = 0, status = "", faculty = "", course_id = "",
                 course_title = "", lettergrade = "", subplan = ""):
        self.entry_id = None
        self.name = name
        self.period = period
        self.activity = int(activity)
        self.partial = int(partial)
        self.semester = int(semester[1])
        self.status = status
        self.faculty = faculty
        self.course_nr = self.__convert_course_id(course_id, 'nr')
        self.course_acc = self.__convert_course_id(course_id, 'acc')
        self.course_hum = self.__convert_course_id(course_id, 'hum')
        self.course_ssc = self.__convert_course_id(course_id, 'ssc')
        self.course_sci = self.__convert_course_id(course_id, 'sci')
        self.course_title = course_title
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

    def get_period(self):
        return self.period

    def set_period(self, period):
        self.period = period

    def get_activity(self):
        return self.activity

    def set_activity(self, activity):
        self.activity = activity

    def get_partial(self):
        return self.partial

    def set_partial(self, partial):
        self.partial = partial

    def get_semester(self):
        return self.semester

    def set_semester(self, semester):
        self.semester = semester

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_faculty(self):
        return self.faculty

    def set_faculty(self, faculty):
        self.faculty = faculty

    def get_course_nr(self):
        return self.course_nr

    def set_course_nr(self, course_nr):
        self.course_nr = course_nr

    def get_course_acc(self):
        return self.course_acc

    def set_course_acc(self, course_acc):
        self.course_acc = course_acc

    def get_course_hum(self):
        return self.course_hum

    def set_course_hum(self, course_hum):
        self.course_hum = course_hum

    def get_course_ssc(self):
        return self.course_ssc

    def set_course_ssc(self, course_ssc):
        self.course_ssc = course_ssc

    def get_course_sci(self):
        return self.course_sci

    def set_course_sci(self, course_sci):
        self.course_sci = course_sci

    def get_coursetitle(self):
        return self.course_title

    def set_coursetitle(self, course_title):
        self.course_title = course_title

    def get_grade(self):
        return self.grade

    def set_grade(self, grade):
        self.grade = grade

    def get_subplan(self):
        return self.subplan

    def set_subplan(self, subplan):
        self.subplan = subplan

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

        test = [self.name, []]

        if not (type(self.name) is str and len(self.name) > 0):
            test[1].append("name")
        if not (type(self.period) is str and len(self.period) > 0):
            test[1].append("period")
        if not (type(self.activity) is int and len(self.activity) > 0):
            test[1].append("activity")
        if not (type(self.partial) is int and len(self.partial) > 0):
            test[1].append("partial")
        if not (type(self.semester) in (1, 2)):
            test[1].append("semester")
        if not (type(self.status) is str and len(self.status) > 0):
            test[1].append("status")
        if not (type(self.faculty) is str and len(self.faculty) > 0):
            test[1].append("faculty")
        if not (type(self.course_nr) is str and len(self.course_nr) = 6):
            test[1].append("course_nr")
        if not (type(self.course_acc) is bool):
            test[1].append("course_acc")
        if not (type(self.course_hum) is bool):
            test[1].append("course_hum")
        if not (type(self.course_ssc) is bool):
            test[1].append("course_ssc")
        if not (type(self.course_sci) is bool):
            test[1].append("course_sci")
        if not (type(self.course_title) is str and len(self.course_title) > 0):
            test[1].append("course_title")
        if not (type(self.grade) is int and
                (self.grade = 0 or 3 <= self.grade <= 14)):
            test[1].append("grade")
        if not (type(self.subplan) is str and len(self.subplan) > 0):
            test[1].append("subplan")

        if len(test[1]) > 0:
            return test
        else:
            return None

    def __convert_course_id(self, course_id, element):
        """ Takes a course id and extracts either the nr or a bool for the type.
        """

        if element is "nr":
            return course_id[:6]

        else:
            return element in course_id.lower()

    def __convert_grade(self, letter_grade):
        """ Convert a letter grade to a numerical grade between 0 and 14.
            F = 0, D- = 3, D = 4, D+ = 5, ..., A = 13, A+ = 14
            This representation is chosen for easier learning.
        """

        grades = ["F", "F", "F", "D-", "D", "D+", "C-", "C", "C+", "B-", "B",
                  "B+", "A-", "A", "A+"]

        return float(grades.find(letter_grade))

    def __hash_entry(self):
        """ Hashes the data entry. Disregards self.entry_id.
        """

        import hashlib

        elements = (self.name, self.period, self.activity, self.partial,
                    self.semester, self.status, self.faculty, self.course_nr,
                    self.course_acc, self.course_hum, self.course_ssc,
                    self.course_sci, self.course_title, self.grade,
                    self.subplan)

        hashes = ''.join(hashlib.md5(e.encode()).hexdigest() for e in elements)
        return hashlib.md5(hashes.encode()).hexdigest()

---------------------------------------------------------------------------------------------------------------------------------------------------------

class Recommender(object):
    """ AUC Course Recommender.
    """

    def __init__(self, name, filepath = None, anonymize = False):
        self.name = name
        self.data = [] # list of RecommenderData objects
        self.entries = {} # dict with ids and names of entries

        if filepath is not None:
            self.import_data(filepath, anonymize)

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
            self.data.append(RecommenderData(e[0], e[1], e[2], e[3], e[4], e[5],
                                             e[6], e[7], e[8], e[9], e[10]))

        print "Successfully imported", str(worksheet.nrows - 1), "rows."

    def __dedupe(self):
        """ Hash each data entry and remove the duplicates.
        """
        pass
        # -----------------------------------------------------------------------------------------------------------------

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
            with open('recommenderdata.seeds', 'a') as out:
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
