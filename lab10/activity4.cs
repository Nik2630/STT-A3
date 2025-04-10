using System;

namespace Lab10
{
    public class Student
    {
        public string Name { get; set; }
        public string ID { get; set; } 
        public double Marks { get; set; }

        // Constructor
        public Student(string name, string id, double marks)
        {
            Name = name;
            ID = id;
            Marks = marks;
        }

        public Student(Student other)
        {
            Name = other.Name;
            ID = other.ID;
            Marks = other.Marks;
        }

        public Student(string name, string id) : this(name, id, 0.0) { } 

        // Method to get grade 
        public virtual string GetGrade()
        {
            if (Marks >= 90) return "A";
            else if (Marks >= 80) return "B";
            else if (Marks >= 70) return "C";
            else if (Marks >= 60) return "D";
            else return "F";
        }

        // Method to display details 
        public virtual void DisplayDetails()
        {
            Console.WriteLine($"--- Student Details ---");
            Console.WriteLine($"Name:  {Name}");
            Console.WriteLine($"ID:    {ID}");
            Console.WriteLine($"Marks: {Marks}");
            Console.WriteLine($"Grade: {GetGrade()}");
        }
         // A static Main() could exist here, but only one Main can be the entry point.
         // The CLR looks for a static Main method to start execution.
    }

    public class StudentIITGN : Student
    {
        public string Hostel_Name_IITGN { get; set; }

        // Constructor for derived class 
        public StudentIITGN(string name, string id, double marks, string hostelName)
            : base(name, id, marks) // Call base class constructor
        {
            Hostel_Name_IITGN = hostelName;
        }

        // Override DisplayDetails to add hostel name
        public override void DisplayDetails()
        {
            base.DisplayDetails(); // Call base method first
            Console.WriteLine($"Hostel:{Hostel_Name_IITGN}");
        }

        // If both base and derived have static Main(), only the one designated
        // as the entry point (usually in Program class) runs automatically.
    }

    // --- Main Program Execution ---
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("--- OOP ---");

            Console.WriteLine("\n--- Creating Base Student ---");
            Student student1 = new Student("name1", "S101", 85.5); 
            student1.DisplayDetails();

            Console.WriteLine("\n--- Creating IITGN Student ---");
            StudentIITGN iitgnStudent1 = new StudentIITGN("name2", "22211007", 92.0, "Nehru Hall"); 
            iitgnStudent1.DisplayDetails(); // Calls overridden method

            Console.WriteLine("\n--- Using Copy Constructor ---");
            Student student2 = new Student(student1);
            student2.Name = "name1 Copy"; 
            student2.DisplayDetails();

            Console.WriteLine("\n--- Using Overloaded Constructor ---");
            Student student3 = new Student("name3", "S103");
            student3.DisplayDetails();

            Console.WriteLine("\n--- Polymorphism ---");
            Student polyStudent = iitgnStudent1; 
            polyStudent.DisplayDetails(); 

            Console.WriteLine("\nPress any key to exit.");
            Console.ReadKey();
        }
    }
}