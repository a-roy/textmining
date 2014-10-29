class CourseItem(object):
    """ One course desciption: 1 course given in 1 year.
    """

    def __init__(self, course_id = "", title = "", year = 0,
                 ecp = 0, theme = "", track = "", prereqs = "",
                 description = ""):
        self.entry_id = None # string or None
        self.nr = self.__convert_id(id, 'nr') # string
        self.acc = self.__convert_id(id, 'acc') # Boolean
        self.hum = self.__convert_id(id, 'hum') # Boolean
        self.ssc = self.__convert_id(id, 'ssc') # Boolean
        self.sci = self.__convert_id(id, 'sci') # Boolean
        self.title = title # string
        self.year = int(year) # int
        self.ecp = int(ecp) # int
        self.theme = theme # string
        self.track = track # string
        self.prereq_text = prereqs # string
        self.prereq_courses = [] # list
        self.description_text = description # string
        self.description_words = {} # dict (FreqDict)
        self.corruption = self.__check_integrity() # Boolean
        self.entry_hash = self.__hash_entry() # string

    def get_entry_id(self):
        return self.entry_id

    def set_entry_id(self, entry_id):
        self.entry_id = entry_id

    def get_nr(self):
        return self.nr

    def set_nr(self, nr):
        self.nr = nr
        self.entry_hash = self.__hash_entry()

    def get_acc(self):
        return self.acc

    def set_acc(self, acc):
        self.acc = acc
        self.entry_hash = self.__hash_entry()

    def get_hum(self):
        return self.hum

    def set_hum(self, hum):
        self.hum = hum
        self.entry_hash = self.__hash_entry()

    def get_ssc(self):
        return self.ssc

    def set_ssc(self, ssc):
        self.ssc = ssc
        self.entry_hash = self.__hash_entry()

    def get_sci(self):
        return self.sci

    def set_sci(self, sci):
        self.sci = sci
        self.entry_hash = self.__hash_entry()

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title
        self.entry_hash = self.__hash_entry()

    def get_year(self):
        return self.year

    def set_year(self, year):
        self.year = year
        self.entry_hash = self.__hash_entry()

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        self.entry_hash = self.__hash_entry()

    def get_ecp(self):
        return self.ecp

    def set_ecp(self, ecp):
        self.ecp = ecp
        self.entry_hash = self.__hash_entry()

    def get_theme(self):
        return self.theme

    def set_theme(self, theme):
        self.theme = theme
        self.entry_hash = self.__hash_entry()

    def get_track(self):
        return self.track

    def set_track(self, track):
        self.track = track
        self.entry_hash = self.__hash_entry()

    def get_prereq_text(self):
        return self.prereq_text

    def set_prereq_text(self, prereq_text):
        self.prereq_text = prereq_text
        self.entry_hash = self.__hash_entry()

    def get_prereq_courses(self):
        return self.prereq_courses

    def set_prereq_courses(self, prereq_courses):
        self.prereq_courses = prereq_courses
        self.entry_hash = self.__hash_entry()

    def get_description_text(self):
        return self.description_text

    def set_description_text(self, description_text):
        self.description_text = description_text
        self.entry_hash = self.__hash_entry()

    def get_description_words(self):
        return self.description_words

    def set_description_words(self, description_words):
        self.description_words = description_words
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
    if not (type(self.title) is str and len(self.title) > 0):
        test.append("title")
    if not (type(self.year) is str and 2009 < self.year < 2050:
        test.append("year")
    if not (type(self.ecp) is str and 0 < self.ecp < 18:
        test.append("ecp")
    if not (type(self.theme) is str and len(self.theme) > 0):
        test.append("theme")
    if not (type(self.track) is str and len(self.track) > 0):
        test.append("track")
    if not (type(self.prereq_text) is str and len(self.prereq_text) > 0):
        test.append("prereq_text")
    if not (type(self.prereq_courses) is list:
        test.append("prereq_courses")
    if not (type(self.description_text) is str and
            len(self.description_text) > 0):
        test.append("description_text")
    if not (type(self.description_words) is dict:
        test.append("description_words")

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
