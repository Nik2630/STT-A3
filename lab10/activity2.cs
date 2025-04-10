using System;

namespace Lab10
{
    public class Calculator
    {
        public void PerformCalculations()
        {
            double num1, num2;

            Console.WriteLine("--- Basic Calculator ---");

            Console.Write("Enter the first number: ");
            string input1 = Console.ReadLine(); 
            if (!double.TryParse(input1, out num1))
            {
                Console.WriteLine("Invalid input for the first number.");
                return;
            }

            Console.Write("Enter the second number: ");
            string input2 = Console.ReadLine();
            if (!double.TryParse(input2, out num2))
            {
                Console.WriteLine("Invalid input for the second number.");
                return;
            }

            double sum = num1 + num2;
            double difference = num1 - num2;
            double product = num1 * num2;

            Console.WriteLine("\n--- Results ---");
            Console.WriteLine($"Addition:       {num1} + {num2} = {sum}");
            Console.WriteLine($"Subtraction:    {num1} - {num2} = {difference}");
            Console.WriteLine($"Multiplication: {num1} * {num2} = {product}");

            if (num2 != 0)
            {
                double quotient = num1 / num2;
                Console.WriteLine($"Division:       {num1} / {num2} = {quotient}");
            }
            else
            {
                Console.WriteLine("Division:       Cannot divide by zero.");
            }

             if (sum == Math.Floor(sum)) // Check if sum is effectively an integer
             {
                if (sum % 2 == 0)
                {
                    Console.WriteLine($"The sum ({sum}) is an Even number.");
                }
                else
                {
                    Console.WriteLine($"The sum ({sum}) is an Odd number.");
                }
             }
             else
             {
                Console.WriteLine($"The sum ({sum}) is not a whole number, even/odd check not applicable.");
             }
        }
    }

    // --- Main Program Execution ---
    class Program
    {
        static void Main(string[] args)
        {
            Calculator myCalculator = new Calculator();
            myCalculator.PerformCalculations();

            Console.WriteLine("\nPress any key to exit.");
            Console.ReadKey();
        }
    }
}