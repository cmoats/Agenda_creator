'''Cameron Moats
creates an appointment schedule to tell us if there are any conflicts or not and return us the conflicts'''
from datetime import datetime

class Appt:
    """ Makes an appointment with a start time, finish time and
     a description of that appointment
    """

    def __init__(self, start: datetime, finish: datetime, desc: str):
        """An appointment from start time to finish time, with description desc.
        Start and finish should be the same day.
        """
        assert finish > start, f"Period finish ({finish}) must be after start ({start})"
        self.start = start
        self.finish = finish
        self.desc = desc

    def __lt__(self, other: 'Appt') -> bool:
        """Tells us if appointment a starts before appointment b """
        return self.finish <= other.start

    def __gt__(self, other: 'Appt') -> bool:
        """ Tells us if appointment a starts later than b"""
        return self.start >= other.finish

    def __eq__(self, other: 'Appt') -> bool:
        """Tells us if two appointments have the same start and finish time"""
        return self.start == other.start and self.finish == other.finish

    def overlaps(self, other: 'Appt') -> bool:
        """tells if two appointments overlap"""
        if (self).__lt__(other) and (self).__gt__(other) == False:
          return False
        else:
          return True

    def intersect(self, other: 'Appt') -> 'Appt':
        """Gives us the overlapping period of two appointment objects"""
        assert self.overlaps(other)  # Precondition
        inter_start = max(self.start, other.start) #start of overlapping appointments
        inter_finish = min(self.finish, other.finish) #end of overlapping
        return Appt(inter_start, inter_finish, self.desc + ' and ' + other.desc)

    def __str__(self) -> str:
        """Gives us the textual format of an appointment:
        yyyy-mm-dd hh:mm hh:mm
        """
        date_iso = self.start.date().isoformat()
        start_iso = self.start.time().isoformat(timespec='minutes')
        finish_iso = self.finish.time().isoformat(timespec='minutes')
        return f"{date_iso} {start_iso} {finish_iso} | {self.desc}"

    def __repr__(self) -> str:
        return f"Appt({repr(self.start)}, {repr(self.finish)}, {repr(self.desc)})"


class Agenda:
    """creates an object with a list of appointments"""
    def __init__(self):
        """creates"""
        self.elements = [ ]

    def __eq__(self, other: 'Agenda') -> bool:
        """tells us if our agenda is equal"""
        return self.elements == other.elements

    def __len__(self) -> int:
        """tells us how many appointments we have"""
        length = len(self.elements)
        return length

    def append(self, other: 'Appt') -> tuple:
        """adds an appointment to agenda"""
        return self.elements.append(other)

    def __str__(self) -> str:
        """Makes each appointment on a different line"""
        lines = [str(e) for e in self.elements]
        return "\n".join(lines)

    def __repr__(self) -> str:
        """The constructor does not actually work this way"""
        return f"Agenda({self.elements})"

    def sort(self):
        """Sorts the agenda by the start time of an appointment"""
        self.elements.sort(key=lambda appt: appt.start)

    def conflicts(self) -> 'Agenda':
        """"gives us an agenda of conflicting appointments. Agenda gets sorted"""
        self.sort()
        conflict_agenda = Agenda()
        for i in range (len(self.elements)):
            for j in range (i+1, len(self.elements)):
                if self.elements[i].overlaps(self.elements[j]):
                    conflict_agenda.append(self.elements[i].intersect(self.elements[j])) #adds each conflict to conflict agenda
                else:
                    break

        return conflict_agenda



if __name__== "__main__":
    print("Running usage examples")
    appt1 = Appt(datetime(2018, 3, 15, 13, 30), datetime(2018, 3, 15, 15, 30), "Early afternoon nap")
    appt2 = Appt(datetime(2018, 3, 15, 15, 00), datetime(2018, 3, 15, 16, 00), "Coffee break")
    if appt2 > appt1:
        print(f"appt1 '{appt1}' was over when appt2 '{appt2}'  started")
    elif appt1.overlaps(appt2):
        print("Oh no, a conflict in the schedule!")
        print(appt1.intersect(appt2))
    agenda = Agenda()
    agenda.append(appt1)
    agenda.append(appt2)
    ag_conflicts = agenda.conflicts()
    if len(ag_conflicts) == 0:
        print(f"Agenda has no conflicts")
    else:
        print(f"In agenda:\n{agenda}")
        print(f"Conflicts:\n {ag_conflicts}")