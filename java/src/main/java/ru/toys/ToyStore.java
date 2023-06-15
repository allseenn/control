package ru.toys;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;

public class ToyStore {
    private ArrayList<Toy> toys;
    private ArrayList<Toy> prizeToys;
    private String prizeToyFile;

    public ToyStore(String prizeToyFile) {
        this.toys = new ArrayList<>();
        this.prizeToys = new ArrayList<>();
        this.prizeToyFile = prizeToyFile;
    }

    public void addToy(int id, String name, int quantity, double weight) {
        toys.add(new Toy(id, name, quantity, weight));
        System.out.println("Добавлена игрушка: " + name);
    }

    public void changeWeight(int id, double weight) {
        for (Toy toy : toys) {
            if (toy.getId() == id) {
                toy.setWeight(weight);
                System.out.println("Изменен вес игрушки " + toy.getName() + " на " + weight);
                break;
            }
        }
    }

    public void drawToy() {
        double totalWeight = 0;
        for (Toy toy : toys) {
            totalWeight += toy.getWeight();
        }

        double randomValue = new Random().nextDouble() * totalWeight;
        for (Toy toy : toys) {
            randomValue -= toy.getWeight();
            if (randomValue <= 0) {
                prizeToys.add(toy);
                toy.setQuantity(toy.getQuantity() - 1);
                System.out.println("Выбрана призовая игрушка: " + toy.getName());
                break;
            }
        }
    }

    public void getPrizeToy() {
        if (!prizeToys.isEmpty()) {
            Toy prizeToy = prizeToys.remove(0);
            try (FileWriter writer = new FileWriter(prizeToyFile, true)) {
                writer.write(prizeToy.getName() + "\n");
                System.out.println("Получена призовая игрушка: " + prizeToy.getName());
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private class Toy {
        private int id;
        private String name;
        private int quantity;
        private double weight;

        public Toy(int id, String name, int quantity, double weight) {
            this.id = id;
            this.name = name;
            this.quantity = quantity;
            this.weight = weight;
        }

        public int getId() {
            return id;
        }

        public String getName() {
            return name;
        }

        public int getQuantity() {
            return quantity;
        }

        public void setQuantity(int quantity) {
            this.quantity = quantity;
        }

        public double getWeight() {
            return weight;
        }

        public void setWeight(double weight) {
            this.weight = weight;
        }
    }
}
