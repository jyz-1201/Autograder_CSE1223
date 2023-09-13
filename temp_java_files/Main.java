import java.util.Scanner;
public class Main {
public static void main(String[] args) {

Scanner input = new Scanner(System.in);
    // TODO: Your code below this line

 // Prompt the user to enter the first number
        System.out.print("Enter the first: ");
        int firstNum = input.nextInt();

        // Prompt the user to enter the second number
        System.out.print("Enter the second: ");
        int secondNum = input.nextInt();

        // Consume the newline character left by nextInt()
        input.nextLine();

        // Prompt the user to enter their name
        System.out.print("Enter your name: ");
        String name = input.nextLine();

        // Calculate the sum of the two numbers
        int sum = firstNum + secondNum;

        // Display the result with a message
        System.out.println(name + ", the sum is " + sum);

        input.close();
    }
}
}