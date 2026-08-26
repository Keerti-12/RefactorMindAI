package sample_java;

public class Customer {
    private String customerId;
    private String customerType; // "VIP" or "REGULAR"
    private String email;

    public Customer(String customerId, String customerType, String email) {
        this.customerId = customerId;
        this.customerType = customerType;
        this.email = email;
    }

    public String getCustomerId() {
        return customerId;
    }

    public String getCustomerType() {
        return customerType;
    }

    public String getEmail() {
        return email;
    }
}