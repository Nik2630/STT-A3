using System;

namespace Lab10
{
    public class LoopFunctionDemo
    {
        // For loop
        public void PrintNumbers1To10()
        {
            Console.WriteLine("--- For Loop ---");
            Console.Write("Numbers 1 to 10: ");
            for (int i = 1; i <= 10; i++)
            {
                Console.Write($"{i} ");
            }
            Console.WriteLine(); 
        }

        // While loop
        public void UserInputLoop()
        {
            Console.WriteLine("\n--- While Loop ---");
            string input = "";
            // Keep asking until user types 'exit'
            while (input.Trim().ToLower() != "exit")
            {
                Console.Write("Enter text (or 'exit' to stop): ");
                input = Console.ReadLine();
                Console.WriteLine($"You entered: {input}");
            }
            Console.WriteLine("Exited the input loop.");
        }

        // Factorial function 
        public long CalculateFactorial(int number)
        {
            if (number < 0) return -1; // Indicate error for negative input
            if (number == 0) return 1;

            long factorialResult = 1;
            try
            {
                
                checked
                {
                    for (int i = 1; i <= number; i++)
                    {
                        factorialResult *= i;
                    }
                }
            }
            catch (OverflowException)
            {
                Console.WriteLine($"\nWarning: Factorial calculation overflowed for {number}.");
                return -2; // Indicate overflow error
            }
            return factorialResult;
        }

        // Method using the factorial function
        public void RunFactorialCalculator()
        {
            Console.WriteLine("\n--- Factorial Function ---");
            Console.Write("Enter a non-negative integer for factorial: ");
            string input = Console.ReadLine(); 

            if (int.TryParse(input, out int number))
            {
                long result = CalculateFactorial(number); 

                if (result == -1)
                {
                     Console.WriteLine("Factorial is not defined for negative numbers.");
                }
                else if (result != -2) // Check it wasn't an overflow indicator
                {
                     Console.WriteLine($"The factorial of {number} is {result}.");
                }
            }
            else
            {
                Console.WriteLine("Invalid input. Please enter an integer.");
            }
        }
    }

    // --- Main Program Execution ---
    class Program
    {
        static void Main(string[] args)
        {
            LoopFunctionDemo demo = new LoopFunctionDemo();

            demo.PrintNumbers1To10();
            demo.UserInputLoop();
            demo.RunFactorialCalculator();

            Console.WriteLine("\nPress any key to exit.");
            Console.ReadKey();
        }
    }
}