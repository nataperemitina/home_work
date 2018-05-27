class Person(object):
    __slots__ = ('__firstname', '__lastname')
    def __init__(self, firstname, lastname):
        self.__lastname = lastname
        self.__firstname = firstname

    def get_full_name(self):
        return '{} {}'.format(self.get_firstname(), self.get_lastname())

    def get_firstname(self):
        return self.__firstname

    def get_lastname(self):
        return self.__lastname


class Teacher(Person):
    __slots__ = ('__pupils',)
    def __init__(self, firstname, lastname, pupils=[]):
        super().__init__(firstname, lastname)
        self.__pupils = pupils

    def add_pupil(self, pupil):
        if pupil not in self.get_pupils():
            self.get_pupils().append(pupil)

    def get_pupils(self):
        return self.__pupils

    def remove_pupil(self, pupil):
        if pupil in self.get_pupils():
            self.get_pupils().remove(pupil)

    def __repr__(self):
        return "Teacher:{0}; pupils:{1}".format(self.get_full_name(),
                                                    self.__pupils)


class Pupil(Person):
    __slots__ = ('__lessons_count', '__tasks')
    def __init__(self, firstname, lastname):
        super().__init__(firstname, lastname)
        self.__lessons_count = 0
        self.__tasks = {}

    def inc_lessons(self):
        self.__lessons_count += 1

    def get_lessons(self):
        return self.__lessons_count

    def get_tasks(self):
        return self.__tasks

    def mark_task(self, task, mark):
        self.__tasks[task] = mark

    def __repr__(self):
        return "Name:{0};lesson_count:{1};tasks:{2}".format(self.get_full_name(),
                                                            self.__lessons_count,
                                                            self.__tasks)


class Course(object):
    __slots__ = ('__theme', '__start_time', '__end_time', '__teachers',)
    def __init__(self, theme):
        self.__theme = theme
        self.__start_time = None
        self.__end_time = None
        self.__teachers = []


    def get_start_time(self):
        return self.__start_time

    def set_start_time(self, time):
        self.__start_time = time

    def get_end_time(self):
        return self.__end_time

    def set_end_time(self, time):
        self.__end_time = time

    def get_teachers(self):
        return self.__teachers

    def add_teacher(self, teacher):
        if teacher not in self.get_teachers():
            self.get_teachers().append(teacher)

    def remove_teacher(self, teacher):
        if teacher in self.get_teachers():
            self.get_teachers().remove(teacher)

    def __repr__(self):
        return "Course name:{0}; start:{1}-end:{2}; teacher:{3} ".format(self.__theme,
                                                                         self.__start_time,
                                                                         self.__end_time,
                                                                         self.__teachers)
def main():

    # define_math_course
    course_math = Course("Math")
    course_math.set_start_time("01/09/2017")
    course_math.set_end_time("01/06/2018")

    teacher_ted = Teacher("Frank", "Tailor")
    course_math.add_teacher(teacher_ted)

    pupil_alex = Pupil("Alex", "Black")
    teacher_ted.add_pupil(pupil_alex)

    pupil_jane = Pupil("Jane", "Smith")
    teacher_ted.add_pupil(pupil_jane)

    pupil_alex.mark_task("leson1", "A")
    pupil_alex.mark_task("leson2", "C")
    pupil_alex.inc_lessons()
    pupil_alex.inc_lessons()

    pupil_jane.mark_task("leson1", "B")
    pupil_jane.mark_task("leson2", "C")
    pupil_jane.inc_lessons()
    pupil_jane.inc_lessons()

    print("{0}".format(course_math))

if __name__ == "__main__":
    main()