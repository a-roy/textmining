class GradeItem(object):
    """ One data entry: 1 course taken by 1 student in 1 semester.
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
        self.entry_hash = self.__hash_entry()

    def get_period(self):
        return self.period

    def set_period(self, period):
        self.period = period
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
        if not (type(self.period) is str and len(self.period) > 0):
            test.append("period")
        if not (type(self.activity) is int and len(self.activity) > 0):
            test.append("activity")
        if not (type(self.partial) is int and len(self.partial) > 0):
            test.append("partial")
        if not (type(self.semester) in (1, 2)):
            test.append("semester")
        if not (type(self.status) is str and len(self.status) > 0):
            test.append("status")
        if not (type(self.faculty) is str and len(self.faculty) > 0):
            test.append("faculty")
        if not (type(self.course_nr) is str and len(self.course_nr) = 6):
            test.append("course_nr")
        if not (type(self.course_acc) is bool):
            test.append("course_acc")
        if not (type(self.course_hum) is bool):
            test.append("course_hum")
        if not (type(self.course_ssc) is bool):
            test.append("course_ssc")
        if not (type(self.course_sci) is bool):
            test.append("course_sci")
        if not (type(self.course_title) is str and len(self.course_title) > 0):
            test.append("course_title")
        if not (type(self.grade) is int and
                (self.grade = 0 or 3 <= self.grade <= 14)):
            test.append("grade")
        if not (type(self.subplan) is str and len(self.subplan) > 0):
            test.append("subplan")

        if len(test) > 0:
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
        """ Hashes the data entry. Disregards self.entry_id and self.corruption.
        """

        import hashlib

        elements = (self.name, self.period, self.activity, self.partial,
                    self.semester, self.status, self.faculty, self.course_nr,
                    self.course_acc, self.course_hum, self.course_ssc,
                    self.course_sci, self.course_title, self.grade,
                    self.subplan)

        hashes = ''.join(hashlib.md5(e.encode()).hexdigest() for e in elements)
        return hashlib.md5(hashes.encode()).hexdigest()
