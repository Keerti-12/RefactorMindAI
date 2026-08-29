package sample_java;

public class PremiumCustomer extends Customer {

    private double creditLimit;

    public PremiumCustomer(String customerId, String email, double creditLimit) {
        super(customerId, "VIP", email);
        this.creditLimit = creditLimit;
    }

    public double getCreditLimit() {
        return creditLimit;
    }
}