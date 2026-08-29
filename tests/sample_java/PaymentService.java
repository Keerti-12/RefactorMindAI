package sample_java;

import inventory.InventoryService;
import sample_java.Customer;

public class PaymentService {

    // CROSS-FILE DEPENDS_ON: field type is Customer, defined in Customer.java
    private Customer customer;
    private InventoryService inventoryService;
    private DatabaseConnection db = new DatabaseConnection();

    public PaymentService(Customer customer) {
        this.customer = customer;
    }

    // CROSS-FILE CALLS: calls customer.getCustomerType() — method defined in
    // Customer.java
    public boolean processPayment(double amount) {
        String type = customer.getCustomerType();

        double fee = 0.0;
        if (type.equals("VIP")) {
            fee = amount * 0.01;
        } else {
            fee = amount * 0.03;
        }

        double totalAmount = amount + fee;

        inventoryService.reserveStock((int) amount);
        try {
            db.saveOrder("PAY-" + customer.getCustomerId(), totalAmount);
            return true;
        } catch (Exception e) {
            System.out.println("Payment failed: " + e.getMessage());
            return false;
        }
    }
}