using System;

namespace Lab10
{
    public class Calculator
    {

        public void PerformCalculationsWithExceptions()
        {
            double num1 = 0, num2 = 0;

            Console.WriteLine("--- Calculator with Exception Handling ---"); 

            try
            {
                // Handle invalid number format input
                Console.Write("Enter the first number: ");
                string input1 = Console.ReadLine();
                num1 = double.Parse(input1); // Parse can throw FormatException

                Console.Write("Enter the second number: ");
                string input2 = Console.ReadLine();
                num2 = double.Parse(input2);

                // --- Calculations ---
                double sum = num1 + num2;
                double difference = num1 - num2;
                double product = num1 * num2;

                Console.WriteLine("\n--- Results ---");
                Console.WriteLine($"Addition:       {num1} + {num2} = {sum}");
                Console.WriteLine($"Subtraction:    {num1} - {num2} = {difference}");
                Console.WriteLine($"Multiplication: {num1} * {num2} = {product}");

                // Handle division by zero
                
                try
                {
                    if (num2 == 0)
                    {
                         Console.WriteLine("Division: Attempted to divide by zero.");
                         
                    }
                    else
                    {
                       double quotient = num1 / num2;
                       Console.WriteLine($"Division:       {num1} / {num2} = {quotient}");
                    }
                }
                catch (DivideByZeroException) 
                {
                    Console.WriteLine("Division Error: Cannot divide by zero.");
                }

                // Check if sum is even or odd 
                 if (sum == Math.Floor(sum))
                 {
                     if (sum % 2 == 0) Console.WriteLine($"The sum ({sum}) is an Even number.");
                     else Console.WriteLine($"The sum ({sum}) is an Odd number.");
                 }
                 else
                 {
                     Console.WriteLine($"The sum ({sum}) is not a whole number, even/odd check not applicable.");
                 }

            }
            catch (FormatException)
            {
                Console.WriteLine("Input Error: Invalid number format entered."); 
            }
            catch (Exception ex) // Catch any other unexpected errors
            {
                Console.WriteLine($"An unexpected error occurred: {ex.Message}");
            }
        }
    }

    // --- Main Program Execution ---
    class Program
    {
        static void Main(string[] args)
        {
            Calculator myCalculator = new Calculator();
            myCalculator.PerformCalculationsWithExceptions();

            Console.WriteLine("\nPress any key to exit.");
            Console.ReadKey();
        }
    }
}