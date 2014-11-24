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
        if not (type(self.semester) in [1, 2]):
            test.append("semester")
        if not (type(self.period) in ['main', 'intensive']):
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
