package ru.toys;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        ToyStore store = new ToyStore("prizeToys.txt");
        int count = new Scanner(System.in).nextLine();
        store.addToy(1, "Мяч", 10, 0.2);
        store.addToy(2, "Кукла", 5, 0.3);
        store.addToy(3, "Машинка", 7, 0.5);

        store.drawToy();
        store.drawToy();
        store.drawToy();

        store.getPrizeToy();
    }
}
