package sample_java;

import java.util.Date;

public class OrderProcessor {
    
    // SMELL 1: Tight coupling. No Dependency Injection.
    private DatabaseConnection db = new DatabaseConnection();

    // SMELL 2: God method with deep nesting and undocumented business rules.
    public boolean processOrder(String orderId, double amount, String customerType) {
        if (orderId != null && !orderId.isEmpty()) {
            if (amount > 0) {
                double discount = 0.0;
                
                // SMELL 3: Hardcoded magic strings and logic
                if (customerType.equals("VIP")) {
                    discount = amount * 0.10;
                } else if (customerType.equals("REGULAR")) {
                    discount = amount * 0.05;
                }

                double finalAmount = amount - discount;
                
                // SMELL 4: Outdated API usage (java.util.Date instead of java.time.Instant)
                Date now = new Date();
                System.out.println("Processing at: " + now.toString());

                try {
                    // SMELL 5: Direct DB call makes this very hard to unit test safely
                    db.saveOrder(orderId, finalAmount);
                    return true;
                } catch (Exception e) {
                    // SMELL 6: Poor exception handling
                    System.out.println("Error saving order: " + e.getMessage());
                    return false;
                }
            }
        }
        return false;
    }
}

// Dummy class to simulate a database for our controlled environment
class DatabaseConnection {
    public void saveOrder(String id, double amount) throws Exception {
        System.out.println("Connecting to legacy Oracle DB... saving " + id);
    }
}