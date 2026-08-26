package inventory;

import inventory.Product;

public class InventoryService {

    // CROSS-FILE DEPENDS_ON: field type is Product, defined in Product.java
    private Product product;

    public InventoryService(Product product) {
        this.product = product;
    }

    // CROSS-FILE CALLS: calls product.getQuantity() and product.reduceQuantity()
    public boolean reserveStock(int requestedQuantity) {
        int available = product.getQuantity();

        if (available >= requestedQuantity) {
            product.reduceQuantity(requestedQuantity);
            return true;
        }

        return false;
    }

    public String getProductInfo() {
        return product.getProductId();
    }
}