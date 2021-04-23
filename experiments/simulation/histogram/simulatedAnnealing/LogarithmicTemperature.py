# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
import math
from simulatedAnnealing.Temperature import Temperature

# /**
#  * @author herald
#  */
class LogarithmicTemperature(Temperature):

    def __init__(self, d: float): self.d = d

    def getTemperature(self, step: int) -> float:
        try:
            return self.d / math.log(float(step))
        except ValueError: return -float("inf") # because Java does not handle these border cases: https://www.geeksforgeeks.org/java-math-log-method-example/
        except ZeroDivisionError: # Neither does Java handle this one: https://stackoverflow.com/questions/50089498/how-to-set-the-root-directory-for-visual-studio-code-python-extension
            res = float("inf")
            if self.d < 0: res = -res
            return res
