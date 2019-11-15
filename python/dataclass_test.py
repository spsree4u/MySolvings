
# Data class example
from dataclasses import dataclass, field, asdict, astuple


def get_avg_age():
    ages = [20, 22, 24, 26]
    return sum(ages)//len(ages)


@dataclass(init=True, repr=True, eq=True, order=True, frozen=False, unsafe_hash=True)
class Student:
    name: str = field()
    is_senior: bool = field(init=False)
    city: str = field(init=False, default='tcr', repr=False, hash=False)
    age: int = field(default_factory=get_avg_age, compare=False, metadata={'format': 'year'})

    def __post_init__(self):
        self.is_senior = True if self.age >= 60 else False


s1 = Student(name='sree', age=25)
s2 = Student(name='sree', age=26)

print(s1)
print(s1 == s2)
print(s1 > s2)
# s1.name = 'jith'
# print(s1)
print(hash(s1))
s1.name = 'jith'
print(hash(s1))
# print(s1.__dataclass_fields__['name'])
s3 = Student(name='hello')
print(s3)
print(s3.city)
print(s1.__dataclass_fields__['age'].metadata['format'])
s4 = Student(name='hoi', age=60)
print(s4)


@dataclass
class Marks:
    sub1: int
    sub2: int


m = Marks(sub1=90, sub2=85)


@dataclass
class GradStudent(Student):
    specialisation: str = "Maths"
    mrks: Marks = m
    age: int = 21


gs = GradStudent(name='sruthi')
print(gs)
print(asdict(gs))
print(astuple(gs))


# news
print(12_345_67)
print(0xbad_c0ffee)
print(0b_0111_1000_1101_0001)
error = 21738129726
print(f'{error:#x}')


def fun2(a: int, b: int=10) -> int:
    print(a + b)


fun2(3)
