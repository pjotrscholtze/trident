# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
# package madgik.exareme.utils.simulatedAnnealing;
import math
from simulatedAnnealing.Temperature import Temperature
# /**
#  * @author herald
#  */
# public class LogarithmicTemperature implements Temperature {
class LogarithmicTemperature(Temperature):
#     private static final long serialVersionUID = 1L;
#     private final double d;

#     public LogarithmicTemperature(double d) {
#         this.d = d;
#     }
    def __init__(self, d: float): self.d = d

#     @Override public double getTemperature(int step) {
    def getTemperature(self, step: int) -> float:
#         return d / Math.log((double) step);
        try:
            return self.d / math.log(float(step))
        except ValueError: return -float("inf") # because Java does not handle these border cases: https://www.geeksforgeeks.org/java-math-log-method-example/
        except ZeroDivisionError: # Neither does Java handle this one: https://stackoverflow.com/questions/50089498/how-to-set-the-root-directory-for-visual-studio-code-python-extension
            res = float("inf")
            if self.d < 0: res = -res
            return res
#     }
# }
